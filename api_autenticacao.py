"""
EAGLES - API de Autenticação por QR Code
Módulo responsável pela geração e validação de QR Codes para autenticação
de Gerentes e Donos no sistema.
"""

from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import hashlib
import secrets
import qrcode
import io
import base64
import psycopg2
from psycopg2.extras import RealDictCursor
from functools import wraps

app = Flask(__name__)

# Configuração do banco de dados
DB_CONFIG = {
    'host': 'localhost',
    'database': 'eagles_db',
    'user': 'eagles_user',
    'password': 'eagles_password'
}

def get_db_connection():
    """Estabelece conexão com o banco de dados"""
    conn = psycopg2.connect(**DB_CONFIG)
    return conn

def gerar_token_seguro():
    """Gera um token aleatório seguro"""
    return secrets.token_urlsafe(32)

def validar_token_sessao(f):
    """Decorator para validar token de sessão nas rotas protegidas"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'erro': 'Token de autenticação não fornecido'}), 401
        
        # Remove o prefixo "Bearer " se presente
        if token.startswith('Bearer '):
            token = token[7:]
        
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            cursor.execute("""
                SELECT s.*, u.nome, u.tipo_usuario
                FROM sessoes s
                JOIN usuarios u ON s.id_usuario = u.id_usuario
                WHERE s.token_sessao = %s AND s.data_expiracao > NOW()
            """, (token,))
            
            sessao = cursor.fetchone()
            
            if not sessao:
                return jsonify({'erro': 'Token inválido ou expirado'}), 401
            
            request.usuario_autenticado = sessao
            return f(*args, **kwargs)
            
        finally:
            cursor.close()
            conn.close()
    
    return decorated_function


@app.route('/api/auth/gerar-qrcode', methods=['POST'])
@validar_token_sessao
def gerar_qrcode():
    """
    Gera um QR Code para autenticação de Gerente ou Dono
    Apenas o Contador (Samuel) pode gerar QR Codes
    
    Body JSON:
    {
        "id_usuario": 123,
        "tipo_acesso": "GERENTE" ou "DONO",
        "validade_horas": 24 (opcional, padrão 24h)
    }
    """
    # Verifica se o usuário autenticado é um contador
    if request.usuario_autenticado['tipo_usuario'] != 'CONTADOR':
        return jsonify({'erro': 'Apenas contadores podem gerar QR Codes'}), 403
    
    dados = request.get_json()
    id_usuario = dados.get('id_usuario')
    tipo_acesso = dados.get('tipo_acesso')
    validade_horas = dados.get('validade_horas', 24)
    
    # Validação dos dados
    if not id_usuario or not tipo_acesso:
        return jsonify({'erro': 'id_usuario e tipo_acesso são obrigatórios'}), 400
    
    if tipo_acesso not in ['GERENTE', 'DONO']:
        return jsonify({'erro': 'tipo_acesso deve ser GERENTE ou DONO'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # Verifica se o usuário existe e tem o tipo correto
        cursor.execute("""
            SELECT id_usuario, nome, tipo_usuario
            FROM usuarios
            WHERE id_usuario = %s AND tipo_usuario = %s AND ativo = TRUE
        """, (id_usuario, tipo_acesso))
        
        usuario = cursor.fetchone()
        
        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado ou tipo incompatível'}), 404
        
        # Gera token único
        token = gerar_token_seguro()
        data_expiracao = datetime.now() + timedelta(hours=validade_horas)
        
        # Insere o QR Code no banco
        cursor.execute("""
            INSERT INTO qr_codes (id_usuario, token, tipo_acesso, data_expiracao, ativo)
            VALUES (%s, %s, %s, %s, TRUE)
            RETURNING id_qr_code
        """, (id_usuario, token, tipo_acesso, data_expiracao))
        
        id_qr_code = cursor.fetchone()['id_qr_code']
        conn.commit()
        
        # Gera a imagem do QR Code
        qr_data = {
            'token': token,
            'tipo': tipo_acesso,
            'id_qr': id_qr_code
        }
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(str(qr_data))
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Converte a imagem para base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return jsonify({
            'sucesso': True,
            'id_qr_code': id_qr_code,
            'token': token,
            'usuario': usuario['nome'],
            'tipo_acesso': tipo_acesso,
            'data_expiracao': data_expiracao.isoformat(),
            'qrcode_base64': f'data:image/png;base64,{img_base64}'
        }), 201
        
    except Exception as e:
        conn.rollback()
        return jsonify({'erro': f'Erro ao gerar QR Code: {str(e)}'}), 500
        
    finally:
        cursor.close()
        conn.close()


@app.route('/api/auth/validar-qrcode', methods=['POST'])
def validar_qrcode():
    """
    Valida um QR Code e cria uma sessão de autenticação
    
    Body JSON:
    {
        "token": "token_do_qrcode",
        "dispositivo": "iPhone 13",
        "ip_address": "192.168.1.100"
    }
    """
    dados = request.get_json()
    token = dados.get('token')
    dispositivo = dados.get('dispositivo', 'Desconhecido')
    ip_address = dados.get('ip_address', request.remote_addr)
    
    if not token:
        return jsonify({'erro': 'Token é obrigatório'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # Busca o QR Code e valida
        cursor.execute("""
            SELECT qr.*, u.nome, u.email, u.tipo_usuario
            FROM qr_codes qr
            JOIN usuarios u ON qr.id_usuario = u.id_usuario
            WHERE qr.token = %s 
            AND qr.ativo = TRUE 
            AND qr.data_expiracao > NOW()
            AND u.ativo = TRUE
        """, (token,))
        
        qr_code = cursor.fetchone()
        
        if not qr_code:
            return jsonify({'erro': 'QR Code inválido ou expirado'}), 401
        
        # Cria uma nova sessão
        token_sessao = gerar_token_seguro()
        data_expiracao_sessao = datetime.now() + timedelta(hours=12)
        
        cursor.execute("""
            INSERT INTO sessoes (id_usuario, token_sessao, data_expiracao, dispositivo, ip_address)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_sessao
        """, (qr_code['id_usuario'], token_sessao, data_expiracao_sessao, dispositivo, ip_address))
        
        id_sessao = cursor.fetchone()['id_sessao']
        
        # Desativa o QR Code após uso (segurança)
        cursor.execute("""
            UPDATE qr_codes SET ativo = FALSE WHERE id_qr_code = %s
        """, (qr_code['id_qr_code'],))
        
        conn.commit()
        
        return jsonify({
            'sucesso': True,
            'token_sessao': token_sessao,
            'id_sessao': id_sessao,
            'usuario': {
                'id': qr_code['id_usuario'],
                'nome': qr_code['nome'],
                'email': qr_code['email'],
                'tipo': qr_code['tipo_usuario']
            },
            'data_expiracao': data_expiracao_sessao.isoformat()
        }), 200
        
    except Exception as e:
        conn.rollback()
        return jsonify({'erro': f'Erro ao validar QR Code: {str(e)}'}), 500
        
    finally:
        cursor.close()
        conn.close()


@app.route('/api/auth/logout', methods=['POST'])
@validar_token_sessao
def logout():
    """Encerra a sessão atual"""
    token = request.headers.get('Authorization')
    if token.startswith('Bearer '):
        token = token[7:]
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            DELETE FROM sessoes WHERE token_sessao = %s
        """, (token,))
        
        conn.commit()
        
        return jsonify({'sucesso': True, 'mensagem': 'Logout realizado com sucesso'}), 200
        
    except Exception as e:
        conn.rollback()
        return jsonify({'erro': f'Erro ao fazer logout: {str(e)}'}), 500
        
    finally:
        cursor.close()
        conn.close()


