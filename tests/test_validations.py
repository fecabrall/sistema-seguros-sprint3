"""
Testes para validações de negócio do sistema de seguros.
"""
import pytest
from datetime import datetime, timedelta
from neoroute.utils import validar_cpf, validar_cpf_ou_erro, validar_datas_apolice, validar_datas_sinistro
from neoroute.exceptions import CpfInvalido, DataInvalida

class TestValidacaoCPF:
    """Testes para validação de CPF."""
    
    def test_cpf_valido(self):
        """Testa CPF válido."""
        assert validar_cpf("11144477735") == True
        assert validar_cpf("111.444.777-35") == True
        assert validar_cpf("111 444 777 35") == True
    
    def test_cpf_invalido(self):
        """Testa CPFs inválidos."""
        assert validar_cpf("12345678901") == False
        assert validar_cpf("11111111111") == False
        assert validar_cpf("00000000000") == False
        assert validar_cpf("") == False
        assert validar_cpf(None) == False
    
    def test_cpf_ou_erro_valido(self):
        """Testa função que lança exceção para CPF inválido."""
        cpf_limpo = validar_cpf_ou_erro("111.444.777-35")
        assert cpf_limpo == "11144477735"
    
    def test_cpf_ou_erro_invalido(self):
        """Testa exceção para CPF inválido."""
        with pytest.raises(CpfInvalido):
            validar_cpf_ou_erro("12345678901")

class TestValidacaoDatas:
    """Testes para validação de datas."""
    
    def test_datas_apolice_validas(self):
        """Testa datas válidas para apólice."""
        hoje = datetime.now()
        ontem = hoje - timedelta(days=1)
        amanha = hoje + timedelta(days=1)
        
        # Não deve lançar exceção
        validar_datas_apolice(ontem, amanha)
        validar_datas_apolice(ontem, None)
    
    def test_datas_apolice_invalidas(self):
        """Testa datas inválidas para apólice."""
        hoje = datetime.now()
        ontem = hoje - timedelta(days=1)
        amanha = hoje + timedelta(days=1)
        
        # Emissão >= vencimento
        with pytest.raises(DataInvalida):
            validar_datas_apolice(amanha, ontem)
        
        # Emissão futura
        with pytest.raises(DataInvalida):
            validar_datas_apolice(amanha, None)
    
    def test_datas_sinistro_validas(self):
        """Testa datas válidas para sinistro."""
        hoje = datetime.now()
        ontem = hoje - timedelta(days=1)
        amanha = hoje + timedelta(days=1)
        
        # Não deve lançar exceção
        validar_datas_sinistro(ontem, amanha)
        validar_datas_sinistro(ontem, None)
    
    def test_datas_sinistro_invalidas(self):
        """Testa datas inválidas para sinistro."""
        hoje = datetime.now()
        ontem = hoje - timedelta(days=1)
        amanha = hoje + timedelta(days=1)
        
        # Abertura >= fechamento
        with pytest.raises(DataInvalida):
            validar_datas_sinistro(amanha, ontem)
        
        # Abertura futura
        with pytest.raises(DataInvalida):
            validar_datas_sinistro(amanha, None)
