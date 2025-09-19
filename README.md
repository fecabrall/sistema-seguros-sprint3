# Sistema de Seguros NeoRoute CLI

Sistema de gestão de seguros desenvolvido em Python com interface de linha de comando (CLI), utilizando SQLite para persistência de dados, auditoria completa e experiência otimizada no terminal.

---

## Autores

- **AUGUSTO OLIVEIRA CODO DE SOUZA** — RM: 562080  
- **FELIPE DE OLIVEIRA CABRAL** — RM: 561720  
- **JONAS ALAF DA SILVA** — RM: 566479  
- **SOFIA BUERIS NETTO DE SOUZA** — RM: 565818  
- **VINICIUS ADRIAN SIQUEIRA DE OLIVEIRA** — RM: 564962  

---

## Estrutura do Projeto

```
sistema-seguros-sprint3/
├── neoroute/                # Módulo principal do sistema
│   ├── __init__.py
│   ├── __main__.py         # Ponto de entrada principal
│   ├── cli.py              # Interface de linha de comando
│   ├── models.py           # Modelos de dados SQLAlchemy
│   ├── db.py               # Configuração do banco SQLite
│   ├── auth.py             # Sistema de autenticação
│   ├── audit.py            # Sistema de auditoria e logs
│   ├── migrate.py          # Migração de dados JSON → SQLite
│   ├── utils.py            # Validações e utilitários
│   ├── exceptions.py       # Exceções customizadas
│   └── logger.py           # Configuração de logs
├── scripts/
│   └── relatorios.py       # Geração de relatórios avançados
├── data/
│   ├── seguros.db          # Banco de dados SQLite principal
│   └── initial_admin.txt   # Credenciais do administrador
├── dados/                  # Dados iniciais em JSON (Sprint 2)
│   ├── clientes.json
│   ├── apolices.json
│   ├── seguros.json
│   └── sinistros.json
├── logs/                   # Arquivos de log do sistema
├── exports/                # Relatórios exportados (CSV/JSON)
├── tests/                  # Testes automatizados
├── requirements.txt        # Dependências Python
└── .env.example           # Exemplo de variáveis de ambiente
```

---

## Instalação e Configuração

### 1. Clonar o repositório
```bash
git clone https://github.com/fecabrall/sistema-seguros-sprint3.git
cd sistema-seguros-sprint3
```

### 2. Criar ambiente virtual
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente (opcional)
```bash
cp .env.example .env
# Editar .env se necessário (padrão: SQLite local)
```

### 5. Executar migração inicial (uma única vez)
```bash
python -m neoroute.migrate
```
*Este comando cria o schema SQLite e importa os dados JSON da Sprint 2*

---

## Como Usar

### Iniciar o Sistema
```bash
python -m neoroute
```

**Credenciais de Acesso:**
- **Usuário:** `admin`
- **Senha:** `admin1234@`

### Menu Principal
Após o login, você terá acesso ao menu interativo:

- **(E)mitir** - Emitir nova apólice
- **(R)egistrar Sinistro** - Registrar novo sinistro
- **(C)ancelar** - Cancelar apólice existente
- **(B)uscar** - Buscar por CPF, número de apólice ou nome
- **(G)erar Relatório** - Gerar relatórios e estatísticas
- **(Q)Sair** - Sair do sistema

---

## Exemplos de Uso

### 1. Emitir Nova Apólice
```
Menu: (E)mitir | (R)egistrar Sinistro | (C)ancelar | (B)uscar | (G)erar Relatório | (Q)Sair
Escolha: e

Nome do cliente: João Silva
CPF do cliente: 12345678901
Número da apólice: AP001
Prêmio: 1500.00
Valor segurado: 50000.00
Data emissão (dd/mm/YYYY): 15/09/2025

✅ Apólice AP001 criada com sucesso.
```

### 2. Registrar Sinistro
```
Escolha: r

Número da apólice: AP001
Data abertura (dd/mm/YYYY): 20/09/2025
Descrição: Colisão traseira no estacionamento
Valor (0 se desconhecido): 5000.00

✅ Sinistro registrado.
```

