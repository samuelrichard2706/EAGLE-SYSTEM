# EAGLES - Wireframe UI Mobile do Dono

## Identidade Visual Eagles
- **Tema**: Dark Mode (mesma identidade do Gerente)
- **Paleta de Cores**:
  - Background principal: `#0A0E1A`
  - Background secundário: `#151B2D`
  - Texto primário: `#E8EAF0`
  - Texto secundário: `#8B92A8`
  - Verde (Positivo): `#10B981`
  - Vermelho (Alerta): `#EF4444`
  - Amarelo (Atenção): `#F59E0B`
- **Filosofia**: "Voo da Águia" - Visão estratégica, decisões informadas, clareza total

---

## TELA 1: Login por QR Code

```
┌─────────────────────────────────────┐
│  [Status Bar]                       │
├─────────────────────────────────────┤
│                                     │
│         [Logo Eagles]               │
│     🦅 Visão de Águia               │
│                                     │
│  ┌───────────────────────────────┐ │
│  │                               │ │
│  │     [Ícone QR Code]          │ │
│  │                               │ │
│  │  Escaneie o QR Code          │ │
│  │  gerado pelo Contador        │ │
│  │                               │ │
│  └───────────────────────────────┘ │
│                                     │
│  ┌───────────────────────────────┐ │
│  │  [Botão: Escanear QR Code]   │ │
│  │  Background: #10B981          │ │
│  └───────────────────────────────┘ │
│                                     │
│      Acesso Proprietário            │
│                                     │
└─────────────────────────────────────┘
```

**Comportamento**: Idêntico ao Gerente, mas com perfil "DONO"

---

## TELA 2: Dashboard Estratégico "Voo da Águia"

```
┌─────────────────────────────────────┐
│  [Status Bar]                       │
├─────────────────────────────────────┤
│  🦅 Eagles          [Ícone Perfil]  │
│  [Empresa Selecionada] ▼            │
│  📅 Dezembro 2025                   │
├─────────────────────────────────────┤
│                                     │
│  ┌─────────────────────────────┐   │
│  │ SEMÁFORO DE SAÚDE           │   │
│  │                             │   │
│  │     [Círculo Grande]        │   │
│  │         🟢                  │   │
│  │      SAUDÁVEL               │   │
│  │                             │   │
│  │  Baseado nas metas          │   │
│  │  definidas pelo contador    │   │
│  └─────────────────────────────┘   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ INDICADORES-CHAVE           │   │
│  ├─────────────────────────────┤   │
│  │ 💰 Lucro Líquido            │   │
│  │    R$ 45.230,00             │   │
│  │    ↗ +12% vs mês anterior   │   │
│  │                             │   │
│  │ 📊 Margem de Contribuição   │   │
│  │    32,5%                    │   │
│  │    [Barra de Progresso]     │   │
│  │    ████████░░░░ Meta: 35%   │   │
│  │                             │   │
│  │ ⚖️ Ponto de Equilíbrio       │   │
│  │    R$ 28.500,00             │   │
│  │    ✓ Atingido               │   │
│  └─────────────────────────────┘   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ LUCRO REAL                  │   │
│  ├─────────────────────────────┤   │
│  │ Competência: R$ 45.230,00   │   │
│  │ Caixa:       R$ 38.100,00   │   │
│  │ Diferença:   R$ 7.130,00    │   │
│  │ [Ícone Info: Ver detalhes]  │   │
│  └─────────────────────────────┘   │
│                                     │
│  [Scroll para mais...]              │
│                                     │
├─────────────────────────────────────┤
│  [Nav Bar]                          │
│  🏠 Visão  🔍 Lente  📬 Alertas    │
└─────────────────────────────────────┘
```

**Componentes**:
- **Semáforo de Saúde**: Indicador visual grande e imediato
  - Verde: Empresa saudável (metas atingidas)
  - Amarelo: Atenção necessária (próximo das metas)
  - Vermelho: Alerta crítico (abaixo das metas)
- **Indicadores-Chave**: Cards com métricas principais
- **Comparativos**: Setas e percentuais de evolução
- **Barras de Progresso**: Visualização de metas

