from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey, func
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    email = Column(String)
    role = Column(String, nullable=False, default='comum')
    created_at = Column(DateTime, server_default=func.current_timestamp())

class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False, index=True)
    email = Column(String)
    telefone = Column(String)
    endereco = Column(Text)
    created_at = Column(DateTime, server_default=func.current_timestamp())
    apolices = relationship('Apolice', back_populates='cliente', cascade='all, delete-orphan')

class Seguro(Base):
    __tablename__ = 'seguros'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    descricao = Column(Text)
    created_at = Column(DateTime, server_default=func.current_timestamp())
    apolices = relationship('Apolice', back_populates='seguro')

class Apolice(Base):
    __tablename__ = 'apolices'
    id = Column(Integer, primary_key=True)
    numero = Column(String, unique=True, nullable=False, index=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    seguro_id = Column(Integer, ForeignKey('seguros.id'), nullable=False)
    premio = Column(Float, nullable=False)
    valor_seguro = Column(Float, nullable=False)
    data_emissao = Column(DateTime, nullable=False)
    data_vencimento = Column(DateTime)
    ativa = Column(Boolean, default=True)
    cancelada = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.current_timestamp())

    cliente = relationship('Cliente', back_populates='apolices')
    seguro = relationship('Seguro', back_populates='apolices')
    sinistros = relationship('Sinistro', back_populates='apolice', cascade='all, delete-orphan')

class Sinistro(Base):
    __tablename__ = 'sinistros'
    id = Column(Integer, primary_key=True)
    apolice_id = Column(Integer, ForeignKey('apolices.id'), nullable=False)
    data_abertura = Column(DateTime, nullable=False)
    data_fechamento = Column(DateTime)
    status = Column(String, nullable=False)
    descricao = Column(Text)
    valor = Column(Float)
    created_at = Column(DateTime, server_default=func.current_timestamp())

    apolice = relationship('Apolice', back_populates='sinistros')

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    username = Column(String)
    operation = Column(String, nullable=False)
    table_name = Column(String)
    entity_id = Column(String)
    details = Column(Text)
    created_at = Column(DateTime, server_default=func.current_timestamp())