@app.route('/api/auth/validar-sessao', methods=['GET'])
@validar_token_sessao
def validar_sessao():
    """Valida se a sessão atual ainda é válida"""
    return jsonify({
        'sucesso': True,
        'usuario': {
            'id': request.usuario_autenticado['id_usuario'],
            'nome': request.usuario_autenticado['nome'],
            'tipo': request.usuario_autenticado['tipo_usuario']
        }
    }), 200


@app.route('/api/auth/listar-qrcodes-ativos', methods=['GET'])
@validar_token_sessao
def listar_qrcodes_ativos():
    """
    Lista todos os QR Codes ativos gerados pelo contador
    Apenas contadores podem acessar
    """
    if request.usuario_autenticado['tipo_usuario'] != 'CONTADOR':
        return jsonify({'erro': 'Acesso negado'}), 403
    
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cursor.execute("""
            SELECT qr.*, u.nome, u.email
            FROM qr_codes qr
            JOIN usuarios u ON qr.id_usuario = u.id_usuario
            WHERE qr.ativo = TRUE AND qr.data_expiracao > NOW()
            ORDER BY qr.data_geracao DESC
        """)
        
        qrcodes = cursor.fetchall()
        
        return jsonify({
            'sucesso': True,
            'total': len(qrcodes),
            'qrcodes': qrcodes
        }), 200
        
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