---

## TELA 3: Lente do Contador (Contas Destacadas)

```
┌─────────────────────────────────────┐
│  [← Voltar]  Lente do Contador      │
│  📅 Dezembro 2025                   │
├─────────────────────────────────────┤
│                                     │
│  🔍 Observações do Contador         │
│  Samuel destacou 4 contas           │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ [Badge: RECEITA]            │   │
│  │ 3.1.01 - Vendas de Produtos │   │
│  │                             │   │
│  │ Saldo Atual: R$ 125.300,00  │   │
│  │ ↗ +18% vs mês anterior      │   │
│  │                             │   │
│  │ 💬 Observação do Contador:  │   │
│  │ "Excelente crescimento nas  │   │
│  │ vendas de produtos premium. │   │
│  │ Recomendo manter estratégia │   │
│  │ de marketing focada nesse   │   │
│  │ segmento."                  │   │
│  │                             │   │
│  │ Por: Samuel | 20/12/2025    │   │
│  └─────────────────────────────┘   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ [Badge: DESPESA]            │   │
│  │ 4.1.15 - Despesas com       │   │
│  │          Fornecedores       │   │
│  │                             │   │
│  │ Saldo Atual: R$ 32.800,00   │   │
│  │ ⚠ +35% vs mês anterior      │   │
│  │                             │   │
│  │ 💬 Observação do Contador:  │   │
│  │ "Atenção: aumento           │   │
│  │ significativo nas despesas  │   │
│  │ com fornecedores. Sugiro    │   │
│  │ renegociação de contratos   │   │
│  │ e análise de alternativas." │   │
│  │                             │   │
│  │ Por: Samuel | 21/12/2025    │   │
│  └─────────────────────────────┘   │
│                                     │
│  [Scroll para mais...]              │
│                                     │
├─────────────────────────────────────┤
│  [Nav Bar]                          │
│  🏠 Visão  🔍 Lente  📬 Alertas    │
└─────────────────────────────────────┘
```

**Comportamento**:
- Lista apenas contas com observações aprovadas e destacadas
- Cards com código da conta, nome, saldo e variação
- Observação contextualizada do contador em destaque
- Badges coloridos por tipo de conta (Receita/Despesa/Ativo/Passivo)
- Informação de quem fez a observação e quando

---

## TELA 4: Alertas e Notificações

```
┌─────────────────────────────────────┐
│  [← Voltar]  Alertas                │
├─────────────────────────────────────┤
│                                     │
│  [Filtros: Todos ▼  Não Lidos ▼]   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ [Ícone Vermelho] CRÍTICO    │   │
│  │ Ponto de Equilíbrio         │   │
│  │                             │   │
│  │ Empresa está próxima do     │   │
│  │ ponto de equilíbrio. Atenção│   │
│  │ às despesas operacionais.   │   │
│  │                             │   │
│  │ 23/12/2025 - 14:30          │   │
│  │ [Marcar como lido]          │   │
│  └─────────────────────────────┘   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ [Ícone Amarelo] ATENÇÃO     │   │
│  │ Health Check - Gerente      │   │
│  │                             │   │
│  │ Desempenho do gerente em    │   │
│  │ Dezembro: 85% de completude │   │
│  │ nos registros. 3 atrasos não│   │
│  │ justificados.               │   │
│  │                             │   │
│  │ 22/12/2025 - 09:15          │   │
│  │ [Marcar como lido]          │   │
│  └─────────────────────────────┘   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ [Ícone Verde] INFORMATIVO   │   │
│  │ Balancete Disponível        │   │
│  │                             │   │
│  │ O balancete de Dezembro foi │   │
│  │ importado e está disponível │   │
│  │ para consulta.              │   │
│  │                             │   │
│  │ 20/12/2025 - 16:00          │   │
│  │ ✓ Lido                      │   │
│  └─────────────────────────────┘   │
│                                     │
│  [Scroll para mais...]              │
│                                     │
├─────────────────────────────────────┤
│  [Nav Bar]                          │
│  🏠 Visão  🔍 Lente  📬 Alertas    │
└─────────────────────────────────────┘
```

