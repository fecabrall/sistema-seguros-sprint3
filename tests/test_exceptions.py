"""
Testes para exceções customizadas do sistema de seguros.
"""
import pytest
from neoroute.exceptions import (
    CpfInvalido, ApoliceInexistente, ApoliceJaCancelada, SinistroInexistente,
    OperacaoNaoPermitida, DataInvalida, ClienteInexistente, SeguroInexistente
)

class TestExcecoes:
    """Testes para exceções customizadas."""
    
    def test_cpf_invalido(self):
        """Testa exceção CpfInvalido."""
        cpf = "12345678901"
        exc = CpfInvalido(cpf)
        assert exc.cpf == cpf
        assert str(exc) == f"CPF inválido: {cpf}"
    
    def test_apolice_inexistente(self):
        """Testa exceção ApoliceInexistente."""
        numero = "APO123"
        exc = ApoliceInexistente(numero)
        assert exc.numero == numero
        assert str(exc) == f"Apólice não encontrada: {numero}"
    
    def test_apolice_ja_cancelada(self):
        """Testa exceção ApoliceJaCancelada."""
        numero = "APO123"
        exc = ApoliceJaCancelada(numero)
        assert exc.numero == numero
        assert str(exc) == f"Apólice {numero} já está cancelada"
    
    def test_sinistro_inexistente(self):
        """Testa exceção SinistroInexistente."""
        sinistro_id = 123
        exc = SinistroInexistente(sinistro_id)
        assert exc.sinistro_id == sinistro_id
        assert str(exc) == f"Sinistro não encontrado: {sinistro_id}"
    
    def test_operacao_nao_permitida(self):
        """Testa exceção OperacaoNaoPermitida."""
        operacao = "emitir apólice"
        usuario = "usuario_comum"
        exc = OperacaoNaoPermitida(operacao, usuario)
        assert exc.operacao == operacao
        assert exc.usuario == usuario
        assert str(exc) == f"Operação '{operacao}' não permitida para usuário '{usuario}'"
    
    def test_data_invalida(self):
        """Testa exceção DataInvalida."""
        mensagem = "Data de emissão deve ser anterior à data de vencimento"
        exc = DataInvalida(mensagem)
        assert str(exc) == f"Data inválida: {mensagem}"
    
    def test_cliente_inexistente(self):
        """Testa exceção ClienteInexistente."""
        cpf = "12345678901"
        exc = ClienteInexistente(cpf)
        assert exc.cpf == cpf
        assert str(exc) == f"Cliente não encontrado: {cpf}"
    
    def test_seguro_inexistente(self):
        """Testa exceção SeguroInexistente."""
        seguro_id = 456
        exc = SeguroInexistente(seguro_id)
        assert exc.seguro_id == seguro_id
        assert str(exc) == f"Tipo de seguro não encontrado: {seguro_id}"
