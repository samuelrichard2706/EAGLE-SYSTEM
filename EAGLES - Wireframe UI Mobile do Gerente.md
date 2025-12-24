# EAGLES - Wireframe UI Mobile do Gerente

## Identidade Visual Eagles
- **Tema**: Dark Mode
- **Paleta de Cores**:
  - Background principal: `#0A0E1A` (Azul escuro profundo)
  - Background secundário: `#151B2D` (Azul escuro médio)
  - Texto primário: `#E8EAF0` (Branco suave)
  - Texto secundário: `#8B92A8` (Cinza azulado)
  - Accent Verde (Positivo): `#10B981` (Verde águia)
  - Accent Vermelho (Alerta): `#EF4444` (Vermelho alerta)
  - Accent Amarelo (Atenção): `#F59E0B` (Amarelo atenção)
  - Bordas: `#1F2937` (Cinza escuro)
- **Tipografia**: 
  - Fonte: Inter ou SF Pro (iOS) / Roboto (Android)
  - Títulos: Bold, 20-24px
  - Subtítulos: Semibold, 16-18px
  - Corpo: Regular, 14-16px
- **Ícones**: Lucide Icons ou Heroicons (linhas finas, minimalistas)
- **Espaçamento**: 8px grid system (8, 16, 24, 32px)

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
│         Acesso Gerente              │
│                                     │
└─────────────────────────────────────┘
```

**Comportamento**:
- Ao clicar em "Escanear QR Code", abre a câmera
- Após escaneamento bem-sucedido, valida via API `/api/auth/validar-qrcode`
- Armazena token de sessão localmente
- Redireciona para Dashboard Operacional

---

## TELA 2: Dashboard Operacional (Home)

```
┌─────────────────────────────────────┐
│  [Status Bar]                       │
├─────────────────────────────────────┤
│  🦅 Eagles          [Ícone Perfil]  │
│  Olá, [Nome Gerente]                │
│  [Cliente Selecionado] ▼            │
├─────────────────────────────────────┤
│                                     │
│  📅 Escala de Hoje                  │
│  [Data: Terça, 24 Dez 2025]        │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ TURNO MANHÃ (08:00-12:00)  │   │
│  ├─────────────────────────────┤   │
│  │ ✓ João Silva                │   │
│  │   Check-in: 08:05           │   │
│  │   [Badge Verde: PRESENTE]   │   │
│  ├─────────────────────────────┤   │
│  │ ⚠ Maria Santos              │   │
│  │   Check-in: 08:20           │   │
│  │   [Badge Amarelo: ATRASO]   │   │
│  ├─────────────────────────────┤   │
│  │ ✗ Pedro Costa               │   │
│  │   [Badge Vermelho: FALTA]   │   │
│  │   [Botão: Registrar Falta]  │   │
│  └─────────────────────────────┘   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ TURNO TARDE (13:00-18:00)  │   │
│  ├─────────────────────────────┤   │
│  │ ⏱ Ana Oliveira              │   │
│  │   [Badge Cinza: PENDENTE]   │   │
│  │   [Botão: Fazer Check-in]   │   │
│  └─────────────────────────────┘   │
│                                     │
│  ┌───────────────────────────────┐ │
│  │ [Botão: Registrar Caixa]     │ │
│  │ [Botão: Adicionar Despesa]   │ │
│  └───────────────────────────────┘ │
│                                     │
├─────────────────────────────────────┤
│  [Nav Bar]                          │
│  🏠 Home  👥 Equipe  📊 Relatórios │
└─────────────────────────────────────┘
```

**Componentes**:
- **Header**: Logo, nome do gerente, seletor de cliente
- **Seção Escala**: Cards por turno com lista de funcionários
- **Status Badges**:
  - Verde (#10B981): Presente
  - Amarelo (#F59E0B): Atraso
  - Vermelho (#EF4444): Falta
  - Cinza (#6B7280): Pendente
- **Botões de Ação**: Destaque visual, fácil acesso
- **Bottom Navigation**: 3 abas principais

---

## TELA 3: Registro de Presença (Check-in)

```
┌─────────────────────────────────────┐
│  [← Voltar]  Check-in               │
├─────────────────────────────────────┤
│                                     │
│  Funcionário Selecionado:           │
│                                     │
│  ┌───────────────────────────────┐ │
│  │  [Avatar]  Ana Oliveira       │ │
│  │  Cargo: Atendente             │ │
│  │  Turno: TARDE (13:00-18:00)   │ │
│  └───────────────────────────────┘ │
│                                     │
│  Horário de Check-in:               │
│  ┌───────────────────────────────┐ │
│  │  [13:05]  🕐                  │ │
│  │  (Automático)                 │ │
│  └───────────────────────────────┘ │
│                                     │
│  Status:                            │
│  ┌───────────────────────────────┐ │
│  │  ○ Presente (No horário)      │ │
│  │  ○ Atraso (Após tolerância)   │ │
│  └───────────────────────────────┘ │
│                                     │
│  ⚠ Tolerância: 15 minutos          │
│  ✓ Status sugerido: PRESENTE       │
│                                     │
│  ┌───────────────────────────────┐ │
│  │  [Botão: Confirmar Check-in]  │ │
│  │  Background: #10B981          │ │
│  └───────────────────────────────┘ │
│                                     │
│  ┌───────────────────────────────┐ │
│  │  [Botão: Cancelar]            │ │
│  │  Background: Transparente     │ │
│  │  Border: #1F2937              │ │
│  └───────────────────────────────┘ │
│                                     │
└─────────────────────────────────────┘
```

**Comportamento**:
- Horário capturado automaticamente ao abrir a tela
- Sistema calcula automaticamente se é atraso (baseado na escala + 15min tolerância)
- Ao confirmar, chama API `/api/presenca/registrar-checkin`
- Mostra feedback visual de sucesso (toast verde)
- Retorna ao Dashboard

---

## TELA 4: Registro de Falta

```
┌─────────────────────────────────────┐
│  [← Voltar]  Registrar Falta        │
├─────────────────────────────────────┤
│                                     │
│  Funcionário:                       │
│  ┌───────────────────────────────┐ │
│  │  [Avatar]  Pedro Costa        │ │
│  │  Cargo: Auxiliar              │ │
│  │  Data: 24/12/2025             │ │
│  └───────────────────────────────┘ │
│                                     │
│  Tipo de Falta:                     │
│  ┌───────────────────────────────┐ │
│  │  ○ Justificada                │ │
│  │  ○ Injustificada              │ │
│  └───────────────────────────────┘ │
│                                     │
│  Motivo (opcional):                 │
│  ┌───────────────────────────────┐ │
│  │  [Text Area]                  │ │
│  │  Ex: Atestado médico          │ │
│  │                               │ │
│  │                               │ │
│  └───────────────────────────────┘ │
│                                     │
│  ┌───────────────────────────────┐ │
│  │  [Botão: Registrar Falta]     │ │
│  │  Background: #EF4444          │ │
│  └───────────────────────────────┘ │
│                                     │
│  ┌───────────────────────────────┐ │
│  │  [Botão: Cancelar]            │ │
│  └───────────────────────────────┘ │
│                                     │
└─────────────────────────────────────┘
```

**Comportamento**:
- Seleção obrigatória do tipo de falta
- Campo de motivo opcional (mas recomendado para justificadas)
- Ao confirmar, chama API `/api/presenca/registrar-falta`
- Feedback visual de confirmação
- Retorna ao Dashboard

---

## TELA 5: Fechamento de Caixa "Cego"

```
┌─────────────────────────────────────┐
│  [← Voltar]  Fechamento de Caixa    │
├─────────────────────────────────────┤
│                                     │
│  📅 Data: 24/12/2025                │
│  🕐 Horário: 18:30                  │
│                                     │
│  Valor Total do Caixa:              │
│  ┌───────────────────────────────┐ │
│  │  R$                           │ │
│  │  [Input Numérico Grande]      │ │
│  │  0,00                         │ │
│  └───────────────────────────────┘ │
│                                     │
│  [Teclado Numérico]                 │
│  ┌─────────────────────────────┐   │
│  │  1    2    3                │   │
│  │  4    5    6                │   │
│  │  7    8    9                │   │
│  │  ,    0    ⌫                │   │
│  └─────────────────────────────┘   │
│                                     │
│  ℹ️ Fechamento "Cego"               │
│  Informe o valor sem conferência   │
│  prévia do sistema                  │
│                                     │
│  ┌───────────────────────────────┐ │
│  │  [Botão: Confirmar Fechamento]│ │
│  │  Background: #10B981          │ │
│  └───────────────────────────────┘ │
│                                     │
└─────────────────────────────────────┘
```

**Comportamento**:
- Input numérico grande e destacado
- Teclado customizado para facilitar entrada
- Não mostra valor esperado (fechamento "cego")
- Ao confirmar, chama API de fechamento de caixa
- Mostra confirmação e retorna ao Dashboard

---

## TELA 6: Adicionar Despesa (com Câmera)

```
┌─────────────────────────────────────┐
│  [← Voltar]  Nova Despesa           │
├─────────────────────────────────────┤
│                                     │
│  Comprovante:                       │
│  ┌───────────────────────────────┐ │
│  │  [Área de Preview da Foto]    │ │
│  │                               │ │
│  │  [Ícone Câmera Grande]        │ │
│  │  Tirar Foto do Comprovante    │ │
│  │                               │ │
│  └───────────────────────────────┘ │
│  [Botão: 📷 Capturar]              │
│                                     │
│  Descrição:                         │
│  ┌───────────────────────────────┐ │
│  │  [Input Text]                 │ │
│  │  Ex: Compra de materiais      │ │
│  └───────────────────────────────┘ │
│                                     │
│  Valor:                             │
│  ┌───────────────────────────────┐ │
│  │  R$ [Input Numérico]          │ │
│  │  0,00                         │ │
│  └───────────────────────────────┘ │
│                                     │
│  Data:                              │
│  ┌───────────────────────────────┐ │
│  │  [Date Picker]                │ │
│  │  24/12/2025  📅               │ │
│  └───────────────────────────────┘ │
│                                     │
│  Categoria:                         │
│  ┌───────────────────────────────┐ │
│  │  [Dropdown]                   │ │
│  │  Selecione...  ▼              │ │
│  └───────────────────────────────┘ │
│                                     │
│  ┌───────────────────────────────┐ │
│  │  [Botão: Salvar Despesa]      │ │
│  │  Background: #10B981          │ │
│  └───────────────────────────────┘ │
│                                     │
└─────────────────────────────────────┘
```

**Comportamento**:
- Ao clicar em "Capturar", abre câmera nativa
- Após captura, mostra preview da foto
- Permite editar/recapturar
- Upload da foto junto com dados da despesa
- Validação: descrição, valor e data obrigatórios
- Feedback de sucesso e retorno ao Dashboard

---

## TELA 7: Equipe (Lista Completa)

```
┌─────────────────────────────────────┐
│  🦅 Eagles          [Ícone Perfil]  │
│  Gestão de Equipe                   │
├─────────────────────────────────────┤
│                                     │
│  [Barra de Busca]                   │
│  🔍 Buscar funcionário...           │
│                                     │
│  [Filtros: Todos ▼  Ativos ▼]      │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ [Avatar] João Silva         │   │
│  │ Cargo: Gerente              │   │
│  │ ✓ 23 presenças | ⚠ 2 atrasos│  │
│  │ [Ver Detalhes →]            │   │
│  └─────────────────────────────┘   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ [Avatar] Maria Santos       │   │
│  │ Cargo: Atendente            │   │
│  │ ✓ 24 presenças | ✗ 1 falta  │   │
│  │ [Ver Detalhes →]            │   │
│  └─────────────────────────────┘   │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ [Avatar] Pedro Costa        │   │
│  │ Cargo: Auxiliar             │   │
│  │ ✓ 20 presenças | ✗ 3 faltas │   │
│  │ [Ver Detalhes →]            │   │
│  └─────────────────────────────┘   │
│                                     │
│  [Scroll...]                        │
│                                     │
├─────────────────────────────────────┤
│  [Nav Bar]                          │
│  🏠 Home  👥 Equipe  📊 Relatórios │
└─────────────────────────────────────┘
```

**Comportamento**:
- Lista todos os funcionários ativos
- Busca em tempo real
- Resumo de presença/faltas do mês
- Ao clicar em "Ver Detalhes", abre tela de histórico individual

---

## Pseudo-código: Componente de Check-in

```javascript
// Componente: RegistroPresenca.jsx

