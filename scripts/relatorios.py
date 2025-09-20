
import sqlite3
import os
import csv
import json
from datetime import datetime
from tabulate import tabulate

# Conectar no banco de dados
db_path = os.path.join(os.path.dirname(__file__), "../data/seguros.db")
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Criar diretório de exports se não existir
exports_dir = os.path.join(os.path.dirname(__file__), "../exports")
os.makedirs(exports_dir, exist_ok=True)

def print_relatorio(titulo, query, headers=None, export_csv=True, export_json=True):
    """Executa query e exibe relatório, opcionalmente exportando para CSV/JSON."""
    print(f"\n=== {titulo} ===")
    cur.execute(query)
    rows = cur.fetchall()
    
    if rows:
        print(tabulate(rows, headers=headers, tablefmt="grid"))
        
        # Exportar para CSV
        if export_csv:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{titulo.lower().replace(' ', '_').replace(':', '')}_{timestamp}.csv"
            csv_path = os.path.join(exports_dir, filename)
            
            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                if headers:
                    writer.writerow(headers)
                writer.writerows(rows)
            print(f"📄 Exportado para CSV: {csv_path}")
        
        # Exportar para JSON
        if export_json:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{titulo.lower().replace(' ', '_').replace(':', '')}_{timestamp}.json"
            json_path = os.path.join(exports_dir, filename)
            
            data = {
                "titulo": titulo,
                "data_geracao": datetime.now().isoformat(),
                "total_registros": len(rows),
                "dados": []
            }
            
            for row in rows:
                if headers:
                    data["dados"].append(dict(zip(headers, row)))
                else:
                    data["dados"].append(row)
            
            with open(json_path, 'w', encoding='utf-8') as jsonfile:
                json.dump(data, jsonfile, ensure_ascii=False, indent=2)
            print(f"📄 Exportado para JSON: {json_path}")
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
    WHERE s.status = 'aberto'
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

# ========================
# RELATÓRIO 6: Receita mensal prevista (novo)
# ========================
print_relatorio(
    "RELATÓRIO 6: Receita mensal prevista",
    """
    SELECT 
        strftime('%Y-%m', data_emissao) AS mes_ano,
        COUNT(*) AS total_apolices,
        SUM(premio) AS receita_prevista
    FROM apolices 
    WHERE ativa = 1 AND cancelada = 0
    GROUP BY strftime('%Y-%m', data_emissao)
    ORDER BY mes_ano DESC
    """,
    headers=["Mês/Ano", "Total Apólices", "Receita Prevista (R$)"]
)

# ========================
# RELATÓRIO 7: Top clientes por valor segurado (novo)
# ========================
print_relatorio(
    "RELATÓRIO 7: Top clientes por valor segurado",
    """
    SELECT 
        c.nome,
        COUNT(a.id) AS total_apolices,
        SUM(a.valor_seguro) AS valor_total_segurado,
        SUM(a.premio) AS total_premios
    FROM clientes c
    JOIN apolices a ON c.id = a.cliente_id
    WHERE a.ativa = 1 AND a.cancelada = 0
    GROUP BY c.id, c.nome
    ORDER BY valor_total_segurado DESC
    LIMIT 10
    """,
    headers=["Cliente", "Total Apólices", "Valor Segurado (R$)", "Total Prêmios (R$)"]
)

# ========================
# RELATÓRIO 8: Sinistros por período (novo)
# ========================
print_relatorio(
    "RELATÓRIO 8: Sinistros por período",
    """
    SELECT 
        strftime('%Y-%m', data_abertura) AS periodo,
        COUNT(*) AS total_sinistros,
        SUM(valor) AS valor_total,
        AVG(valor) AS valor_medio
    FROM sinistros
    GROUP BY strftime('%Y-%m', data_abertura)
    ORDER BY periodo DESC
    """,
    headers=["Período", "Total Sinistros", "Valor Total (R$)", "Valor Médio (R$)"]
)

# ========================
# RELATÓRIO 9: Apólices vencidas (novo)
# ========================
print_relatorio(
    "RELATÓRIO 9: Apólices vencidas",
    """
    SELECT 
        a.numero,
        c.nome,
        a.data_vencimento,
        a.premio,
        a.valor_seguro,
        CASE 
            WHEN a.cancelada = 1 THEN 'Cancelada'
            WHEN a.ativa = 0 THEN 'Inativa'
            ELSE 'Ativa'
        END AS status
    FROM apolices a
    JOIN clientes c ON a.cliente_id = c.id
    WHERE a.data_vencimento < date('now')
    ORDER BY a.data_vencimento DESC
    """,
    headers=["Número", "Cliente", "Data Vencimento", "Prêmio (R$)", "Valor Segurado (R$)", "Status"]
)

# ========================
# RELATÓRIO 10: Resumo geral do sistema (novo)
# ========================
print_relatorio(
    "RELATÓRIO 10: Resumo geral do sistema",
    """
    SELECT 
        'Clientes' AS categoria,
        COUNT(*) AS total
    FROM clientes
    UNION ALL
    SELECT 
        'Apólices Ativas' AS categoria,
        COUNT(*) AS total
    FROM apolices 
    WHERE ativa = 1 AND cancelada = 0
    UNION ALL
    SELECT 
        'Sinistros Abertos' AS categoria,
        COUNT(*) AS total
    FROM sinistros 
    WHERE status = 'aberto'
    UNION ALL
    SELECT 
        'Receita Total Prevista' AS categoria,
        SUM(premio) AS total
    FROM apolices 
    WHERE ativa = 1 AND cancelada = 0
    """,
    headers=["Categoria", "Total"]
)

print(f"\n🎉 Todos os relatórios foram gerados e exportados para: {exports_dir}")

# Fechar conexão
conn.close()
