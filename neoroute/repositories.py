from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from .models import Cliente, Apolice, Seguro, Sinistro

# -------- Clientes --------

def get_or_create_cliente_by_cpf(session: Session, nome: str, cpf: str, email: Optional[str] = None,
                                  telefone: Optional[str] = None, endereco: Optional[str] = None) -> Cliente:
    cliente = session.query(Cliente).filter(Cliente.cpf == cpf).first()
    if cliente:
        return cliente
    cliente = Cliente(nome=nome, cpf=cpf, email=email, telefone=telefone, endereco=endereco)
    session.add(cliente)
    session.commit()
    session.refresh(cliente)
    return cliente


def update_cliente(session: Session, cpf: str, nome: Optional[str] = None, email: Optional[str] = None,
                   telefone: Optional[str] = None, endereco: Optional[str] = None) -> Optional[Cliente]:
    cliente = session.query(Cliente).filter(Cliente.cpf == cpf).first()
    if not cliente:
        return None
    if nome is not None:
        cliente.nome = nome
    if email is not None:
        cliente.email = email
    if telefone is not None:
        cliente.telefone = telefone
    if endereco is not None:
        cliente.endereco = endereco
    session.add(cliente)
    session.commit()
    session.refresh(cliente)
    return cliente


# -------- Seguros --------

def get_or_create_default_seguro(session: Session) -> Seguro:
    seg = session.query(Seguro).first()
    if seg:
        return seg
    seg = Seguro(nome='Padrão')
    session.add(seg)
    session.commit()
    session.refresh(seg)
    return seg


# -------- Apólices --------

def get_apolice_by_numero(session: Session, numero: str) -> Optional[Apolice]:
    return session.query(Apolice).filter(Apolice.numero == numero).first()


def criar_apolice(session: Session, numero: str, cliente_id: int, seguro_id: int, premio: float,
                  valor_seguro: float, data_emissao: datetime, data_vencimento: Optional[datetime]):
    ap = Apolice(
        numero=numero,
        cliente_id=cliente_id,
        seguro_id=seguro_id,
        premio=premio,
        valor_seguro=valor_seguro,
        data_emissao=data_emissao,
        data_vencimento=data_vencimento,
    )
    session.add(ap)
    session.commit()
    session.refresh(ap)
    return ap


def cancelar_apolice(session: Session, ap: Apolice) -> Apolice:
    ap.cancelada = True
    ap.ativa = False
    session.add(ap)
    session.commit()
    session.refresh(ap)
    return ap


# -------- Sinistros --------

def abrir_sinistro(session: Session, apolice_id: int, data_abertura: datetime, descricao: str, valor: float) -> Sinistro:
    sin = Sinistro(
        apolice_id=apolice_id,
        data_abertura=data_abertura,
        status='aberto',
        descricao=descricao,
        valor=valor,
    )
    session.add(sin)
    session.commit()
    session.refresh(sin)
    return sin


def fechar_sinistro(session: Session, sinistro_id: int, data_fechamento: datetime) -> Optional[Sinistro]:
    sin = session.query(Sinistro).filter(Sinistro.id == sinistro_id).first()
    if not sin:
        return None
    sin.data_fechamento = data_fechamento
    sin.status = 'fechado'
    session.add(sin)
    session.commit()
    session.refresh(sin)
    return sin
