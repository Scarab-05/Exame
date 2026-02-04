# RoomFlow

RoomFlow é uma aplicação web projetada para gerenciar reservas de salas de forma eficiente. Os utilizadores podem visualizar salas disponíveis, reservá-las, e os administradores podem gerenciar salas e reservas.

## Funcionalidades

### Funcionalidades para Utilizadores
1. **Lista de Salas**: Visualizar salas disponíveis com suas capacidades.
2. **Reserva Flexível**: Selecionar sala, data, hora de início e hora de término personalizada.
3. **Prevenção de Conflitos**: Impede reservas sobrepostas com mensagens de erro claras.
4. **Persistência de Sessão**: Mantém o utilizador autenticado mesmo após reiniciar a aplicação.
5. **Cancelamento de Reservas**: Permite cancelar reservas existentes diretamente no calendário.

### Funcionalidades para Administradores
1. **Gestão de Salas**: Adicionar ou remover salas.
2. **Gestão de Reservas**: Visualizar, cancelar ou apagar reservas.

## Detalhes Técnicos
- **Frontend**: Interface moderna para utilizadores e administradores, com suporte para seleção dinâmica de horários.
- **Backend**: Lógica de reservas, prevenção de conflitos e persistência de sessão.
- **Base de Dados**: SQLite para armazenar dados de salas e reservas.
- **Versionamento**: Git para controlo de versões.

## Primeiros Passos
1. Clone o repositório.
2. Configure a base de dados SQLite.
3. Execute a aplicação com o comando:
   ```bash
   python RoomFlow/app.py
   ```

## Requisitos
- Python
- Flask
- Flask-Session
- SQLite