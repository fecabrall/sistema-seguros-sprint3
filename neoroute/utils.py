import re
from datetime import datetime

def only_digits(s):
    return re.sub(r"\D", "", (s or ""))

def validar_cpf(cpf_raw: str) -> bool:
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

def parse_date_ddmmyyyy(s):
    if not s: return None
    for fmt in ["%d/%m/%Y","%Y-%m-%d"]:
        try: return datetime.strptime(s, fmt)
        except: pass
    return None
