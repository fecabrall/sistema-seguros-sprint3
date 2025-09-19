import os, json, shutil, argparse
from .db import init_db, get_session
from .models import Cliente, Seguro, Apolice, Sinistro
from .utils import parse_date_ddmmyyyy
from .logger import get_logger
from datetime import datetime

logger = get_logger()

def backup_db(path='data/seguros.db'):
    if os.path.exists(path):
        bak_dir = os.path.join('backups')
        os.makedirs(bak_dir, exist_ok=True)
        ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
        dst = os.path.join(bak_dir, f"{os.path.basename(path)}.{ts}.bak")
        shutil.copy2(path, dst)
        logger.info(f"backup criado: {dst}")
        return dst
    return None

def import_jsons(input_dir='dados'):
    session = get_session()
    try:
        files = {
            'clientes': os.path.join(input_dir, 'clientes.json'),
            'seguros': os.path.join(input_dir, 'seguros.json'),
            'apolices': os.path.join(input_dir, 'apolices.json'),
            'sinistros': os.path.join(input_dir, 'sinistros.json')
        }

        # === Importar clientes ===
        if os.path.exists(files['clientes']):
            with open(files['clientes'], encoding='utf-8') as f:
                data = json.load(f)
            for c in data:
                cpf = c.get('cpf')
                if not cpf:
                    continue
                if session.query(Cliente).filter(Cliente.cpf == cpf).first():
                    continue
                cliente = Cliente(
                    nome=c.get('nome', 'desconhecido'),
                    cpf=cpf,
                    email=c.get('email'),
                    telefone=c.get('telefone'),
                    endereco=c.get('endereco')
                )
                session.add(cliente)
            session.commit()

        # === Importar seguros ===
        if os.path.exists(files['seguros']):
            with open(files['seguros'], encoding='utf-8') as f:
                data = json.load(f)
            for s in data:
                # Montar nome/descricao se não existirem no JSON
                nome = s.get("nome") or (s.get("tipo", "desconhecido").capitalize())
                descricao = s.get("descricao") or f"Seguro {s.get('tipo', 'genérico')} - valor {s.get('valor_base', 'não informado')}"
                # Evitar duplicado
                if session.query(Seguro).filter(Seguro.nome == nome).first():
                    continue
                session.add(Seguro(nome=nome, descricao=descricao))
            session.commit()

        # === Importar apólices ===
        if os.path.exists(files['apolices']):
            with open(files['apolices'], encoding='utf-8') as f:
                data = json.load(f)
            for a in data:
                num = a.get('numero')
                if not num:
                    continue
                if session.query(Apolice).filter(Apolice.numero == num).first():
                    continue
                cpf = a.get('cpf') or a.get('cpf_cliente') or a.get('cliente_cpf')
                cliente = session.query(Cliente).filter(Cliente.cpf == cpf).first()
                if not cliente:
                    cliente = Cliente(nome=a.get('nome_cliente', 'desconhecido'), cpf=cpf)
                    session.add(cliente)
                    session.commit()
                seguro = session.query(Seguro).first()
                data_em = parse_date_ddmmyyyy(a.get('data_emissao')) or datetime.utcnow()
                data_v = parse_date_ddmmyyyy(a.get('data_vencimento'))
                ap = Apolice(
                    numero=num,
                    cliente_id=cliente.id,
                    seguro_id=(seguro.id if seguro else None),
                    premio=float(a.get('premio') or 0),
                    valor_seguro=float(a.get('valor_seguro') or 0),
                    data_emissao=data_em,
                    data_vencimento=data_v
                )
                session.add(ap)
            session.commit()

        # === Importar sinistros ===
        if os.path.exists(files['sinistros']):
            with open(files['sinistros'], encoding='utf-8') as f:
                data = json.load(f)
            for s in data:
                num = s.get('numero_apolice') or s.get('apolice_numero')
                ap = session.query(Apolice).filter(Apolice.numero == num).first()
                if not ap:
                    continue
                data_ab = parse_date_ddmmyyyy(s.get('data_abertura') or s.get('data')) or datetime.utcnow()
                data_fc = parse_date_ddmmyyyy(s.get('data_fechamento'))
                sin = Sinistro(
                    apolice_id=ap.id,
                    data_abertura=data_ab,
                    data_fechamento=data_fc,
                    status=s.get('status', 'aberto'),
                    descricao=s.get('descricao'),
                    valor=s.get('valor')
                )
                session.add(sin)
            session.commit()

        logger.info('import ok')
    except Exception as e:
        session.rollback()
        logger.error(f'import falhou: {e}')
    finally:
        session.close()

def run(input_dir='dados'):
    init_db()
    backup_db()
    import_jsons(input_dir)
    print('Migração finalizada.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='dados')
    args = parser.parse_args()
    run(input_dir=args.input)
