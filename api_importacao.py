"""
EAGLES - API de Importação de XML (NF-e) e Planilhas de Estoque
Módulo responsável pela importação inteligente de documentos fiscais e atualização de estoque
"""

from flask import Flask, request, jsonify
import xml.etree.ElementTree as ET
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from decimal import Decimal
import os

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


def calcular_custo_medio_ponderado(saldo_anterior, custo_anterior, quantidade_entrada, custo_entrada):
    """
    Calcula o Custo Médio Ponderado
    CMP = (Saldo_Anterior * Custo_Anterior + Quantidade_Entrada * Custo_Entrada) / (Saldo_Anterior + Quantidade_Entrada)
    """
    if saldo_anterior + quantidade_entrada == 0:
        return Decimal('0.00')
    
    valor_estoque_anterior = saldo_anterior * custo_anterior
    valor_entrada = quantidade_entrada * custo_entrada
    novo_saldo = saldo_anterior + quantidade_entrada
    
    return (valor_estoque_anterior + valor_entrada) / novo_saldo


def extrair_dados_nfe_xml(xml_content):
    """
    Extrai dados relevantes de um XML de NF-e
    Retorna dicionário com informações da nota e lista de itens
    """
    try:
        # Namespace padrão da NF-e
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        
        root = ET.fromstring(xml_content)
        
        # Extrai informações da nota
        inf_nfe = root.find('.//nfe:infNFe', ns)
        chave_acesso = inf_nfe.get('Id', '').replace('NFe', '')
        
        ide = root.find('.//nfe:ide', ns)
        numero_nota = ide.find('nfe:nNF', ns).text
        serie = ide.find('nfe:serie', ns).text
        data_emissao = ide.find('nfe:dhEmi', ns).text.split('T')[0]
        
        # Informações do emitente/destinatário
        emit = root.find('.//nfe:emit', ns)
        fornecedor_cnpj = emit.find('nfe:CNPJ', ns).text if emit.find('nfe:CNPJ', ns) is not None else None
        fornecedor_nome = emit.find('nfe:xNome', ns).text if emit.find('nfe:xNome', ns) is not None else None
        
        # Total da nota
        total = root.find('.//nfe:total/nfe:ICMSTot', ns)
        valor_total = Decimal(total.find('nfe:vNF', ns).text)
        
        # Extrai itens
        itens = []
        for det in root.findall('.//nfe:det', ns):
            prod = det.find('nfe:prod', ns)
            
            item = {
                'codigo_produto': prod.find('nfe:cProd', ns).text,
                'nome_produto': prod.find('nfe:xProd', ns).text,
                'ncm': prod.find('nfe:NCM', ns).text if prod.find('nfe:NCM', ns) is not None else None,
                'cfop': prod.find('nfe:CFOP', ns).text if prod.find('nfe:CFOP', ns) is not None else None,
                'unidade_medida': prod.find('nfe:uCom', ns).text,
                'quantidade': Decimal(prod.find('nfe:qCom', ns).text),
                'valor_unitario': Decimal(prod.find('nfe:vUnCom', ns).text),
                'valor_total': Decimal(prod.find('nfe:vProd', ns).text)
            }
            itens.append(item)
        
        return {
            'chave_acesso': chave_acesso,
            'numero_nota': numero_nota,
            'serie': serie,
            'data_emissao': data_emissao,
            'fornecedor_cnpj': fornecedor_cnpj,
            'fornecedor_nome': fornecedor_nome,
            'valor_total': valor_total,
            'itens': itens
        }
        
    except Exception as e:
        raise Exception(f'Erro ao processar XML: {str(e)}')


