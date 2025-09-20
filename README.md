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
├── scripts/                 # Scripts auxiliares
│   └── relatorios.py        # Relatórios completos (export CSV/JSON)
├── data/                    # Dados persistidos
│   ├── seguros.db           # Banco de dados SQLite
│   └── initial_admin.txt    # Últimas credenciais geradas do admin
├── dados/                   # Dados da Sprint 2 (JSON) para migração one-shot
│   ├── clientes.json
│   ├── apolices.json
│   ├── seguros.json
│   └── sinistros.json
├── exports/                 # Relatórios exportados (CSV/JSON)
├── logs/                    # Arquivos de logs (app.log)
├── backups/                 # Backups automáticos do banco
├── tests/                   # Testes automatizados
├── requirements.txt         # Dependências Python
├── .env.example             # Exemplo de variáveis de ambiente
└── alembic.ini              # Configuração (opcional) do Alembic
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

Você pode rodar a CLI de forma interativa e usar atalhos.

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

3) Relatórios completos (com exportação CSV/JSON):

```bash
python scripts/relatorios.py
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

# Perfis de Usuário
- Admin: criar/editar/cancelar apólices e sinistros  
- Comum: consultas e relatórios  
- Usuário ativo registrado em todas as entradas de audit_logs