**Tipos de Alertas**:
- **CRÍTICO** (Vermelho): Situações urgentes que requerem ação imediata
- **ATENÇÃO** (Amarelo): Situações que merecem monitoramento
- **INFORMATIVO** (Verde): Notificações gerais e atualizações

**Comportamento**:
- Apenas alertas aprovados pelo contador são exibidos
- Notificações push para alertas críticos
- Filtros por tipo e status de leitura
- Marcar como lido/não lido

---

## TELA 5: Detalhamento de Indicador (Lucro Real)

```
┌─────────────────────────────────────┐
│  [← Voltar]  Lucro Real             │
│  📅 Dezembro 2025                   │
├─────────────────────────────────────┤
│                                     │
│  ┌─────────────────────────────┐   │
│  │ REGIME DE COMPETÊNCIA       │   │
│  │                             │   │
│  │ Receitas:    R$ 125.300,00  │   │
│  │ (-) Custos:  R$  52.100,00  │   │
│  │ (-) Despesas:R$  27.970,00  │   │
│  │ ─────────────────────────   │   │
│  │ = Lucro:     R$  45.230,00  │   │
│  └─────────────────────────────┘   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ REGIME DE CAIXA             │   │
│  │                             │   │
│  │ Entradas:    R$ 108.200,00  │   │
│  │ (-) Saídas:  R$  70.100,00  │   │
│  │ ─────────────────────────   │   │
│  │ = Saldo:     R$  38.100,00  │   │
│  └─────────────────────────────┘   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ ANÁLISE                     │   │
│  │                             │   │
│  │ Diferença: R$ 7.130,00      │   │
│  │                             │   │
│  │ ℹ️ A diferença entre         │   │
│  │ competência e caixa indica  │   │
│  │ valores a receber de vendas │   │
│  │ realizadas no mês.          │   │
│  └─────────────────────────────┘   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ [Gráfico de Barras]         │   │
│  │ Comparativo 6 meses         │   │
│  │                             │   │
│  │ Jul Ago Set Out Nov Dez     │   │
│  │ ███ ███ ███ ███ ███ ████    │   │
│  └─────────────────────────────┘   │
│                                     │
└─────────────────────────────────────┘
```

**Comportamento**:
- Detalhamento completo do indicador selecionado
- Comparação entre regimes (Competência vs Caixa)
- Explicações contextuais para o dono
- Gráficos de evolução temporal
- Possibilidade de exportar relatório

---

## TELA 6: Perfil e Configurações

```
┌─────────────────────────────────────┐
│  [← Voltar]  Perfil                 │
├─────────────────────────────────────┤
│                                     │
│  [Avatar Grande]                    │
│  [Nome do Dono]                     │
│  Proprietário                       │
│                                     │
│  ┌───────────────────────────────┐ │
│  │ Empresas Vinculadas:          │ │
│  │                               │ │
│  │ • Empresa ABC Ltda            │ │
│  │ • Empresa XYZ Comércio        │ │
│  │                               │ │
│  │ [Trocar Empresa]              │ │
│  └───────────────────────────────┘ │
│                                     │
│  ┌───────────────────────────────┐ │
│  │ Preferências                  │ │
│  │                               │ │
│  │ 🔔 Notificações               │ │
│  │    [Toggle ON]                │ │
│  │                               │ │
│  │ 📊 Período Padrão             │ │
│  │    [Mês Atual ▼]              │ │
│  │                               │ │
│  │ 🌙 Tema                       │ │
│  │    [Dark Mode (fixo)]         │ │
│  └───────────────────────────────┘ │
│                                     │
│  ┌───────────────────────────────┐ │
│  │ Contador Responsável:         │ │
│  │                               │ │
│  │ [Avatar] Samuel Costa         │ │
│  │ contador@eagles.com           │ │
│  │ [Enviar Mensagem]             │ │
│  └───────────────────────────────┘ │
│                                     │
│  ┌───────────────────────────────┐ │
│  │ [Botão: Sair]                 │ │
│  │ Background: Transparente      │ │
│  │ Color: #EF4444                │ │
│  └───────────────────────────────┘ │
│                                     │
└─────────────────────────────────────┘
```