@app.route('/api/importacao/xml-nfe', methods=['POST'])
def importar_xml_nfe():
    """
    Importa um XML de NF-e e processa automaticamente:
    - Cadastra a nota fiscal
    - Cadastra produtos (se não existirem)
    - Atualiza estoque
    - Recalcula Custo Médio Ponderado
    
    Form-data:
    - arquivo: arquivo XML
    - id_cliente: ID do cliente
    - tipo_nota: ENTRADA ou SAIDA
    """
    if 'arquivo' not in request.files:
        return jsonify({'erro': 'Arquivo XML não fornecido'}), 400
    
    arquivo = request.files['arquivo']
    id_cliente = request.form.get('id_cliente')
    tipo_nota = request.form.get('tipo_nota', 'ENTRADA')
    
    if not id_cliente:
        return jsonify({'erro': 'id_cliente é obrigatório'}), 400
    
    if tipo_nota not in ['ENTRADA', 'SAIDA']:
        return jsonify({'erro': 'tipo_nota deve ser ENTRADA ou SAIDA'}), 400
    
    # Lê o conteúdo do XML
    xml_content = arquivo.read().decode('utf-8')
    
    try:
        dados_nfe = extrair_dados_nfe_xml(xml_content)
    except Exception as e:
        return jsonify({'erro': str(e)}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        # Verifica se a nota já foi importada
        cursor.execute("""
            SELECT id_nota_fiscal FROM notas_fiscais WHERE chave_acesso = %s
        """, (dados_nfe['chave_acesso'],))
        
        if cursor.fetchone():
            return jsonify({'erro': 'Nota fiscal já importada anteriormente'}), 409
        
        # Insere a nota fiscal
        cursor.execute("""
            INSERT INTO notas_fiscais (
                id_cliente, chave_acesso, numero_nota, serie, tipo_nota,
                fornecedor_cliente_cnpj, fornecedor_cliente_nome, valor_total,
                data_emissao, arquivo_xml, status_processamento
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'PROCESSADO')
            RETURNING id_nota_fiscal
        """, (
            id_cliente, dados_nfe['chave_acesso'], dados_nfe['numero_nota'],
            dados_nfe['serie'], tipo_nota, dados_nfe['fornecedor_cnpj'],
            dados_nfe['fornecedor_nome'], dados_nfe['valor_total'],
            dados_nfe['data_emissao'], xml_content
        ))
        
        id_nota_fiscal = cursor.fetchone()['id_nota_fiscal']
        
        produtos_processados = []
        
        # Processa cada item da nota
        for item in dados_nfe['itens']:
            # Verifica se o produto já existe
            cursor.execute("""
                SELECT id_produto, saldo_estoque, custo_medio_ponderado
                FROM produtos
                WHERE id_cliente = %s AND codigo_produto = %s
            """, (id_cliente, item['codigo_produto']))
            
            produto = cursor.fetchone()
            
            if not produto:
                # Cadastra novo produto
                cursor.execute("""
                    INSERT INTO produtos (
                        id_cliente, codigo_produto, nome_produto, unidade_medida,
                        custo_medio_ponderado, saldo_estoque
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id_produto
                """, (
                    id_cliente, item['codigo_produto'], item['nome_produto'],
                    item['unidade_medida'], item['valor_unitario'], 0
                ))
                
                id_produto = cursor.fetchone()['id_produto']
                saldo_anterior = Decimal('0')
                custo_anterior = Decimal('0')
            else:
                id_produto = produto['id_produto']
                saldo_anterior = produto['saldo_estoque']
                custo_anterior = produto['custo_medio_ponderado']
            
            # Insere o item da nota
            cursor.execute("""
                INSERT INTO itens_nota_fiscal (
                    id_nota_fiscal, id_produto, codigo_produto, nome_produto,
                    quantidade, valor_unitario, valor_total, ncm, cfop
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                id_nota_fiscal, id_produto, item['codigo_produto'], item['nome_produto'],
                item['quantidade'], item['valor_unitario'], item['valor_total'],
                item['ncm'], item['cfop']
            ))
            
            # Calcula novo custo médio e saldo
            if tipo_nota == 'ENTRADA':
                novo_custo_medio = calcular_custo_medio_ponderado(
                    saldo_anterior, custo_anterior,
                    item['quantidade'], item['valor_unitario']
                )
                novo_saldo = saldo_anterior + item['quantidade']
                tipo_movimentacao = 'ENTRADA'
            else:  # SAIDA
                novo_custo_medio = custo_anterior
                novo_saldo = saldo_anterior - item['quantidade']
                tipo_movimentacao = 'SAIDA'
            
            # Registra movimentação de estoque
            cursor.execute("""
                INSERT INTO movimentacoes_estoque (
                    id_produto, tipo_movimentacao, quantidade, valor_unitario, valor_total,
                    custo_medio_anterior, custo_medio_novo, saldo_anterior, saldo_novo,
                    origem, id_documento
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'XML_NFE', %s)
            """, (
                id_produto, tipo_movimentacao, item['quantidade'], item['valor_unitario'],
                item['valor_total'], custo_anterior, novo_custo_medio,
                saldo_anterior, novo_saldo, id_nota_fiscal
            ))
            
            # Atualiza o produto
            cursor.execute("""
                UPDATE produtos
                SET saldo_estoque = %s,
                    custo_medio_ponderado = %s,
                    data_atualizacao = NOW()
                WHERE id_produto = %s
            """, (novo_saldo, novo_custo_medio, id_produto))
            
            produtos_processados.append({
                'codigo': item['codigo_produto'],
                'nome': item['nome_produto'],
                'quantidade': float(item['quantidade']),
                'saldo_novo': float(novo_saldo),
                'custo_medio_novo': float(novo_custo_medio)
            })
        
        conn.commit()
        
        return jsonify({
            'sucesso': True,
            'mensagem': 'NF-e importada com sucesso',
            'id_nota_fiscal': id_nota_fiscal,
            'chave_acesso': dados_nfe['chave_acesso'],
            'numero_nota': dados_nfe['numero_nota'],
            'total_itens': len(produtos_processados),
            'produtos_processados': produtos_processados
        }), 201
        
    except Exception as e:
        conn.rollback()
        return jsonify({'erro': f'Erro ao importar NF-e: {str(e)}'}), 500
        
    finally:
        cursor.close()
        conn.close()


@app.route('/api/importacao/planilha-estoque', methods=['POST'])
def importar_planilha_estoque():
    """
    Importa planilha de estoque (Excel/CSV) e atualiza saldos
    
    Form-data:
    - arquivo: arquivo Excel ou CSV
    - id_cliente: ID do cliente
    
    Formato esperado da planilha:
    | codigo_produto | nome_produto | quantidade | custo_unitario |
    """
    if 'arquivo' not in request.files:
        return jsonify({'erro': 'Arquivo não fornecido'}), 400
    
    arquivo = request.files['arquivo']
    id_cliente = request.form.get('id_cliente')
    
    if not id_cliente:
        return jsonify({'erro': 'id_cliente é obrigatório'}), 400
    
    # Determina o tipo de arquivo
    filename = arquivo.filename.lower()
    
    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(arquivo)
        elif filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(arquivo)
        else:
            return jsonify({'erro': 'Formato de arquivo não suportado. Use CSV ou Excel'}), 400
        
        # Valida colunas obrigatórias
        colunas_obrigatorias = ['codigo_produto', 'nome_produto', 'quantidade', 'custo_unitario']
        colunas_faltantes = [col for col in colunas_obrigatorias if col not in df.columns]
        
        if colunas_faltantes:
            return jsonify({
                'erro': f'Colunas obrigatórias faltantes: {", ".join(colunas_faltantes)}'
            }), 400
        
    except Exception as e:
        return jsonify({'erro': f'Erro ao ler arquivo: {str(e)}'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    produtos_processados = []
    erros = []
    
    try:
        for index, row in df.iterrows():
            try:
                codigo = str(row['codigo_produto']).strip()
                nome = str(row['nome_produto']).strip()
                quantidade = Decimal(str(row['quantidade']))
                custo = Decimal(str(row['custo_unitario']))
                
                # Busca produto existente
                cursor.execute("""
                    SELECT id_produto, saldo_estoque, custo_medio_ponderado
                    FROM produtos
                    WHERE id_cliente = %s AND codigo_produto = %s
                """, (id_cliente, codigo))
                
                produto = cursor.fetchone()
                
                if not produto:
                    # Cadastra novo produto
                    cursor.execute("""
                        INSERT INTO produtos (
                            id_cliente, codigo_produto, nome_produto,
                            custo_medio_ponderado, saldo_estoque
                        ) VALUES (%s, %s, %s, %s, %s)
                        RETURNING id_produto
                    """, (id_cliente, codigo, nome, custo, quantidade))
                    
                    id_produto = cursor.fetchone()['id_produto']
                    saldo_anterior = Decimal('0')
                    custo_anterior = Decimal('0')
                else:
                    id_produto = produto['id_produto']
                    saldo_anterior = produto['saldo_estoque']
                    custo_anterior = produto['custo_medio_ponderado']
                
                # Calcula novo custo médio
                novo_custo_medio = calcular_custo_medio_ponderado(
                    saldo_anterior, custo_anterior, quantidade, custo
                )
                novo_saldo = saldo_anterior + quantidade
                
                # Registra movimentação
                cursor.execute("""
                    INSERT INTO movimentacoes_estoque (
                        id_produto, tipo_movimentacao, quantidade, valor_unitario,
                        valor_total, custo_medio_anterior, custo_medio_novo,
                        saldo_anterior, saldo_novo, origem
                    ) VALUES (%s, 'ENTRADA', %s, %s, %s, %s, %s, %s, %s, 'PLANILHA')
                """, (
                    id_produto, quantidade, custo, quantidade * custo,
                    custo_anterior, novo_custo_medio, saldo_anterior, novo_saldo
                ))
                
                # Atualiza produto
                cursor.execute("""
                    UPDATE produtos
                    SET saldo_estoque = %s,
                        custo_medio_ponderado = %s,
                        data_atualizacao = NOW()
                    WHERE id_produto = %s
                """, (novo_saldo, novo_custo_medio, id_produto))
                
                produtos_processados.append({
                    'linha': index + 2,
                    'codigo': codigo,
                    'nome': nome,
                    'quantidade': float(quantidade),
                    'saldo_novo': float(novo_saldo),
                    'custo_medio_novo': float(novo_custo_medio)
                })
                
            except Exception as e:
                erros.append({
                    'linha': index + 2,
                    'erro': str(e)
                })
        
        if erros:
            conn.rollback()
            return jsonify({
                'sucesso': False,
                'mensagem': 'Erros encontrados durante importação',
                'erros': erros
            }), 400
        
        conn.commit()
        
        return jsonify({
            'sucesso': True,
            'mensagem': 'Planilha importada com sucesso',
            'total_produtos': len(produtos_processados),
            'produtos_processados': produtos_processados
        }), 201
        
    except Exception as e:
        conn.rollback()
        return jsonify({'erro': f'Erro ao importar planilha: {str(e)}'}), 500
        
    finally:
        cursor.close()
        conn.close()


@app.route('/api/importacao/status-nota/<chave_acesso>', methods=['GET'])
def consultar_status_nota(chave_acesso):
    """Consulta o status de processamento de uma nota fiscal"""
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    try:
        cursor.execute("""
            SELECT nf.*, 
                   COUNT(inf.id_item_nota) as total_itens
            FROM notas_fiscais nf
            LEFT JOIN itens_nota_fiscal inf ON nf.id_nota_fiscal = inf.id_nota_fiscal
            WHERE nf.chave_acesso = %s
            GROUP BY nf.id_nota_fiscal
        """, (chave_acesso,))
        
        nota = cursor.fetchone()
        
        if not nota:
            return jsonify({'erro': 'Nota fiscal não encontrada'}), 404
        
        return jsonify({
            'sucesso': True,
            'nota': nota
        }), 200
        
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
