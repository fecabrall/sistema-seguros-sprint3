import re
from datetime import datetime
from .exceptions import CpfInvalido, DataInvalida

def only_digits(s):
    return re.sub(r"\D", "", (s or ""))

def validar_cpf(cpf_raw: str) -> bool:
    """Valida CPF e retorna True se válido, False caso contrário."""
    cpf = only_digits(cpf_raw)
    if len(cpf) != 11: return False
    if cpf == cpf[0] * 11: return False
    def calc(cpf_slice, factor):
        total = 0
        for d in cpf_slice:
            total += int(d) * factor; factor -= 1
        resto = (total * 10) % 11
        return 0 if resto == 10 else resto
    d1 = calc(cpf[:9], 10); d2 = calc(cpf[:9] + str(d1), 11)
    return int(cpf[9]) == d1 and int(cpf[10]) == d2

def validar_cpf_ou_erro(cpf_raw: str) -> str:
    """Valida CPF e lança exceção se inválido."""
    if not validar_cpf(cpf_raw):
        raise CpfInvalido(cpf_raw)
    return only_digits(cpf_raw)

def parse_date_ddmmyyyy(s):
    """Converte string de data para datetime."""
    if not s: return None
    for fmt in ["%d/%m/%Y","%Y-%m-%d"]:
        try: return datetime.strptime(s, fmt)
        except: pass
    return None

def validar_datas_apolice(data_emissao: datetime, data_vencimento: datetime = None):
    """Valida se as datas da apólice são coerentes."""
    if data_emissao and data_vencimento:
        if data_emissao >= data_vencimento:
            raise DataInvalida("Data de emissão deve ser anterior à data de vencimento")
    
    if data_emissao and data_emissao > datetime.now():
        raise DataInvalida("Data de emissão não pode ser futura")

def validar_datas_sinistro(data_abertura: datetime, data_fechamento: datetime = None):
    """Valida se as datas do sinistro são coerentes."""
    if data_abertura and data_fechamento:
        if data_abertura >= data_fechamento:
            raise DataInvalida("Data de abertura deve ser anterior à data de fechamento")
    
    if data_abertura and data_abertura > datetime.now():
        raise DataInvalida("Data de abertura não pode ser futura")
