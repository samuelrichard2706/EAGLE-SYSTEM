"""
EAGLES - API da Lente do Contador
Módulo responsável pela ferramenta de observações contextualizadas do contador
sobre contas específicas do balancete
"""

from flask import Flask, request, jsonify
from datetime import datetime
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


@app.route('/api/lente/adicionar-observacao', methods=['POST'])
@validar_token_sessao
def adicionar_observacao():
    """
    Adiciona uma observação de consultoria a uma conta específica do balancete
    Apenas Contador pode adicionar observações
    
    Body JSON:
    {
        "id_lancamento": 123,
        "observacao_consultoria": "Texto da observação contextualizada",
        "destacado": true (opcional, padrão true)
    }
    """
    if request.usuario_autenticado['tipo_usuario'] != 'CONTADOR':
        return jsonify({'erro': 'Apenas contadores podem adicionar observações'}), 403
    
    dados = request.get_json()
    id_lancamento = dados.get('id_lancamento')
    observacao_consultoria = dados.get('observacao_consultoria')
    destacado = dados.get('destacado', True)
    
    if not id_lancamento or not observacao_consultoria:
        return jsonify({'erro': 'id_lancamento e observacao_consultoria são obrigatórios'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # Verifica se o lançamento existe
        cursor.execute("""
            SELECT lb.*, b.id_cliente, b.mes_referencia, b.ano_referencia
            FROM lancamentos_balancete lb
            JOIN balancetes b ON lb.id_balancete = b.id_balancete
            WHERE lb.id_lancamento = %s
        """, (id_lancamento,))
        
        lancamento = cursor.fetchone()
        
        if not lancamento:
            return jsonify({'erro': 'Lançamento não encontrado'}), 404
        
        # Adiciona observação
        cursor.execute("""
            INSERT INTO lente_contador (
                id_lancamento, id_contador, observacao_consultoria, destacado, aprovado
            ) VALUES (%s, %s, %s, %s, TRUE)
            RETURNING id_lente
        """, (
            id_lancamento,
            request.usuario_autenticado['id_usuario'],
            observacao_consultoria,
            destacado
        ))
        
        id_lente = cursor.fetchone()['id_lente']
        conn.commit()
        
        return jsonify({
            'sucesso': True,
            'mensagem': 'Observação adicionada com sucesso',
            'id_lente': id_lente,
            'conta': lancamento['nome_conta'],
            'codigo_conta': lancamento['codigo_conta']
        }), 201
        
    except Exception as e:
        conn.rollback()
        return jsonify({'erro': f'Erro ao adicionar observação: {str(e)}'}), 500
        
    finally:
        cursor.close()
        conn.close()


@app.route('/api/lente/editar-observacao/<int:id_lente>', methods=['PUT'])
@validar_token_sessao
def editar_observacao(id_lente):
    """
    Edita uma observação existente
    Apenas o Contador que criou pode editar
    
    Body JSON:
    {
        "observacao_consultoria": "Novo texto",
        "destacado": false (opcional)
    }
    """
    if request.usuario_autenticado['tipo_usuario'] != 'CONTADOR':
        return jsonify({'erro': 'Apenas contadores podem editar observações'}), 403
    
    dados = request.get_json()
    observacao_consultoria = dados.get('observacao_consultoria')
    destacado = dados.get('destacado')
    
    if not observacao_consultoria:
        return jsonify({'erro': 'observacao_consultoria é obrigatória'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # Verifica se a observação existe e pertence ao contador
        cursor.execute("""
            SELECT id_lente FROM lente_contador
            WHERE id_lente = %s AND id_contador = %s
        """, (id_lente, request.usuario_autenticado['id_usuario']))
        
        if not cursor.fetchone():
            return jsonify({'erro': 'Observação não encontrada ou sem permissão'}), 404
        
        # Atualiza observação
        if destacado is not None:
            cursor.execute("""
                UPDATE lente_contador
                SET observacao_consultoria = %s, destacado = %s
                WHERE id_lente = %s
            """, (observacao_consultoria, destacado, id_lente))
        else:
            cursor.execute("""
                UPDATE lente_contador
                SET observacao_consultoria = %s
                WHERE id_lente = %s
            """, (observacao_consultoria, id_lente))
        
        conn.commit()
        
        return jsonify({
            'sucesso': True,
            'mensagem': 'Observação atualizada com sucesso'
        }), 200
        
    except Exception as e:
        conn.rollback()
        return jsonify({'erro': f'Erro ao editar observação: {str(e)}'}), 500
        
    finally:
        cursor.close()
        conn.close()


@app.route('/api/lente/remover-observacao/<int:id_lente>', methods=['DELETE'])
@validar_token_sessao
def remover_observacao(id_lente):
    """
    Remove uma observação
    Apenas o Contador que criou pode remover
    """
    if request.usuario_autenticado['tipo_usuario'] != 'CONTADOR':
        return jsonify({'erro': 'Apenas contadores podem remover observações'}), 403
    
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # Verifica se a observação existe e pertence ao contador
        cursor.execute("""
            SELECT id_lente FROM lente_contador
            WHERE id_lente = %s AND id_contador = %s
        """, (id_lente, request.usuario_autenticado['id_usuario']))
        
        if not cursor.fetchone():
            return jsonify({'erro': 'Observação não encontrada ou sem permissão'}), 404
        
        # Remove observação
        cursor.execute("""
            DELETE FROM lente_contador WHERE id_lente = %s
        """, (id_lente,))
        
        conn.commit()
        
        return jsonify({
            'sucesso': True,
            'mensagem': 'Observação removida com sucesso'
        }), 200
        
    except Exception as e:
        conn.rollback()
        return jsonify({'erro': f'Erro ao remover observação: {str(e)}'}), 500
        
    finally:
        cursor.close()
        conn.close()


@app.route('/api/lente/listar-observacoes', methods=['GET'])
@validar_token_sessao
def listar_observacoes():
    """
    Lista observações de um balancete
    Query params:
    - id_cliente: ID do cliente
    - mes: Mês de referência
    - ano: Ano de referência
    - apenas_destacadas: true/false (opcional)
    """
    id_cliente = request.args.get('id_cliente')
    mes = request.args.get('mes')
    ano = request.args.get('ano')
    apenas_destacadas = request.args.get('apenas_destacadas', 'false').lower() == 'true'
    
    if not all([id_cliente, mes, ano]):
        return jsonify({'erro': 'id_cliente, mes e ano são obrigatórios'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        query = """
            SELECT 
                lc.id_lente,
                lc.observacao_consultoria,
                lc.destacado,
                lc.aprovado,
                lc.data_criacao,
                lb.codigo_conta,
                lb.nome_conta,
                lb.saldo_anterior,
                lb.debito,
                lb.credito,
                lb.saldo_atual,
                u.nome as contador_nome
            FROM lente_contador lc
            JOIN lancamentos_balancete lb ON lc.id_lancamento = lb.id_lancamento
            JOIN balancetes b ON lb.id_balancete = b.id_balancete
            JOIN usuarios u ON lc.id_contador = u.id_usuario
            WHERE b.id_cliente = %s 
            AND b.mes_referencia = %s 
            AND b.ano_referencia = %s
            AND lc.aprovado = TRUE
        """
        
        params = [id_cliente, mes, ano]
        
        if apenas_destacadas:
            query += " AND lc.destacado = TRUE"
        
        query += " ORDER BY lb.codigo_conta"
        
        cursor.execute(query, params)
        observacoes = cursor.fetchall()
        
        return jsonify({
            'sucesso': True,
            'total': len(observacoes),
            'mes_referencia': mes,
            'ano_referencia': ano,
            'observacoes': observacoes
        }), 200
        
    finally:
        cursor.close()
        conn.close()


@app.route('/api/lente/balancete-com-observacoes', methods=['GET'])
@validar_token_sessao
def obter_balancete_com_observacoes():
    """
    Obtém o balancete completo com as observações destacadas
    Usado pelo Dashboard do Dono
    
    Query params:
    - id_cliente: ID do cliente
    - mes: Mês de referência
    - ano: Ano de referência
    """
    id_cliente = request.args.get('id_cliente')
    mes = request.args.get('mes')
    ano = request.args.get('ano')
    
    if not all([id_cliente, mes, ano]):
        return jsonify({'erro': 'id_cliente, mes e ano são obrigatórios'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # Busca balancete
        cursor.execute("""
            SELECT * FROM balancetes
            WHERE id_cliente = %s AND mes_referencia = %s AND ano_referencia = %s
        """, (id_cliente, mes, ano))
        
        balancete = cursor.fetchone()
        
        if not balancete:
            return jsonify({'erro': 'Balancete não encontrado'}), 404
        
        # Busca lançamentos com observações
        cursor.execute("""
            SELECT 
                lb.id_lancamento,
                lb.codigo_conta,
                lb.nome_conta,
                lb.saldo_anterior,
                lb.debito,
                lb.credito,
                lb.saldo_atual,
                lc.id_lente,
                lc.observacao_consultoria,
                lc.destacado,
                u.nome as contador_nome,
                lc.data_criacao as data_observacao
            FROM lancamentos_balancete lb
            LEFT JOIN lente_contador lc ON lb.id_lancamento = lc.id_lancamento 
                AND lc.aprovado = TRUE AND lc.destacado = TRUE
            LEFT JOIN usuarios u ON lc.id_contador = u.id_usuario
            WHERE lb.id_balancete = %s
            ORDER BY lb.codigo_conta
        """, (balancete['id_balancete'],))
        
        lancamentos = cursor.fetchall()
        
        # Separa contas com e sem observações
        contas_destacadas = []
        contas_normais = []
        
        for lanc in lancamentos:
            if lanc['id_lente']:
                contas_destacadas.append(lanc)
            else:
                contas_normais.append(lanc)
        
        return jsonify({
            'sucesso': True,
            'balancete': {
                'id_balancete': balancete['id_balancete'],
                'mes_referencia': balancete['mes_referencia'],
                'ano_referencia': balancete['ano_referencia'],
                'data_importacao': balancete['data_importacao'].isoformat(),
                'status_processamento': balancete['status_processamento']
            },
            'total_contas': len(lancamentos),
            'total_destacadas': len(contas_destacadas),
            'contas_destacadas': contas_destacadas,
            'contas_normais': contas_normais
        }), 200
        
    finally:
        cursor.close()
        conn.close()


@app.route('/api/lente/estatisticas', methods=['GET'])
@validar_token_sessao
def obter_estatisticas():
    """
    Obtém estatísticas de uso da Lente do Contador
    Query params:
    - id_cliente: ID do cliente (opcional, se não fornecido retorna geral)
    - mes: Mês de referência (opcional)
    - ano: Ano de referência (opcional)
    """
    if request.usuario_autenticado['tipo_usuario'] != 'CONTADOR':
        return jsonify({'erro': 'Apenas contadores podem acessar estatísticas'}), 403
    
    id_cliente = request.args.get('id_cliente')
    mes = request.args.get('mes')
    ano = request.args.get('ano')
    
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        query = """
            SELECT 
                COUNT(lc.id_lente) as total_observacoes,
                COUNT(CASE WHEN lc.destacado = TRUE THEN 1 END) as total_destacadas,
                COUNT(DISTINCT lb.id_balancete) as balancetes_analisados,
                COUNT(DISTINCT b.id_cliente) as clientes_atendidos
            FROM lente_contador lc
            JOIN lancamentos_balancete lb ON lc.id_lancamento = lb.id_lancamento
            JOIN balancetes b ON lb.id_balancete = b.id_balancete
            WHERE lc.id_contador = %s
        """
        
        params = [request.usuario_autenticado['id_usuario']]
        
        if id_cliente:
            query += " AND b.id_cliente = %s"
            params.append(id_cliente)
        
        if mes and ano:
            query += " AND b.mes_referencia = %s AND b.ano_referencia = %s"
            params.extend([mes, ano])
        
        cursor.execute(query, params)
        estatisticas = cursor.fetchone()
        
        return jsonify({
            'sucesso': True,
            'estatisticas': estatisticas
        }), 200
        
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)