---

## TELA 7: Mensagens com Contador

```
┌─────────────────────────────────────┐
│  [← Voltar]  Mensagens              │
│  Conversa com Samuel Costa          │
├─────────────────────────────────────┤
│                                     │
│  [Data: 20/12/2025]                 │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ Samuel (Contador)           │   │
│  │ 10:30                       │   │
│  │                             │   │
│  │ Bom dia! O balancete de     │   │
│  │ dezembro já está disponível.│   │
│  │ Destaquei algumas contas    │   │
│  │ importantes para sua análise│   │
│  └─────────────────────────────┘   │
│                                     │
│       ┌─────────────────────────┐  │
│       │ Você (Dono)             │  │
│       │ 11:15                   │  │
│       │                         │  │
│       │ Obrigado! Vi o aumento  │  │
│       │ nas despesas. Podemos   │  │
│       │ conversar sobre isso?   │  │
│       └─────────────────────────┘  │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ Samuel (Contador)           │   │
│  │ 11:20                       │   │
│  │                             │   │
│  │ Claro! Vou preparar um      │   │
│  │ relatório detalhado e       │   │
│  │ agendamos uma reunião.      │   │
│  └─────────────────────────────┘   │
│                                     │
│  [Scroll para mais...]              │
│                                     │
├─────────────────────────────────────┤
│  [Input: Digite sua mensagem...]    │
│  [Botão Enviar: →]                  │
└─────────────────────────────────────┘
```

**Comportamento**:
- Chat contextualizado com o contador
- Histórico de conversas
- Notificações de novas mensagens
- Possibilidade de anexar arquivos

---

## Pseudo-código: Componente Dashboard Estratégico

```javascript
// Componente: DashboardDono.jsx

import React, { useState, useEffect } from 'react';
import { View, Text, ScrollView, RefreshControl } from 'react-native';
import { api } from '../services/api';
import SemaforoSaude from '../components/SemaforoSaude';
import IndicadorCard from '../components/IndicadorCard';
import LucroRealCard from '../components/LucroRealCard';

const DashboardDono = ({ idCliente }) => {
  const [indicadores, setIndicadores] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const carregarIndicadores = async () => {
    try {
      const mesAtual = new Date().getMonth() + 1;
      const anoAtual = new Date().getFullYear();

      const response = await api.get('/api/indicadores/dashboard', {
        params: {
          id_cliente: idCliente,
          mes: mesAtual,
          ano: anoAtual
        }
      });

      setIndicadores(response.data);
    } catch (error) {
      console.error('Erro ao carregar indicadores:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    carregarIndicadores();
  }, [idCliente]);

  const onRefresh = () => {
    setRefreshing(true);
    carregarIndicadores();
  };

  if (loading) {
    return <LoadingScreen />;
  }

  return (
    <ScrollView
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    >
      {/* Semáforo de Saúde */}
      <SemaforoSaude
        status={indicadores.semaforo_saude}
        descricao={indicadores.descricao_saude}
      />

      {/* Indicadores-Chave */}
      <View style={styles.indicadoresContainer}>
        <IndicadorCard
          titulo="Lucro Líquido"
          valor={indicadores.lucro_liquido_competencia}
          variacao={indicadores.variacao_lucro}
          tipo="moeda"
          icone="💰"
        />

        <IndicadorCard
          titulo="Margem de Contribuição"
          valor={indicadores.margem_contribuicao}
          meta={indicadores.meta_margem}
          tipo="percentual"
          icone="📊"
        />

        <IndicadorCard
          titulo="Ponto de Equilíbrio"
          valor={indicadores.ponto_equilibrio}
          atingido={indicadores.ponto_equilibrio_atingido}
          tipo="moeda"
          icone="⚖️"
        />
      </View>

      {/* Lucro Real (Competência vs Caixa) */}
      <LucroRealCard
        lucroCompetencia={indicadores.lucro_liquido_competencia}
        lucroCaixa={indicadores.lucro_liquido_caixa}
        diferenca={indicadores.diferenca_regime}
      />

      {/* Botão para ver mais detalhes */}
      <TouchableOpacity
        style={styles.botaoDetalhes}
        onPress={() => navigation.navigate('DetalhesIndicadores')}
      >
        <Text style={styles.botaoText}>Ver Análise Completa</Text>
      </TouchableOpacity>
    </ScrollView>
  );
};

const styles = {
  container: {
    flex: 1,
    backgroundColor: '#0A0E1A'
  },
  indicadoresContainer: {
    padding: 16,
    gap: 16
  },
  botaoDetalhes: {
    margin: 16,
    padding: 16,
    backgroundColor: '#151B2D',
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#1F2937',
    alignItems: 'center'
  },
  botaoText: {
    color: '#10B981',
    fontSize: 16,
    fontWeight: '600'
  }
};

export default DashboardDono;
```

