"""
EAGLES - API de Gestão de Presença e Faltas
Módulo responsável pelo registro de presença, faltas e gestão de escalas
"""

from flask import Flask, request, jsonify
from datetime import datetime, date, time, timedelta
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


def validar_token_sessao(f):
    """Decorator para validar token de sessão nas rotas protegidas"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'erro': 'Token de autenticação não fornecido'}), 401
        
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


@app.route('/api/presenca/escala-dia', methods=['GET'])
@validar_token_sessao
def obter_escala_dia():
    """
    Obtém a escala de trabalho do dia para o gerente
    Query params:
    - id_cliente: ID do cliente
    - data: Data da escala (formato YYYY-MM-DD, opcional, padrão hoje)
    """
    if request.usuario_autenticado['tipo_usuario'] not in ['GERENTE', 'CONTADOR']:
        return jsonify({'erro': 'Acesso negado'}), 403
    
    id_cliente = request.args.get('id_cliente')
    data_escala = request.args.get('data', date.today().isoformat())
    
    if not id_cliente:
        return jsonify({'erro': 'id_cliente é obrigatório'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cursor.execute("""
            SELECT 
                f.id_funcionario,
                f.nome_completo,
                f.cargo,
                e.id_escala,
                e.turno,
                e.hora_inicio,
                e.hora_fim,
                e.observacao,
                rp.status_presenca,
                rp.tipo_justificativa,
                rp.hora_checkin,
                rp.motivo
            FROM funcionarios f
            LEFT JOIN escalas_trabalho e ON f.id_funcionario = e.id_funcionario 
                AND e.data_escala = %s
            LEFT JOIN registros_presenca rp ON f.id_funcionario = rp.id_funcionario 
                AND rp.data_registro = %s
            WHERE f.id_cliente = %s AND f.ativo = TRUE
            ORDER BY e.hora_inicio, f.nome_completo
        """, (data_escala, data_escala, id_cliente))
        
        funcionarios = cursor.fetchall()
        
        # Organiza por turno
        escalas = {
            'MANHA': [],
            'TARDE': [],
            'NOITE': [],
            'INTEGRAL': [],
            'SEM_ESCALA': []
        }
        
        for func in funcionarios:
            turno = func['turno'] if func['turno'] else 'SEM_ESCALA'
            escalas[turno].append({
                'id_funcionario': func['id_funcionario'],
                'nome': func['nome_completo'],
                'cargo': func['cargo'],
                'id_escala': func['id_escala'],
                'hora_inicio': str(func['hora_inicio']) if func['hora_inicio'] else None,
                'hora_fim': str(func['hora_fim']) if func['hora_fim'] else None,
                'observacao': func['observacao'],
                'status_presenca': func['status_presenca'],
                'tipo_justificativa': func['tipo_justificativa'],
                'hora_checkin': str(func['hora_checkin']) if func['hora_checkin'] else None,
                'motivo': func['motivo']
            })
        
        return jsonify({
            'sucesso': True,
            'data': data_escala,
            'total_funcionarios': len(funcionarios),
            'escalas': escalas
        }), 200
        
    finally:
        cursor.close()
        conn.close()


@app.route('/api/presenca/registrar-checkin', methods=['POST'])
@validar_token_sessao
def registrar_checkin():
    """
    Registra check-in (presença) de um funcionário
    
    Body JSON:
    {
        "id_funcionario": 123,
        "data_registro": "2025-01-15" (opcional, padrão hoje),
        "hora_checkin": "08:30" (opcional, padrão agora),
        "status_presenca": "PRESENTE" (opcional, padrão PRESENTE)
    }
    """
    if request.usuario_autenticado['tipo_usuario'] != 'GERENTE':
        return jsonify({'erro': 'Apenas gerentes podem registrar check-in'}), 403
    
    dados = request.get_json()
    id_funcionario = dados.get('id_funcionario')
    data_registro = dados.get('data_registro', date.today().isoformat())
    hora_checkin = dados.get('hora_checkin', datetime.now().strftime('%H:%M:%S'))
    status_presenca = dados.get('status_presenca', 'PRESENTE')
    
    if not id_funcionario:
        return jsonify({'erro': 'id_funcionario é obrigatório'}), 400
    
    if status_presenca not in ['PRESENTE', 'ATRASO']:
        return jsonify({'erro': 'status_presenca deve ser PRESENTE ou ATRASO'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # Verifica se já existe registro para o dia
        cursor.execute("""
            SELECT id_registro FROM registros_presenca
            WHERE id_funcionario = %s AND data_registro = %s
        """, (id_funcionario, data_registro))
        
        registro_existente = cursor.fetchone()
        
        if registro_existente:
            return jsonify({'erro': 'Já existe registro de presença para este funcionário hoje'}), 409
        
        # Verifica se o funcionário está na escala
        cursor.execute("""
            SELECT id_escala, hora_inicio, turno
            FROM escalas_trabalho
            WHERE id_funcionario = %s AND data_escala = %s
        """, (id_funcionario, data_registro))
        
        escala = cursor.fetchone()
        
        # Determina se é atraso (se houver escala)
        if escala and escala['hora_inicio']:
            hora_escala = escala['hora_inicio']
            hora_checkin_obj = datetime.strptime(hora_checkin, '%H:%M:%S').time()
            
            # Tolerância de 15 minutos
            hora_limite = (datetime.combine(date.today(), hora_escala) + timedelta(minutes=15)).time()
            
            if hora_checkin_obj > hora_limite:
                status_presenca = 'ATRASO'
        
        # Registra presença
        cursor.execute("""
            INSERT INTO registros_presenca (
                id_funcionario, data_registro, status_presenca,
                tipo_justificativa, hora_checkin, id_gerente
            ) VALUES (%s, %s, %s, 'NAO_APLICAVEL', %s, %s)
            RETURNING id_registro
        """, (
            id_funcionario, data_registro, status_presenca,
            hora_checkin, request.usuario_autenticado['id_usuario']
        ))
        
        id_registro = cursor.fetchone()['id_registro']
        conn.commit()
        
        return jsonify({
            'sucesso': True,
            'mensagem': 'Check-in registrado com sucesso',
            'id_registro': id_registro,
            'status_presenca': status_presenca,
            'hora_checkin': hora_checkin
        }), 201
        
    except Exception as e:
        conn.rollback()
        return jsonify({'erro': f'Erro ao registrar check-in: {str(e)}'}), 500
        
    finally:
        cursor.close()
        conn.close()


@app.route('/api/presenca/registrar-falta', methods=['POST'])
@validar_token_sessao
def registrar_falta():
    """
    Registra falta de um funcionário
    
    Body JSON:
    {
        "id_funcionario": 123,
        "data_registro": "2025-01-15" (opcional, padrão hoje),
        "tipo_justificativa": "JUSTIFICADA" ou "INJUSTIFICADA",
        "motivo": "Atestado médico" (opcional)
    }
    """
    if request.usuario_autenticado['tipo_usuario'] != 'GERENTE':
        return jsonify({'erro': 'Apenas gerentes podem registrar faltas'}), 403
    
    dados = request.get_json()
    id_funcionario = dados.get('id_funcionario')
    data_registro = dados.get('data_registro', date.today().isoformat())
    tipo_justificativa = dados.get('tipo_justificativa')
    motivo = dados.get('motivo')
    
    if not id_funcionario or not tipo_justificativa:
        return jsonify({'erro': 'id_funcionario e tipo_justificativa são obrigatórios'}), 400
    
    if tipo_justificativa not in ['JUSTIFICADA', 'INJUSTIFICADA']:
        return jsonify({'erro': 'tipo_justificativa deve ser JUSTIFICADA ou INJUSTIFICADA'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # Verifica se já existe registro para o dia
        cursor.execute("""
            SELECT id_registro FROM registros_presenca
            WHERE id_funcionario = %s AND data_registro = %s
        """, (id_funcionario, data_registro))
        
        registro_existente = cursor.fetchone()
        
        if registro_existente:
            return jsonify({'erro': 'Já existe registro de presença para este funcionário hoje'}), 409
        
        # Registra falta
        cursor.execute("""
            INSERT INTO registros_presenca (
                id_funcionario, data_registro, status_presenca,
                tipo_justificativa, motivo, id_gerente
            ) VALUES (%s, %s, 'FALTA', %s, %s, %s)
            RETURNING id_registro
        """, (
            id_funcionario, data_registro, tipo_justificativa,
            motivo, request.usuario_autenticado['id_usuario']
        ))
        
        id_registro = cursor.fetchone()['id_registro']
        conn.commit()
        
        return jsonify({
            'sucesso': True,
            'mensagem': 'Falta registrada com sucesso',
            'id_registro': id_registro,
            'tipo_justificativa': tipo_justificativa
        }), 201
        
    except Exception as e:
        conn.rollback()
        return jsonify({'erro': f'Erro ao registrar falta: {str(e)}'}), 500
        
    finally:
        cursor.close()
        conn.close()


@app.route('/api/presenca/resumo-mensal', methods=['GET'])
@validar_token_sessao
def obter_resumo_mensal():
    """
    Obtém resumo mensal de presença/faltas
    Query params:
    - id_cliente: ID do cliente
    - mes: Mês (1-12)
    - ano: Ano (YYYY)
    """
    id_cliente = request.args.get('id_cliente')
    mes = request.args.get('mes', datetime.now().month)
    ano = request.args.get('ano', datetime.now().year)
    
    if not id_cliente:
        return jsonify({'erro': 'id_cliente é obrigatório'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cursor.execute("""
            SELECT 
                f.id_funcionario,
                f.nome_completo,
                f.cargo,
                COUNT(CASE WHEN rp.status_presenca = 'PRESENTE' THEN 1 END) as total_presencas,
                COUNT(CASE WHEN rp.status_presenca = 'ATRASO' THEN 1 END) as total_atrasos,
                COUNT(CASE WHEN rp.status_presenca = 'FALTA' AND rp.tipo_justificativa = 'JUSTIFICADA' THEN 1 END) as faltas_justificadas,
                COUNT(CASE WHEN rp.status_presenca = 'FALTA' AND rp.tipo_justificativa = 'INJUSTIFICADA' THEN 1 END) as faltas_injustificadas
            FROM funcionarios f
            LEFT JOIN registros_presenca rp ON f.id_funcionario = rp.id_funcionario
                AND EXTRACT(MONTH FROM rp.data_registro) = %s
                AND EXTRACT(YEAR FROM rp.data_registro) = %s
            WHERE f.id_cliente = %s AND f.ativo = TRUE
            GROUP BY f.id_funcionario, f.nome_completo, f.cargo
            ORDER BY f.nome_completo
        """, (mes, ano, id_cliente))
        
        resumo = cursor.fetchall()
        
        return jsonify({
            'sucesso': True,
            'mes': mes,
            'ano': ano,
            'total_funcionarios': len(resumo),
            'resumo': resumo
        }), 200
        
    finally:
        cursor.close()
        conn.close()


@app.route('/api/presenca/criar-escala', methods=['POST'])
@validar_token_sessao
def criar_escala():
    """
    Cria escala de trabalho para um funcionário
    Apenas Contador pode criar escalas
    
    Body JSON:
    {
        "id_funcionario": 123,
        "data_escala": "2025-01-15",
        "turno": "MANHA",
        "hora_inicio": "08:00",
        "hora_fim": "12:00",
        "observacao": "Opcional"
    }
    """
    if request.usuario_autenticado['tipo_usuario'] != 'CONTADOR':
        return jsonify({'erro': 'Apenas contadores podem criar escalas'}), 403
    
    dados = request.get_json()
    id_funcionario = dados.get('id_funcionario')
    data_escala = dados.get('data_escala')
    turno = dados.get('turno')
    hora_inicio = dados.get('hora_inicio')
    hora_fim = dados.get('hora_fim')
    observacao = dados.get('observacao')
    
    if not all([id_funcionario, data_escala, turno]):
        return jsonify({'erro': 'id_funcionario, data_escala e turno são obrigatórios'}), 400
    
    if turno not in ['MANHA', 'TARDE', 'NOITE', 'INTEGRAL']:
        return jsonify({'erro': 'turno inválido'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cursor.execute("""
            INSERT INTO escalas_trabalho (
                id_funcionario, data_escala, turno, hora_inicio, hora_fim, observacao
            ) VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id_escala
        """, (id_funcionario, data_escala, turno, hora_inicio, hora_fim, observacao))
        
        id_escala = cursor.fetchone()['id_escala']
        conn.commit()
        
        return jsonify({
            'sucesso': True,
            'mensagem': 'Escala criada com sucesso',
            'id_escala': id_escala
        }), 201
        
    except psycopg2.IntegrityError:
        conn.rollback()
        return jsonify({'erro': 'Já existe escala para este funcionário nesta data/turno'}), 409
    except Exception as e:
        conn.rollback()
        return jsonify({'erro': f'Erro ao criar escala: {str(e)}'}), 500
        
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
