

import sqlite3
import os
from tabulate import tabulate

# Conectar no banco de dados
db_path = os.path.join(os.path.dirname(__file__), "../data/seguros.db")
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Função para executar query e imprimir tabela
def print_relatorio(titulo, query, headers=None):
    print(f"\n=== {titulo} ===")
    cur.execute(query)
    rows = cur.fetchall()
    if rows:
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    else:
        print("Nenhum registro encontrado.")

# ========================
# RELATÓRIO 1: Sinistros abertos
# ========================
print_relatorio(
    "RELATÓRIO 1: Sinistros abertos",
    """
    SELECT s.id, cl.nome, s.data_abertura, s.status, s.valor
    FROM sinistros s
    JOIN apolices a ON s.apolice_id = a.id
    JOIN clientes cl ON a.cliente_id = cl.id
    WHERE s.status = 'Aberto'
    ORDER BY s.data_abertura DESC
    """,
    headers=["ID", "Cliente", "Data Abertura", "Status", "Valor"]
)

# ========================
# RELATÓRIO 2: Valor total segurado por cliente
# ========================
print_relatorio(
    "RELATÓRIO 2: Valor total segurado por cliente",
    """
    SELECT c.nome, SUM(a.premio) AS valor_total
    FROM apolices a
    JOIN clientes c ON a.cliente_id = c.id
    GROUP BY c.nome
    ORDER BY valor_total DESC
    """,
    headers=["Cliente", "Valor Total"]
)

# ========================
# RELATÓRIO 3: Sinistros por tipo de cobertura
# ========================
print_relatorio(
    "RELATÓRIO 3: Sinistros por tipo de cobertura",
    """
    SELECT s.id, cl.nome, se.nome, s.descricao, s.valor
    FROM sinistros s
    JOIN apolices a ON s.apolice_id = a.id
    JOIN clientes cl ON a.cliente_id = cl.id
    JOIN seguros se ON a.seguro_id = se.id
    """,
    headers=["ID", "Cliente", "Tipo Seguro", "Descrição", "Valor"]
)

# ========================
# RELATÓRIO 4: Faturamento de apólices por cliente
# ========================
print_relatorio(
    "RELATÓRIO 4: Faturamento de apólices por cliente",
    """
    SELECT c.nome, COUNT(a.id) AS total_apolices, SUM(a.premio) AS total_pago
    FROM apolices a
    JOIN clientes c ON a.cliente_id = c.id
    GROUP BY c.nome
    ORDER BY total_pago DESC
    """,
    headers=["Cliente", "Total Apólices", "Total Pago"]
)

# ========================
# RELATÓRIO 5: Sinistros por status
# ========================
print_relatorio(
    "RELATÓRIO 5: Sinistros por status",
    """
    SELECT status, COUNT(*) AS total
    FROM sinistros
    GROUP BY status
    ORDER BY total DESC
    """,
    headers=["Status", "Total"]
)

# Fechar conexão
conn.close()