---

## Componente: Semáforo de Saúde

```javascript
// Componente: SemaforoSaude.jsx

import React from 'react';
import { View, Text } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';

const SemaforoSaude = ({ status, descricao }) => {
  const getStatusConfig = () => {
    switch (status) {
      case 'VERDE':
        return {
          cor: '#10B981',
          gradiente: ['#10B981', '#059669'],
          emoji: '🟢',
          texto: 'SAUDÁVEL'
        };
      case 'AMARELO':
        return {
          cor: '#F59E0B',
          gradiente: ['#F59E0B', '#D97706'],
          emoji: '🟡',
          texto: 'ATENÇÃO'
        };
      case 'VERMELHO':
        return {
          cor: '#EF4444',
          gradiente: ['#EF4444', '#DC2626'],
          emoji: '🔴',
          texto: 'ALERTA'
        };
      default:
        return {
          cor: '#6B7280',
          gradiente: ['#6B7280', '#4B5563'],
          emoji: '⚪',
          texto: 'SEM DADOS'
        };
    }
  };

  const config = getStatusConfig();

  return (
    <View style={styles.container}>
      <Text style={styles.titulo}>SEMÁFORO DE SAÚDE</Text>
      
      <LinearGradient
        colors={config.gradiente}
        style={styles.circulo}
      >
        <Text style={styles.emoji}>{config.emoji}</Text>
      </LinearGradient>

      <Text style={[styles.statusTexto, { color: config.cor }]}>
        {config.texto}
      </Text>

      <Text style={styles.descricao}>{descricao}</Text>
    </View>
  );
};

const styles = {
  container: {
    backgroundColor: '#151B2D',
    margin: 16,
    padding: 24,
    borderRadius: 12,
    alignItems: 'center'
  },
  titulo: {
    color: '#8B92A8',
    fontSize: 12,
    fontWeight: '600',
    letterSpacing: 1,
    marginBottom: 16
  },
  circulo: {
    width: 120,
    height: 120,
    borderRadius: 60,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 16
  },
  emoji: {
    fontSize: 48
  },
  statusTexto: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 8
  },
  descricao: {
    color: '#8B92A8',
    fontSize: 14,
    textAlign: 'center',
    lineHeight: 20
  }
};

export default SemaforoSaude;
```

---

## Fluxo de Navegação

```
Login (QR Code)
    ↓
Dashboard Estratégico "Voo da Águia"
    ↓
    ├→ Aba Lente → Contas Destacadas pelo Contador
    ├→ Aba Alertas → Lista de Alertas e Notificações
    ├→ Indicador → Detalhamento (Lucro Real, Margem, etc)
    ├→ Perfil → Configurações e Empresas
    └→ Mensagens → Chat com Contador
```

---

## Considerações de UX

1. **Clareza Absoluta**: Informações financeiras apresentadas de forma simples e direta
2. **Hierarquia Visual**: Semáforo de Saúde como elemento principal, seguido de indicadores
3. **Contexto Sempre Presente**: Explicações e observações do contador integradas
4. **Decisões Informadas**: Dados comparativos e históricos para embasar decisões
5. **Comunicação Direta**: Canal direto com o contador para dúvidas
6. **Notificações Inteligentes**: Apenas alertas relevantes e aprovados
7. **Responsividade**: Adaptação perfeita a diferentes tamanhos de tela
8. **Offline Capability**: Visualização de dados em cache quando offline