### 3. Buscar Informações
```
Escolha: b

Buscar por CPF / número apólice / nome: João Silva

┏━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━┓
┃ Número  ┃ Cliente    ┃ CPF           ┃ Ativa ┃ Cancelada ┃
┡━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━┩
│ AP001   │ João Silva │ 12345678901   │ True  │ False     │
└─────────┴────────────┴───────────────┴───────┴───────────┘
```

### 4. Gerar Relatório
```
Escolha: g

Mês (1-12): 9
Ano (YYYY): 2025

Receita prevista (total atual): R$ 15.750,00
```

---

## Funcionalidades da Sprint 3

### 🗄️ Persistência com SQLite
- Migração completa de JSON para SQLite
- Camada de acesso a dados (CRUD) robusta
- Rotina de migração automática dos dados da Sprint 2
- Exportação de relatórios em CSV/JSON para backup

### 📋 Auditoria e Logs
- Registro de todas as operações sensíveis
- Logs em arquivo (`logs/app.log`) e console
- Metadados completos: data/hora, usuário, operação, IDs
- Níveis de log: INFO, ERROR, WARNING

### ⚠️ Tratamento de Erros
- Exceções de negócio padronizadas
- Mensagens amigáveis na CLI (sem stack trace)
- Validações reforçadas: CPF, datas, regras de negócio
- Prevenção de operações inválidas

### 📊 Relatórios Avançados
- **Receita mensal prevista** - Soma de prêmios de apólices ativas
- **Top clientes por valor segurado** - Ranking de clientes
- **Sinistros por status e período** - Análise temporal
- **Exportação automática** para pasta `exports/`

### 🖥️ Experiência no Terminal
- Navegação direta com atalhos intuitivos
- Confirmação explícita para ações destrutivas
- Busca rápida por múltiplos critérios
- Fluxos de uso otimizados e claros
- Interface visual com tabelas formatadas

### 🔐 Autenticação Robusta
- Usuários persistidos em SQLite
- Senhas criptografadas com bcrypt
- Sistema de auditoria integrado
- Sessão de usuário ativa em todas as operações

---

## Arquivos de Log e Exports

### Logs do Sistema
- **Localização:** `logs/app.log`
- **Formato:** `[TIMESTAMP] [LEVEL] [USER] - MESSAGE`
- **Rotação:** Automática por tamanho

### Exports de Relatórios
- **Localização:** `exports/`
- **Formatos:** CSV, JSON
- **Nomenclatura:** `relatorio_YYYYMMDD_HHMMSS.csv`

### Banco de Dados
- **Arquivo:** `data/seguros.db`
- **Backup:** Automático antes de migrações
- **Schema:** Criado automaticamente na primeira execução

---

## Executar Testes

```bash
# Todos os testes
python -m pytest tests/ -v

# Teste específico
python -m pytest tests/test_smoke.py -v

# Com cobertura
python -m pytest tests/ --cov=neoroute --cov-report=html
```

---

## Tecnologias Utilizadas

- **Python 3.11+** - Linguagem principal
- **SQLite** - Banco de dados embarcado
- **SQLAlchemy** - ORM para mapeamento objeto-relacional
- **Typer** - Framework para CLI moderna
- **Rich** - Interface visual rica no terminal
- **BCrypt** - Criptografia de senhas
- **Pytest** - Framework de testes
- **Alembic** - Sistema de migrações de banco

---

## Estrutura de Dados

### Tabelas Principais
- **users** - Usuários do sistema
- **clientes** - Dados dos clientes
- **seguros** - Tipos de seguro disponíveis
- **apolices** - Apólices emitidas
- **sinistros** - Sinistros registrados
- **audit_logs** - Log de auditoria completo

### Relacionamentos
- Cliente → Apólices (1:N)
- Apólice → Sinistros (1:N)
- Seguro → Apólices (1:N)
- User → AuditLogs (1:N)

---

## Contribuição

Este projeto foi desenvolvido como parte da **Sprint 3** do curso de Análise e Desenvolvimento de Sistemas da FIAP, focando em persistência robusta, auditoria completa e experiência otimizada no terminal.
