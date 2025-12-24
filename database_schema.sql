-- =====================================================
-- EAGLES - Sistema de BPO Financeiro
-- Estrutura Completa do Banco de Dados SQL
-- =====================================================

-- =====================================================
-- TABELAS DE CONFIGURAÇÃO E AUTENTICAÇÃO
-- =====================================================

-- Tabela de Usuários (Contador, Gerente, Dono)
CREATE TABLE usuarios (
    id_usuario SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    tipo_usuario VARCHAR(20) NOT NULL CHECK (tipo_usuario IN ('CONTADOR', 'GERENTE', 'DONO')),
    senha_hash VARCHAR(255) NOT NULL,
    ativo BOOLEAN DEFAULT TRUE,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de QR Codes para autenticação
CREATE TABLE qr_codes (
    id_qr_code SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    token VARCHAR(255) UNIQUE NOT NULL,
    tipo_acesso VARCHAR(20) NOT NULL CHECK (tipo_acesso IN ('GERENTE', 'DONO')),
    data_geracao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_expiracao TIMESTAMP,
    ativo BOOLEAN DEFAULT TRUE
);

-- Tabela de Sessões de Autenticação
CREATE TABLE sessoes (
    id_sessao SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    token_sessao VARCHAR(255) UNIQUE NOT NULL,
    data_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_expiracao TIMESTAMP NOT NULL,
    dispositivo VARCHAR(255),
    ip_address VARCHAR(45)
);

-- =====================================================
-- TABELAS DE CLIENTES E EMPRESAS
-- =====================================================

-- Tabela de Clientes (Empresas gerenciadas)
CREATE TABLE clientes (
    id_cliente SERIAL PRIMARY KEY,
    razao_social VARCHAR(255) NOT NULL,
    nome_fantasia VARCHAR(255),
    cnpj VARCHAR(18) UNIQUE NOT NULL,
    cnae VARCHAR(10) NOT NULL,
    tipo_negocio VARCHAR(50) NOT NULL CHECK (tipo_negocio IN ('COMERCIO', 'SERVICO', 'INDUSTRIA', 'CONSTRUTORA', 'OUTRO')),
    regime_tributario VARCHAR(50) NOT NULL CHECK (regime_tributario IN ('SIMPLES_NACIONAL', 'LUCRO_PRESUMIDO', 'LUCRO_REAL')),
    prolabore_fixo DECIMAL(15, 2) DEFAULT 100.00,
    ativo BOOLEAN DEFAULT TRUE,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Relacionamento Usuário-Cliente (Contador, Gerente, Dono vinculados a clientes)
CREATE TABLE usuario_cliente (
    id_usuario_cliente SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    id_cliente INTEGER NOT NULL REFERENCES clientes(id_cliente) ON DELETE CASCADE,
    papel VARCHAR(20) NOT NULL CHECK (papel IN ('CONTADOR', 'GERENTE', 'DONO')),
    data_vinculo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(id_usuario, id_cliente, papel)
);

-- =====================================================
-- TABELAS DE CONFIGURAÇÃO POR CNAE
-- =====================================================

-- Tabela de Configurações de CNAE (Metas e Fórmulas personalizadas)
CREATE TABLE configuracao_cnae (
    id_configuracao SERIAL PRIMARY KEY,
    id_cliente INTEGER NOT NULL REFERENCES clientes(id_cliente) ON DELETE CASCADE,
    cnae VARCHAR(10) NOT NULL,
    meta_lucro_minimo DECIMAL(15, 2),
    meta_margem_contribuicao DECIMAL(5, 2),
    meta_ponto_equilibrio DECIMAL(15, 2),
    semaforo_verde_threshold DECIMAL(5, 2),
    semaforo_amarelo_threshold DECIMAL(5, 2),
    usa_cmv BOOLEAN DEFAULT TRUE,
    usa_cpv BOOLEAN DEFAULT FALSE,
    usa_centro_custo BOOLEAN DEFAULT FALSE,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(id_cliente, cnae)
);

-- =====================================================
-- TABELAS DE PRODUTOS E ESTOQUE
-- =====================================================

-- Tabela de Produtos
CREATE TABLE produtos (
    id_produto SERIAL PRIMARY KEY,
    id_cliente INTEGER NOT NULL REFERENCES clientes(id_cliente) ON DELETE CASCADE,
    codigo_produto VARCHAR(100),
    nome_produto VARCHAR(255) NOT NULL,
    descricao TEXT,
    unidade_medida VARCHAR(10),
    custo_medio_ponderado DECIMAL(15, 4) DEFAULT 0.00,
    saldo_estoque DECIMAL(15, 4) DEFAULT 0.00,
    ativo BOOLEAN DEFAULT TRUE,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(id_cliente, codigo_produto)
);

-- Tabela de Movimentações de Estoque
CREATE TABLE movimentacoes_estoque (
    id_movimentacao SERIAL PRIMARY KEY,
    id_produto INTEGER NOT NULL REFERENCES produtos(id_produto) ON DELETE CASCADE,
    tipo_movimentacao VARCHAR(20) NOT NULL CHECK (tipo_movimentacao IN ('ENTRADA', 'SAIDA', 'AJUSTE')),
    quantidade DECIMAL(15, 4) NOT NULL,
    valor_unitario DECIMAL(15, 4),
    valor_total DECIMAL(15, 2),
    custo_medio_anterior DECIMAL(15, 4),
    custo_medio_novo DECIMAL(15, 4),
    saldo_anterior DECIMAL(15, 4),
    saldo_novo DECIMAL(15, 4),
    origem VARCHAR(50) CHECK (origem IN ('XML_NFE', 'PLANILHA', 'MANUAL', 'AJUSTE')),
    id_documento INTEGER,
    data_movimentacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    observacao TEXT
);

-- =====================================================
-- TABELAS DE DOCUMENTOS FISCAIS
-- =====================================================

-- Tabela de Notas Fiscais (NF-e)
CREATE TABLE notas_fiscais (
    id_nota_fiscal SERIAL PRIMARY KEY,
    id_cliente INTEGER NOT NULL REFERENCES clientes(id_cliente) ON DELETE CASCADE,
    chave_acesso VARCHAR(44) UNIQUE NOT NULL,
    numero_nota VARCHAR(20) NOT NULL,
    serie VARCHAR(10),
    tipo_nota VARCHAR(20) CHECK (tipo_nota IN ('ENTRADA', 'SAIDA')),
    fornecedor_cliente_cnpj VARCHAR(18),
    fornecedor_cliente_nome VARCHAR(255),
    valor_total DECIMAL(15, 2),
    data_emissao DATE,
    data_importacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    arquivo_xml TEXT,
    status_processamento VARCHAR(20) DEFAULT 'PENDENTE' CHECK (status_processamento IN ('PENDENTE', 'PROCESSADO', 'ERRO')),
    observacao TEXT
);

-- Tabela de Itens de Notas Fiscais
CREATE TABLE itens_nota_fiscal (
    id_item_nota SERIAL PRIMARY KEY,
    id_nota_fiscal INTEGER NOT NULL REFERENCES notas_fiscais(id_nota_fiscal) ON DELETE CASCADE,
    id_produto INTEGER REFERENCES produtos(id_produto) ON DELETE SET NULL,
    codigo_produto VARCHAR(100),
    nome_produto VARCHAR(255) NOT NULL,
    quantidade DECIMAL(15, 4) NOT NULL,
    valor_unitario DECIMAL(15, 4) NOT NULL,
    valor_total DECIMAL(15, 2) NOT NULL,
    ncm VARCHAR(10),
    cfop VARCHAR(10),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- TABELAS DE CONTABILIDADE
-- =====================================================

-- Tabela de Plano de Contas
CREATE TABLE plano_contas (
    id_conta SERIAL PRIMARY KEY,
    id_cliente INTEGER NOT NULL REFERENCES clientes(id_cliente) ON DELETE CASCADE,
    codigo_conta VARCHAR(50) NOT NULL,
    nome_conta VARCHAR(255) NOT NULL,
    tipo_conta VARCHAR(20) NOT NULL CHECK (tipo_conta IN ('ATIVO', 'PASSIVO', 'RECEITA', 'DESPESA', 'PATRIMONIO_LIQUIDO')),
    natureza VARCHAR(20) NOT NULL CHECK (natureza IN ('DEVEDORA', 'CREDORA')),
    nivel INTEGER NOT NULL,
    conta_pai INTEGER REFERENCES plano_contas(id_conta) ON DELETE SET NULL,
    aceita_lancamento BOOLEAN DEFAULT TRUE,
    ativo BOOLEAN DEFAULT TRUE,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(id_cliente, codigo_conta)
);

-- Tabela de Balancetes Importados
CREATE TABLE balancetes (
    id_balancete SERIAL PRIMARY KEY,
    id_cliente INTEGER NOT NULL REFERENCES clientes(id_cliente) ON DELETE CASCADE,
    mes_referencia INTEGER NOT NULL CHECK (mes_referencia BETWEEN 1 AND 12),
    ano_referencia INTEGER NOT NULL,
    data_importacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    arquivo_origem VARCHAR(255),
    status_processamento VARCHAR(20) DEFAULT 'PENDENTE' CHECK (status_processamento IN ('PENDENTE', 'PROCESSADO', 'ERRO')),
    observacao TEXT,
    UNIQUE(id_cliente, mes_referencia, ano_referencia)
);

-- Tabela de Lançamentos do Balancete
CREATE TABLE lancamentos_balancete (
    id_lancamento SERIAL PRIMARY KEY,
    id_balancete INTEGER NOT NULL REFERENCES balancetes(id_balancete) ON DELETE CASCADE,
    id_conta INTEGER REFERENCES plano_contas(id_conta) ON DELETE SET NULL,
    codigo_conta VARCHAR(50) NOT NULL,
    nome_conta VARCHAR(255) NOT NULL,
    saldo_anterior DECIMAL(15, 2),
    debito DECIMAL(15, 2),
    credito DECIMAL(15, 2),
    saldo_atual DECIMAL(15, 2),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Lente do Contador (Observações sobre contas específicas)
CREATE TABLE lente_contador (
    id_lente SERIAL PRIMARY KEY,
    id_lancamento INTEGER NOT NULL REFERENCES lancamentos_balancete(id_lancamento) ON DELETE CASCADE,
    id_contador INTEGER NOT NULL REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    observacao_consultoria TEXT NOT NULL,
    destacado BOOLEAN DEFAULT TRUE,
    aprovado BOOLEAN DEFAULT FALSE,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_aprovacao TIMESTAMP
);

-- =====================================================
-- TABELAS DE GESTÃO DE PESSOAS
-- =====================================================

-- Tabela de Funcionários
CREATE TABLE funcionarios (
    id_funcionario SERIAL PRIMARY KEY,
    id_cliente INTEGER NOT NULL REFERENCES clientes(id_cliente) ON DELETE CASCADE,
    nome_completo VARCHAR(255) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    cargo VARCHAR(100),
    data_admissao DATE,
    data_demissao DATE,
    ativo BOOLEAN DEFAULT TRUE,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Escalas de Trabalho
CREATE TABLE escalas_trabalho (
    id_escala SERIAL PRIMARY KEY,
    id_funcionario INTEGER NOT NULL REFERENCES funcionarios(id_funcionario) ON DELETE CASCADE,
    data_escala DATE NOT NULL,
    turno VARCHAR(20) CHECK (turno IN ('MANHA', 'TARDE', 'NOITE', 'INTEGRAL')),
    hora_inicio TIME,
    hora_fim TIME,
    observacao TEXT,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(id_funcionario, data_escala, turno)
);

-- Tabela de Registro de Presença
CREATE TABLE registros_presenca (
    id_registro SERIAL PRIMARY KEY,
    id_funcionario INTEGER NOT NULL REFERENCES funcionarios(id_funcionario) ON DELETE CASCADE,
    data_registro DATE NOT NULL,
    status_presenca VARCHAR(20) NOT NULL CHECK (status_presenca IN ('PRESENTE', 'FALTA', 'ATRASO')),
    tipo_justificativa VARCHAR(30) CHECK (tipo_justificativa IN ('JUSTIFICADA', 'INJUSTIFICADA', 'NAO_APLICAVEL')),
    motivo TEXT,
    hora_checkin TIME,
    id_gerente INTEGER REFERENCES usuarios(id_usuario) ON DELETE SET NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(id_funcionario, data_registro)
);

-- =====================================================
-- TABELAS DE OPERAÇÕES FINANCEIRAS
-- =====================================================

-- Tabela de Fechamentos de Caixa
CREATE TABLE fechamentos_caixa (
    id_fechamento SERIAL PRIMARY KEY,
    id_cliente INTEGER NOT NULL REFERENCES clientes(id_cliente) ON DELETE CASCADE,
    data_fechamento DATE NOT NULL,
    valor_informado DECIMAL(15, 2) NOT NULL,
    valor_esperado DECIMAL(15, 2),
    diferenca DECIMAL(15, 2),
    tipo_fechamento VARCHAR(20) CHECK (tipo_fechamento IN ('CEGO', 'CONFERIDO')),
    id_gerente INTEGER REFERENCES usuarios(id_usuario) ON DELETE SET NULL,
    observacao TEXT,
    data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(id_cliente, data_fechamento)
);

-- Tabela de Despesas (Comprovantes)
CREATE TABLE despesas (
    id_despesa SERIAL PRIMARY KEY,
    id_cliente INTEGER NOT NULL REFERENCES clientes(id_cliente) ON DELETE CASCADE,
    descricao VARCHAR(255) NOT NULL,
    valor DECIMAL(15, 2) NOT NULL,
    data_despesa DATE NOT NULL,
    categoria VARCHAR(100),
    centro_custo VARCHAR(100),
    comprovante_path VARCHAR(500),
    id_gerente INTEGER REFERENCES usuarios(id_usuario) ON DELETE SET NULL,
    aprovado BOOLEAN DEFAULT FALSE,
    id_contador_aprovador INTEGER REFERENCES usuarios(id_usuario) ON DELETE SET NULL,
    data_aprovacao TIMESTAMP,
    data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- TABELAS DE INDICADORES E DASHBOARDS
-- =====================================================

-- Tabela de Indicadores Calculados (Cache de métricas)
CREATE TABLE indicadores_financeiros (
    id_indicador SERIAL PRIMARY KEY,
    id_cliente INTEGER NOT NULL REFERENCES clientes(id_cliente) ON DELETE CASCADE,
    mes_referencia INTEGER NOT NULL CHECK (mes_referencia BETWEEN 1 AND 12),
    ano_referencia INTEGER NOT NULL,
    receita_total DECIMAL(15, 2),
    custo_total DECIMAL(15, 2),
    despesa_total DECIMAL(15, 2),
    lucro_bruto DECIMAL(15, 2),
    lucro_liquido_competencia DECIMAL(15, 2),
    lucro_liquido_caixa DECIMAL(15, 2),
    margem_contribuicao DECIMAL(5, 2),
    ponto_equilibrio DECIMAL(15, 2),
    semaforo_saude VARCHAR(20) CHECK (semaforo_saude IN ('VERDE', 'AMARELO', 'VERMELHO')),
    data_calculo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(id_cliente, mes_referencia, ano_referencia)
);

-- Tabela de Alertas
CREATE TABLE alertas (
    id_alerta SERIAL PRIMARY KEY,
    id_cliente INTEGER NOT NULL REFERENCES clientes(id_cliente) ON DELETE CASCADE,
    tipo_alerta VARCHAR(50) NOT NULL CHECK (tipo_alerta IN ('FINANCEIRO', 'OPERACIONAL', 'FISCAL', 'HEALTH_CHECK')),
    severidade VARCHAR(20) NOT NULL CHECK (severidade IN ('BAIXA', 'MEDIA', 'ALTA', 'CRITICA')),
    titulo VARCHAR(255) NOT NULL,
    mensagem TEXT NOT NULL,
    destinatario VARCHAR(20) CHECK (destinatario IN ('CONTADOR', 'GERENTE', 'DONO')),
    aprovado_contador BOOLEAN DEFAULT FALSE,
    id_contador_aprovador INTEGER REFERENCES usuarios(id_usuario) ON DELETE SET NULL,
    data_aprovacao TIMESTAMP,
    lido BOOLEAN DEFAULT FALSE,
    data_leitura TIMESTAMP,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- TABELAS DE COMUNICAÇÃO
-- =====================================================

-- Tabela de Mensagens Internas
CREATE TABLE mensagens (
    id_mensagem SERIAL PRIMARY KEY,
    id_cliente INTEGER NOT NULL REFERENCES clientes(id_cliente) ON DELETE CASCADE,
    id_remetente INTEGER NOT NULL REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    id_destinatario INTEGER NOT NULL REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    assunto VARCHAR(255),
    conteudo TEXT NOT NULL,
    contexto VARCHAR(100),
    lida BOOLEAN DEFAULT FALSE,
    data_leitura TIMESTAMP,
    data_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- TABELAS DE AUDITORIA E LOG
-- =====================================================

-- Tabela de Log de Auditoria
CREATE TABLE log_auditoria (
    id_log SERIAL PRIMARY KEY,
    id_usuario INTEGER REFERENCES usuarios(id_usuario) ON DELETE SET NULL,
    id_cliente INTEGER REFERENCES clientes(id_cliente) ON DELETE SET NULL,
    tabela_afetada VARCHAR(100) NOT NULL,
    id_registro_afetado INTEGER,
    tipo_operacao VARCHAR(20) NOT NULL CHECK (tipo_operacao IN ('INSERT', 'UPDATE', 'DELETE')),
    dados_anteriores TEXT,
    dados_novos TEXT,
    ip_address VARCHAR(45),
    data_operacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Saúde dos Dados (Monitoramento de desempenho do Gerente)
CREATE TABLE saude_dados (
    id_saude SERIAL PRIMARY KEY,
    id_cliente INTEGER NOT NULL REFERENCES clientes(id_cliente) ON DELETE CASCADE,
    id_gerente INTEGER REFERENCES usuarios(id_usuario) ON DELETE SET NULL,
    mes_referencia INTEGER NOT NULL CHECK (mes_referencia BETWEEN 1 AND 12),
    ano_referencia INTEGER NOT NULL,
    total_registros_esperados INTEGER,
    total_registros_realizados INTEGER,
    percentual_completude DECIMAL(5, 2),
    atrasos_registrados INTEGER DEFAULT 0,
    faltas_injustificadas INTEGER DEFAULT 0,
    score_qualidade DECIMAL(5, 2),
    data_calculo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(id_cliente, id_gerente, mes_referencia, ano_referencia)
);

-- =====================================================
-- ÍNDICES PARA OTIMIZAÇÃO DE PERFORMANCE
-- =====================================================

CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_usuarios_tipo ON usuarios(tipo_usuario);
CREATE INDEX idx_qr_codes_token ON qr_codes(token);
CREATE INDEX idx_sessoes_token ON sessoes(token_sessao);
CREATE INDEX idx_clientes_cnpj ON clientes(cnpj);
CREATE INDEX idx_produtos_cliente ON produtos(id_cliente);
CREATE INDEX idx_movimentacoes_produto ON movimentacoes_estoque(id_produto);
CREATE INDEX idx_notas_fiscais_cliente ON notas_fiscais(id_cliente);
CREATE INDEX idx_notas_fiscais_chave ON notas_fiscais(chave_acesso);
CREATE INDEX idx_balancetes_cliente ON balancetes(id_cliente);
CREATE INDEX idx_lancamentos_balancete ON lancamentos_balancete(id_balancete);
CREATE INDEX idx_funcionarios_cliente ON funcionarios(id_cliente);
CREATE INDEX idx_registros_presenca_funcionario ON registros_presenca(id_funcionario);
CREATE INDEX idx_despesas_cliente ON despesas(id_cliente);
CREATE INDEX idx_alertas_cliente ON alertas(id_cliente);
CREATE INDEX idx_mensagens_destinatario ON mensagens(id_destinatario);
CREATE INDEX idx_log_auditoria_usuario ON log_auditoria(id_usuario);

-- =====================================================
-- FIM DO SCHEMA
-- =====================================================
