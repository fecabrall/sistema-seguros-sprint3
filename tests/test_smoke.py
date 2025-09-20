"""
Testes básicos de smoke para verificar se o sistema está funcionando.
"""
import pytest
from neoroute.db import init_db, get_session
from neoroute.models import Cliente, Apolice, Seguro, Sinistro, User, AuditLog

def test_smoke():
    """Teste básico de smoke."""
    assert True

def test_database_connection():
    """Testa conexão com banco de dados."""
    init_db()
    session = get_session()
    try:
        # Testa se consegue fazer uma query simples
        result = session.query(Cliente).count()
        assert isinstance(result, int)
    finally:
        session.close()

def test_models_exist():
    """Testa se todos os modelos estão definidos."""
    assert Cliente is not None
    assert Apolice is not None
    assert Seguro is not None
    assert Sinistro is not None
    assert User is not None
    assert AuditLog is not None

def test_database_tables():
    """Testa se as tabelas foram criadas."""
    init_db()
    session = get_session()
    try:
        # Verifica se consegue acessar as tabelas
        session.query(Cliente).first()
        session.query(Apolice).first()
        session.query(Seguro).first()
        session.query(Sinistro).first()
        session.query(User).first()
        session.query(AuditLog).first()
    finally:
        session.close()
