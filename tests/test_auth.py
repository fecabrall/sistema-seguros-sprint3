"""
Testes para autenticação e autorização.
"""
import pytest
import time
from neoroute.auth import hash_password, verify_password, create_user, authenticate
from neoroute.db import get_session, init_db
from neoroute.models import User
from sqlalchemy.exc import IntegrityError

class TestAutenticacao:
    """Testes para sistema de autenticação."""
    
    def test_hash_password(self):
        """Testa hash de senha."""
        password = "senha123"
        hashed = hash_password(password)
        
        assert hashed != password
        assert len(hashed) > 0
        assert hashed.startswith("$2b$")
    
    def test_verify_password_correto(self):
        """Testa verificação de senha correta."""
        password = "senha123"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) == True
    
    def test_verify_password_incorreto(self):
        """Testa verificação de senha incorreta."""
        password = "senha123"
        hashed = hash_password(password)
        
        assert verify_password("senha_errada", hashed) == False
        assert verify_password("", hashed) == False
        assert verify_password(password, "hash_invalido") == False
    
    def test_create_user(self):
        """Testa criação de usuário."""
        # Limpar banco antes do teste
        init_db()
        
        timestamp = str(int(time.time() * 1000))
        username = f"testuser_create_{timestamp}"
        
        user = create_user(username, "senha123", "test@email.com", "comum")
        
        assert user.username == username
        assert user.email == "test@email.com"
        assert user.role == "comum"
        assert user.password_hash != "senha123"
        assert verify_password("senha123", user.password_hash)
    
    def test_create_user_duplicado(self):
        """Testa criação de usuário duplicado."""
        init_db()
        
        timestamp = str(int(time.time() * 1000))
        username = f"testuser_dup_{timestamp}"
        
        # Criar primeiro usuário
        create_user(username, "senha123")
        
        # Tentar criar usuário com mesmo username
        with pytest.raises(IntegrityError):
            create_user(username, "outra_senha")
    
    def test_authenticate_usuario_valido(self):
        """Testa autenticação de usuário válido."""
        init_db()
        
        timestamp = str(int(time.time() * 1000))
        username = f"testuser_auth_{timestamp}"
        
        # Criar usuário
        create_user(username, "senha123", role="admin")
        
        # Autenticar
        user = authenticate(username, "senha123")
        
        assert user is not None
        assert user.username == username
        assert user.role == "admin"
    
    def test_authenticate_usuario_inexistente(self):
        """Testa autenticação de usuário inexistente."""
        init_db()
        
        user = authenticate("usuario_inexistente", "senha123")
        assert user is None
    
    def test_authenticate_senha_incorreta(self):
        """Testa autenticação com senha incorreta."""
        init_db()
        
        timestamp = str(int(time.time() * 1000))
        username = f"testuser_senha_{timestamp}"
        
        # Criar usuário
        create_user(username, "senha123")
        
        # Tentar autenticar com senha errada
        user = authenticate(username, "senha_errada")
        assert user is None
