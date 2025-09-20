# Introdução

O projeto **NeoRoute CLI** é um sistema de gestão de seguros, desenvolvido durante a Sprint 3, com foco em **persistência robusta**, **auditoria**, **relatórios detalhados** e **experiência de uso em terminal (CLI)**.  
O sistema utiliza **SQLite** para armazenamento e implementa logs de auditoria, validações reforçadas e fluxos amigáveis para administração de clientes, apólices e sinistros.

---

# Autores

- **AUGUSTO OLIVEIRA CODO DE SOUZA** — RM: 562080  
- **FELIPE DE OLIVEIRA CABRAL** — RM: 561720  
- **JONAS ALAF DA SILVA** — RM: 566479  
- **SOFIA BUERIS NETTO DE SOUZA** — RM: 565818  
- **VINICIUS ADRIAN SIQUEIRA DE OLIVEIRA** — RM: 564962  

---

# Estrutura do Projeto

```
sistema-seguros-sprint3/
│
├── data/
│   └── seguros.db           # Banco de dados SQLite
│
├── scripts/
│   └── relatorios.py        # Script de geração de relatórios
│
├── .venv/                   # Ambiente virtual Python
├── README.md                # Este arquivo
├── requirements.txt         # Bibliotecas Python necessárias
├── exports/                 # Relatórios exportados
├── logs/                    # Arquivos de logs
├── backups/                 # Backups (CSV/JSON)
├── neoroute/                # Módulo principal do sistema
├── tests/                   # Testes automatizados
├── dados/                   # Dados da Sprint 2 (JSON)
├── .env.example             # Exemplo de variáveis de ambiente
└── alembic.ini              # Configuração (opcional) do Alembic
```

---

# Instalação e Configuração

### 1. Criar e ativar o ambiente virtual
python -m venv .venv
.venv\Scripts\Activate.ps1

### 2. Instalar dependências
pip install -r requirements.txt

### 3. Configurar variáveis de ambiente
cp .env.example .env
# Ajuste conforme necessário.

### 4. Criar usuário Admin (via CLI – recomendado)
Crie o usuário admin (idempotente). Use `--force` para resetar a senha se já existir:

```bash
python -m neoroute.cli create-admin --username admin --email admin@neoseguros.com
# Para resetar a senha do admin existente:
python -m neoroute.cli create-admin --username admin --force
```

As credenciais geradas são salvas em `data/initial_admin.txt`.

Alternativa (legado):
```bash
python -m neoroute.create_admin
# Exemplo de usuário criado:
# username: admin
# password: (gerada automaticamente)
```

### 5. Migração de Dados
python -m neoroute.migrate --input dados
# Cria tabelas: clientes, apolices, seguros, sinistros, users, audit_logs
# Popula dados iniciais
# Executar uma única vez

---

# Auditoria e Logs

### Operações registradas
- Criar/editar/cancelar apólices  
- Abrir/fechar sinistros  
- Alterações de cadastro  

### Logs
- Console  
- Arquivo: logs/app.log  

### Informações registradas
- Data/hora  
- Usuário ativo  
- Operação realizada  

---

# Uso da CLI

Você pode rodar a CLI de forma interativa e usar atalhos. Comandos:

1) Iniciar a CLI interativa

```bash
python -m neoroute
# ou
python -m neoroute.cli run
```

2) Fluxos disponíveis no menu (atalhos entre parênteses):

- (E) Emitir apólice
- (R) Registrar sinistro
- (F) Fechar sinistro
- (U) Atualizar cliente
- (C) Cancelar apólice
- (B) Buscar (por CPF, número de apólice ou nome)
- (G) Gerar relatórios rápidos (no terminal)
- (Q) Sair

3) Exemplos práticos

- Emissão de apólice (E)
  - Informe nome e CPF do cliente
  - Número da apólice, prêmio, valor segurado
  - Datas de emissão e vencimento (dd/mm/YYYY)

- Registro de sinistro (R)
  - Informe o número da apólice
  - Data de abertura, descrição e valor

- Fechar sinistro (F)
  - Informe o ID do sinistro
  - Data de fechamento (dd/mm/YYYY)

- Atualizar cliente (U)
  - Informe o CPF e os campos a atualizar (deixe em branco para manter)

4) Relatórios completos (com exportação CSV/JSON):

```bash
python scripts/relatorios.py
```

5) Executar testes automatizados

```bash
python -m pytest tests/ -v
```

---

# Funcionalidades da CLI
- Confirmações para ações destrutivas (ex.: cancelar apólice)  
- Busca rápida por CPF, número de apólice ou nome  

# Regras de Validação
- CPF válido (formato e dígito verificador)  
- Datas coerentes (emissão < vencimento, abertura < fechamento)  
- Não cancelar apólice já cancelada  
- Não fechar sinistro inexistente
- Exceções padronizadas para erros de negócio
- Validação de datas futuras
- Verificação de apólices duplicadas  

# Perfis de Usuário
- Admin: criar/editar/cancelar apólices e sinistros  
- Comum: consultas e relatórios  
- Usuário ativo registrado em todas as entradas de audit_logs