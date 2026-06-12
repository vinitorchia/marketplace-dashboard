import pandas as pd
from sqlalchemy import create_engine, text
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os
import ssl

DATABASE_URL = "postgresql+pg8000://postgres.bcygxizqoamfzuzyiyfh:V1ni.tfs2006%40@aws-1-sa-east-1.pooler.supabase.com:6543/postgres"
PASTA_MONITORADA = r"C:\Vendas"

def get_engine():
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    return create_engine(DATABASE_URL, connect_args={"ssl_context": ssl_context})

def limpar_marketplace(nome):
    if pd.isna(nome):
        return "Desconhecido"
    nome = str(nome)
    if "Mercado Livre" in nome:
        return "Mercado Livre"
    if "Shopee" in nome:
        return "Shopee"
    if "TikTok" in nome or "Tiktok" in nome:
        return "TikTok"
    if "Amazon" in nome:
        return "Amazon"
    return nome.split(" - ")[0].strip()

def calcular_valor_net(row):
    """
    Fórmula: SE(marketplace = Amazon; valor * qtd; valor * 0.85 * qtd)
    Amazon é Vendor — usa valor cheio
    Meli, Shopee, TikTok — aplica 0.85
    """
    if row["marketplace"] == "Amazon":
        return row["valor"] * row["quantidade"]
    else:
        return row["valor"] * 0.85 * row["quantidade"]

def processar_planilha(caminho_arquivo):
    print(f"\n📂 Processando arquivo: {caminho_arquivo}")
    try:
        df = pd.read_excel(caminho_arquivo)
    except Exception as e:
        print(f"❌ Erro ao ler o arquivo: {e}")
        return

    colunas = {
        "Data do pedido": "data",
        "SKU": "sku",
        "Título": "produto",
        "Loja": "marketplace",
        "Valor unitário venda": "valor",
        "Quantidade": "quantidade",
        "Status": "status",
        "Valor total pedido": "valor_total",
    }
    df = df.rename(columns=colunas)

    colunas_necessarias = ["data", "sku", "produto", "marketplace", "valor", "quantidade"]
    faltando = [c for c in colunas_necessarias if c not in df.columns]
    if faltando:
        print(f"❌ Colunas não encontradas: {faltando}")
        return

    df["marketplace"] = df["marketplace"].apply(limpar_marketplace)
    df["data"] = pd.to_datetime(df["data"], dayfirst=True, errors="coerce").dt.date
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce").fillna(0)
    df["quantidade"] = pd.to_numeric(df["quantidade"], errors="coerce").fillna(0).astype(int)
    df["sku"] = df["sku"].astype(str).str.strip()
    df["produto"] = df["produto"].astype(str).str.strip()

    # Calcular valor_net com a fórmula correta
    df["valor_net"] = df.apply(calcular_valor_net, axis=1)

    colunas_banco = ["data", "sku", "produto", "marketplace", "valor", "quantidade", "valor_net"]
    if "status" in df.columns:
        colunas_banco.append("status")
    if "valor_total" in df.columns:
        colunas_banco.append("valor_total")

    df = df[colunas_banco].dropna(subset=["data", "sku"])
    print(f"✅ {len(df)} linhas lidas")

    try:
        engine = get_engine()
        with engine.connect() as conn:
            datas = df["data"].dropna().unique()
            for data in datas:
                conn.execute(text("DELETE FROM vendas WHERE data = :d"), {"d": str(data)})
            conn.commit()
        for i in range(0, len(df), 5000):
            lote = df.iloc[i:i+5000]
            lote.to_sql("vendas", engine, if_exists="append", index=False)
            print(f"✅ Lote {i} a {i+5000} inserido")
        print(f"✅ Dados inseridos com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao salvar no banco: {e}")

class MonitorPlanilha(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith((".xlsx", ".xls", ".csv")):
            time.sleep(2)
            processar_planilha(event.src_path)
    def on_modified(self, event):
        if event.src_path.endswith((".xlsx", ".xls", ".csv")):
            time.sleep(2)
            processar_planilha(event.src_path)

if __name__ == "__main__":
    os.makedirs(PASTA_MONITORADA, exist_ok=True)
    print(f"🚀 ETL iniciado! Monitorando: {PASTA_MONITORADA}")
    print(f"📌 Jogue sua planilha nessa pasta para processar automaticamente.\n")
    observer = Observer()
    observer.schedule(MonitorPlanilha(), path=PASTA_MONITORADA, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
        print("\n⛔ ETL encerrado.")
    observer.join()