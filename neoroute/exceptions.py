"""
Exceções customizadas para o sistema de seguros.
"""

class SeguroException(Exception):
    """Exceção base para erros de negócio do sistema de seguros."""
    pass

class CpfInvalido(SeguroException):
    """Exceção para CPF inválido."""
    def __init__(self, cpf: str):
        self.cpf = cpf
        super().__init__(f"CPF inválido: {cpf}")

class ApoliceInexistente(SeguroException):
    """Exceção para apólice não encontrada."""
    def __init__(self, numero: str):
        self.numero = numero
        super().__init__(f"Apólice não encontrada: {numero}")

class ApoliceJaCancelada(SeguroException):
    """Exceção para tentativa de cancelar apólice já cancelada."""
    def __init__(self, numero: str):
        self.numero = numero
        super().__init__(f"Apólice {numero} já está cancelada")

class SinistroInexistente(SeguroException):
    """Exceção para sinistro não encontrado."""
    def __init__(self, sinistro_id: int):
        self.sinistro_id = sinistro_id
        super().__init__(f"Sinistro não encontrado: {sinistro_id}")

class OperacaoNaoPermitida(SeguroException):
    """Exceção para operação não permitida para o usuário."""
    def __init__(self, operacao: str, usuario: str):
        self.operacao = operacao
        self.usuario = usuario
        super().__init__(f"Operação '{operacao}' não permitida para usuário '{usuario}'")

class DataInvalida(SeguroException):
    """Exceção para datas inválidas ou incoerentes."""
    def __init__(self, mensagem: str):
        super().__init__(f"Data inválida: {mensagem}")

class ClienteInexistente(SeguroException):
    """Exceção para cliente não encontrado."""
    def __init__(self, cpf: str):
        self.cpf = cpf
        super().__init__(f"Cliente não encontrado: {cpf}")

class SeguroInexistente(SeguroException):
    """Exceção para tipo de seguro não encontrado."""
    def __init__(self, seguro_id: int):
        self.seguro_id = seguro_id
        super().__init__(f"Tipo de seguro não encontrado: {seguro_id}")
