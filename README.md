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
└── alembicini/              # Scripts de migração do banco


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

### 4. Criar usuário Admin
python -m neoroute.create_admin
# Exemplo de usuário criado:
# username: admin
# password: A124Nvu5uuQr1g

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
- Arquivo: logs/audit.log  

### Informações registradas
- Data/hora  
- Usuário ativo  
- Operação realizada  
- Tabela e IDs afetados  

---

# Relatórios

O script scripts/relatorios.py gera os seguintes relatórios:

### 1. Sinistros abertos
| ID  | Cliente        | Data Abertura | Status | Valor |
| --- | -------------- | ------------- | ------ | ----- |
| 3   | Ana Souza      | 2025-08-05    | Aberto | 5000  |
| 1   | Maria Oliveira | 2025-06-10    | Aberto | 8000  |

### 2. Valor total segurado por cliente
| Cliente        | Valor Total |
| -------------- | ----------- |
| Maria Oliveira | 350         |
| Ana Souza      | 250         |
| João da Silva  | 200         |
| Carlos Mendes  | 180         |
| Felipe Cabral  | 150         |

### 3. Sinistros por tipo de seguro
| ID  | Cliente        | Tipo Seguro         | Descrição                                 | Valor |
| --- | -------------- | ------------------ | ----------------------------------------- | ----- |
| 1   | Maria Oliveira | Seguro de Automóvel | Acidente de carro envolvendo terceiros    | 8000  |
| 2   | Felipe Cabral  | Seguro Residencial  | Incêndio parcial em residência            | 15000 |
| 3   | Ana Souza      | Seguro Saúde        | Emergência médica em viagem internacional | 5000  |

### 4. Faturamento de apólices por cliente
| Cliente        | Total Apólices | Total Pago |
| -------------- | -------------- | ---------- |
| Maria Oliveira | 1              | 350        |
| Ana Souza      | 1              | 250        |
| João da Silva  | 1              | 200        |
| Carlos Mendes  | 1              | 180        |
| Felipe Cabral  | 1              | 150        |

### 5. Sinistros por status
| Status  | Total |
| ------- | ----- |
| Aberto  | 2     |
| Fechado | 1     |

---

# Uso da CLI

### Emissão de apólice
python -m neoroute.cli emitir_apolice

### Registro de sinistro
python -m neoroute.cli registrar_sinistro

### Atualização de cadastro
python -m neoroute.cli atualizar_cliente

### Geração de relatórios
python scripts/relatorios.py

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