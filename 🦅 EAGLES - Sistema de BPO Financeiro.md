# 🦅 EAGLES - Sistema de BPO Financeiro

## Visão Geral

**Eagles** é um sistema modular de BPO Financeiro desenvolvido com a filosofia de "Visão de Águia" - precisão, amplitude e decisão. O sistema oferece uma plataforma integrada para contadores, gerentes e proprietários de empresas, permitindo gestão financeira completa, controle operacional e tomada de decisões estratégicas baseadas em dados.

## Filosofia e Identidade

- **Nome**: Eagles (Águias)
- **Conceito**: Visão de águia - enxergar o todo com precisão e tomar decisões assertivas
- **Design**: Dark Mode minimalista, linhas afiadas, foco na clareza
- **Cores**:
  - 🟢 Verde (#10B981): Positivo, saudável, aprovado
  - 🔴 Vermelho (#EF4444): Alerta, crítico, atenção urgente
  - 🟡 Amarelo (#F59E0B): Atenção, monitoramento necessário

## Arquitetura Técnica

### Stack Tecnológica

**Backend**:
- Python 3.11+ (Flask/FastAPI)
- PostgreSQL (banco de dados principal)
- APIs RESTful

**Frontend**:
- PWA (Progressive Web App)
- React/Vue.js para web
- React Native para mobile (iOS/Android)
- HTML5/CSS3/JavaScript

**Bibliotecas Python**:
- `pandas`: Processamento de planilhas e dados
- `xml.etree.ElementTree`: Parsing de XML (NF-e)
- `psycopg2`: Conexão com PostgreSQL
- `qrcode`: Geração de QR Codes
- `flask`: Framework web

### Estrutura do Projeto

```
eagles_project/
├── database_schema.sql              # Estrutura completa do banco de dados
├── api_autenticacao.py              # API de autenticação por QR Code
├── api_importacao.py                # API de importação de XML/Planilhas
├── api_presenca.py                  # API de gestão de presença e faltas
├── api_lente_contador.py            # API da Lente do Contador
├── wireframe_ui_gerente.md          # Wireframe da UI mobile do Gerente
├── wireframe_ui_dono.md             # Wireframe da UI mobile do Dono
└── README.md                        # Este arquivo
```

## Módulos do Sistema

### 1. Módulo Contador Master (Desktop)

**Usuário**: Samuel (Contador)
**Plataforma**: Desktop/Web

**Funcionalidades**:
- Dashboard central com visão de todos os clientes
- Semáforo de Saúde Patrimonial personalizável por CNAE
- Importação inteligente de XML (NF-e), planilhas de estoque e balancetes
- **Lente do Contador**: Ferramenta para destacar contas específicas com observações contextualizadas
- Ferramentas de auditoria e log de alterações
- Dashboard de "Saúde dos Dados" (monitoramento de desempenho do Gerente)
- Aprovação de alertas críticos antes de serem visíveis para o Dono
- Geração de QR Codes para autenticação de Gerentes e Donos

### 2. Módulo Super Gerente (Mobile)

**Usuário**: Gerente operacional
**Plataforma**: Mobile (iOS/Android)

**Funcionalidades**:
- Autenticação por QR Code
- Dashboard operacional com escala do dia
- Gestão simplificada de pessoas:
  - Check-in de presença
  - Registro de faltas (justificadas/injustificadas)
  - Visualização de escala de trabalho
- Registro de fechamento de caixa "cego"
- Captura de comprovantes de despesa via câmera

### 3. Módulo Dono (Mobile)

**Usuário**: Proprietário da empresa
**Plataforma**: Mobile (iOS/Android)

**Funcionalidades**:
- Autenticação por QR Code
- Dashboard estratégico "Voo da Águia":
  - Semáforo de Saúde Patrimonial
  - Lucro Real (Competência vs Caixa)
  - Ponto de Equilíbrio
  - Margem de Contribuição
- **Lente do Contador**: Visualização de contas destacadas com observações
- Alertas contextuais validados pelo contador
- Health Check do desempenho do Gerente
- Mensagens diretas com o Contador

## Banco de Dados

### Principais Tabelas

#### Autenticação e Usuários
- `usuarios`: Cadastro de contadores, gerentes e donos
- `qr_codes`: Tokens de QR Code para autenticação
- `sessoes`: Sessões ativas de usuários

#### Clientes e Configuração
- `clientes`: Empresas gerenciadas
- `usuario_cliente`: Relacionamento usuário-cliente
- `configuracao_cnae`: Metas e fórmulas personalizadas por CNAE

#### Produtos e Estoque
- `produtos`: Cadastro de produtos
- `movimentacoes_estoque`: Histórico de movimentações
- `notas_fiscais`: NF-e importadas
- `itens_nota_fiscal`: Itens das notas

#### Contabilidade
- `plano_contas`: Plano de contas contábil
- `balancetes`: Balancetes importados
- `lancamentos_balancete`: Lançamentos contábeis
- `lente_contador`: Observações do contador sobre contas específicas

#### Gestão de Pessoas
- `funcionarios`: Cadastro de funcionários
- `escalas_trabalho`: Escalas de trabalho
- `registros_presenca`: Check-in, faltas e atrasos

#### Operações Financeiras
- `fechamentos_caixa`: Fechamentos de caixa
- `despesas`: Despesas com comprovantes
- `indicadores_financeiros`: Cache de métricas calculadas

#### Comunicação e Auditoria
- `alertas`: Alertas e notificações
- `mensagens`: Mensagens entre usuários
- `log_auditoria`: Log de todas as alterações
- `saude_dados`: Monitoramento de qualidade dos dados

## APIs Principais

### 1. API de Autenticação

**Base URL**: `http://localhost:5000/api/auth`

#### Endpoints:

**POST /gerar-qrcode**
- Gera QR Code para autenticação (apenas Contador)
- Body: `{ "id_usuario": 123, "tipo_acesso": "GERENTE", "validade_horas": 24 }`
- Retorna: QR Code em base64 e token

**POST /validar-qrcode**
- Valida QR Code e cria sessão
- Body: `{ "token": "...", "dispositivo": "iPhone 13" }`
- Retorna: Token de sessão

**POST /logout**
- Encerra sessão atual
- Header: `Authorization: Bearer {token}`

**GET /validar-sessao**
- Valida se sessão está ativa
- Header: `Authorization: Bearer {token}`

### 2. API de Importação

**Base URL**: `http://localhost:5001/api/importacao`

#### Endpoints:

**POST /xml-nfe**
- Importa XML de NF-e e processa automaticamente
- Form-data: `arquivo` (XML), `id_cliente`, `tipo_nota` (ENTRADA/SAIDA)
- Processa: cadastro de produtos, atualização de estoque, cálculo de CMP

**POST /planilha-estoque**
- Importa planilha de estoque (Excel/CSV)
- Form-data: `arquivo`, `id_cliente`
- Formato esperado: `codigo_produto | nome_produto | quantidade | custo_unitario`

**GET /status-nota/{chave_acesso}**
- Consulta status de processamento de uma NF-e

### 3. API de Presença

**Base URL**: `http://localhost:5002/api/presenca`

#### Endpoints:

**GET /escala-dia**
- Obtém escala de trabalho do dia
- Query: `id_cliente`, `data` (opcional)
- Retorna: Funcionários organizados por turno com status

**POST /registrar-checkin**
- Registra check-in de funcionário (apenas Gerente)
- Body: `{ "id_funcionario": 123, "hora_checkin": "08:30" }`
- Calcula automaticamente se é atraso (tolerância de 15min)

**POST /registrar-falta**
- Registra falta de funcionário (apenas Gerente)
- Body: `{ "id_funcionario": 123, "tipo_justificativa": "JUSTIFICADA", "motivo": "..." }`

**GET /resumo-mensal**
- Obtém resumo mensal de presença/faltas
- Query: `id_cliente`, `mes`, `ano`

**POST /criar-escala**
- Cria escala de trabalho (apenas Contador)
- Body: `{ "id_funcionario": 123, "data_escala": "2025-01-15", "turno": "MANHA", ... }`

### 4. API da Lente do Contador

**Base URL**: `http://localhost:5003/api/lente`

#### Endpoints:

**POST /adicionar-observacao**
- Adiciona observação a uma conta do balancete (apenas Contador)
- Body: `{ "id_lancamento": 123, "observacao_consultoria": "...", "destacado": true }`

**PUT /editar-observacao/{id_lente}**
- Edita observação existente (apenas Contador criador)
- Body: `{ "observacao_consultoria": "...", "destacado": false }`

**DELETE /remover-observacao/{id_lente}**
- Remove observação (apenas Contador criador)

**GET /listar-observacoes**
- Lista observações de um balancete
- Query: `id_cliente`, `mes`, `ano`, `apenas_destacadas` (opcional)

**GET /balancete-com-observacoes**
- Obtém balancete completo com observações destacadas (usado pelo Dono)
- Query: `id_cliente`, `mes`, `ano`

**GET /estatisticas**
- Estatísticas de uso da Lente (apenas Contador)
- Query: `id_cliente` (opcional), `mes` (opcional), `ano` (opcional)

## Funcionalidades Especiais

### 1. Custo Médio Ponderado (CMP)

O sistema calcula automaticamente o CMP a cada entrada de produto:

```
CMP = (Saldo_Anterior × Custo_Anterior + Quantidade_Entrada × Custo_Entrada) / (Saldo_Anterior + Quantidade_Entrada)
```

### 2. Lente do Contador

Ferramenta exclusiva que permite ao contador:
- Selecionar contas específicas do balancete
- Adicionar observações contextualizadas para o Dono
- Destacar pontos de atenção ou oportunidades
- Aprovar antes de tornar visível

### 3. Semáforo de Saúde Patrimonial

Indicador visual personalizável por CNAE:
- 🟢 **Verde**: Empresa saudável (metas atingidas)
- 🟡 **Amarelo**: Atenção necessária (próximo das metas)
- 🔴 **Vermelho**: Alerta crítico (abaixo das metas)

### 4. Autenticação por QR Code

Sistema seguro de autenticação:
- Contador gera QR Code no painel desktop
- Gerente/Dono escaneia com o celular
- Token único com validade configurável
- QR Code desativado após primeiro uso

### 5. Configuração por CNAE

Adaptação automática de fórmulas e dashboards:
- **Comércio**: CMV (Custo de Mercadoria Vendida)
- **Serviços**: CPV (Custo de Prestação de Serviços)
- **Construtora**: Centros de custo
- Metas personalizadas por tipo de negócio

## Regras de Negócio

1. **Pro-labore Fixo**: R$ 100,00 como despesa fixa padrão
2. **Tolerância de Atraso**: 15 minutos após horário de entrada
3. **Fechamento de Caixa "Cego"**: Gerente informa valor sem ver expectativa
4. **Aprovação de Alertas**: Contador valida antes de enviar ao Dono
5. **Regime Tributário**: Suporte para Simples Nacional, Lucro Presumido e Lucro Real
6. **Auditoria Completa**: Log de todas as alterações com usuário, data e IP

## Instalação e Configuração

### Pré-requisitos

- Python 3.11+
- PostgreSQL 12+
- Node.js 16+ (para frontend)

### Configuração do Banco de Dados

```bash
# Criar banco de dados
createdb eagles_db

# Executar schema
psql -U eagles_user -d eagles_db -f database_schema.sql
```

### Configuração das APIs

```bash
# Instalar dependências Python
pip install flask psycopg2 pandas qrcode pillow

# Configurar variáveis de ambiente
export DB_HOST=localhost
export DB_NAME=eagles_db
export DB_USER=eagles_user
export DB_PASSWORD=eagles_password

# Executar APIs (em terminais separados)
python api_autenticacao.py      # Porta 5000
python api_importacao.py        # Porta 5001
python api_presenca.py          # Porta 5002
python api_lente_contador.py   # Porta 5003
```

## Roadmap Futuro

- [ ] Integração com APIs bancárias (Open Banking)
- [ ] Relatórios em PDF automatizados
- [ ] Dashboard de BI com gráficos interativos
- [ ] Integração com sistemas de folha de pagamento
- [ ] App mobile nativo (React Native)
- [ ] Módulo de previsão financeira com ML
- [ ] Integração com e-commerce
- [ ] Módulo de conciliação bancária automática

## Suporte e Documentação

Para mais informações sobre os wireframes das interfaces mobile:
- [Wireframe UI Gerente](wireframe_ui_gerente.md)
- [Wireframe UI Dono](wireframe_ui_dono.md)

## Licença

Projeto proprietário - Eagles BPO Financeiro © 2025

---

**Desenvolvido com 🦅 Visão de Águia**