import React, { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, Alert } from 'react-native';
import { api } from '../services/api';

const RegistroPresenca = ({ funcionario, onSuccess }) => {
  const [horaCheckin, setHoraCheckin] = useState('');
  const [statusSugerido, setStatusSugerido] = useState('PRESENTE');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Captura hora atual
    const agora = new Date();
    const hora = agora.toTimeString().slice(0, 8);
    setHoraCheckin(hora);

    // Calcula status baseado na escala
    if (funcionario.escala && funcionario.escala.hora_inicio) {
      const horaEscala = new Date(`2000-01-01T${funcionario.escala.hora_inicio}`);
      const horaLimite = new Date(horaEscala.getTime() + 15 * 60000); // +15min
      const horaAtual = new Date(`2000-01-01T${hora}`);

      if (horaAtual > horaLimite) {
        setStatusSugerido('ATRASO');
      }
    }
  }, []);

  const handleConfirmarCheckin = async () => {
    setLoading(true);
    
    try {
      const response = await api.post('/api/presenca/registrar-checkin', {
        id_funcionario: funcionario.id_funcionario,
        hora_checkin: horaCheckin,
        status_presenca: statusSugerido
      });

      if (response.data.sucesso) {
        Alert.alert('Sucesso', 'Check-in registrado com sucesso!');
        onSuccess();
      }
    } catch (error) {
      Alert.alert('Erro', error.response?.data?.erro || 'Erro ao registrar check-in');
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      {/* UI conforme wireframe */}
      <View style={styles.funcionarioCard}>
        <Text style={styles.nome}>{funcionario.nome_completo}</Text>
        <Text style={styles.cargo}>{funcionario.cargo}</Text>
      </View>

      <View style={styles.horaContainer}>
        <Text style={styles.horaLabel}>Horário de Check-in:</Text>
        <Text style={styles.hora}>{horaCheckin}</Text>
      </View>

      <View style={styles.statusContainer}>
        <Text style={styles.statusLabel}>Status Sugerido:</Text>
        <View style={[
          styles.badge,
          statusSugerido === 'PRESENTE' ? styles.badgeVerde : styles.badgeAmarelo
        ]}>
          <Text style={styles.badgeText}>{statusSugerido}</Text>
        </View>
      </View>

      <TouchableOpacity
        style={[styles.botaoConfirmar, loading && styles.botaoDisabled]}
        onPress={handleConfirmarCheckin}
        disabled={loading}
      >
        <Text style={styles.botaoText}>
          {loading ? 'Registrando...' : 'Confirmar Check-in'}
        </Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = {
  container: {
    flex: 1,
    backgroundColor: '#0A0E1A',
    padding: 16
  },
  funcionarioCard: {
    backgroundColor: '#151B2D',
    padding: 16,
    borderRadius: 8,
    marginBottom: 24
  },
  nome: {
    color: '#E8EAF0',
    fontSize: 18,
    fontWeight: '600'
  },
  cargo: {
    color: '#8B92A8',
    fontSize: 14,
    marginTop: 4
  },
  horaContainer: {
    marginBottom: 24
  },
  horaLabel: {
    color: '#8B92A8',
    fontSize: 14,
    marginBottom: 8
  },
  hora: {
    color: '#E8EAF0',
    fontSize: 32,
    fontWeight: 'bold'
  },
  statusContainer: {
    marginBottom: 32
  },
  statusLabel: {
    color: '#8B92A8',
    fontSize: 14,
    marginBottom: 8
  },
  badge: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 16,
    alignSelf: 'flex-start'
  },
  badgeVerde: {
    backgroundColor: '#10B981'
  },
  badgeAmarelo: {
    backgroundColor: '#F59E0B'
  },
  badgeText: {
    color: '#FFFFFF',
    fontWeight: '600'
  },
  botaoConfirmar: {
    backgroundColor: '#10B981',
    padding: 16,
    borderRadius: 8,
    alignItems: 'center'
  },
  botaoDisabled: {
    opacity: 0.5
  },
  botaoText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600'
  }
};

export default RegistroPresenca;
```

---

## Fluxo de Navegação

```
Login (QR Code)
    ↓
Dashboard Operacional (Home)
    ↓
    ├→ Fazer Check-in → Tela de Check-in → [Sucesso] → Dashboard
    ├→ Registrar Falta → Tela de Falta → [Sucesso] → Dashboard
    ├→ Registrar Caixa → Tela de Caixa → [Sucesso] → Dashboard
    ├→ Adicionar Despesa → Tela de Despesa → [Sucesso] → Dashboard
    ├→ Aba Equipe → Lista de Equipe → Detalhes Funcionário
    └→ Aba Relatórios → Relatórios Mensais
```

---

## Considerações de UX

1. **Feedback Imediato**: Todos os botões devem ter feedback tátil (vibração leve)
2. **Loading States**: Indicadores visuais durante operações assíncronas
3. **Validação em Tempo Real**: Campos validados antes do envio
4. **Offline First**: Armazenar dados localmente se sem conexão, sincronizar depois
5. **Acessibilidade**: Tamanhos de fonte ajustáveis, contraste adequado
6. **Gestos**: Swipe para atualizar listas, pull-to-refresh
7. **Notificações**: Push notifications para lembretes de escala e alertas
