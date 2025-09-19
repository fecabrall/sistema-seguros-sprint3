import typer
from rich.console import Console
from rich.table import Table
from .db import init_db, get_session
from .auth import authenticate
from .utils import validar_cpf, parse_date_ddmmyyyy
from .audit import record
from .logger import get_logger
from .models import Cliente, Apolice, Sinistro, Seguro
from datetime import datetime

console = Console()
app = typer.Typer()
logger = get_logger()

@app.command()
def run(db: str = 'data/seguros.db'):
    """Inicia uma sessão CLI interativa simples."""
    init_db()
    console.print('[bold green]Bem-vindo ao NeoRoute CLI[/bold green]')
    username = typer.prompt('Usuário')
    password = typer.prompt('Senha', hide_input=True)
    user = authenticate(username, password)
    if not user:
        console.print('[red]Usuário ou senha inválidos.[/red]')
        raise typer.Abort()
    console.print(f'[blue]Olá {user.username} (role={user.role})[/blue]')
    while True:
        console.print('\n[bold]Menu:[/bold] (E)mitir (R)egistrar Sinistro (C)ancelar (B)uscar (G)erar Relatório (Q)Sair')
        cmd = typer.prompt('Escolha').strip().lower()
        if cmd in ('q','sair'):
            console.print('Saindo...')
            break
        if cmd == 'e':
            if user.role != 'admin':
                console.print('[red]Apenas admin pode emitir apólices.[/red]'); continue
            nome = typer.prompt('Nome do cliente')
            cpf = typer.prompt('CPF do cliente')
            if not validar_cpf(cpf):
                console.print('[red]CPF inválido.[/red]'); continue
            session = get_session()
            cliente = session.query(Cliente).filter(Cliente.cpf==cpf).first()
            if not cliente:
                cliente = Cliente(nome=nome, cpf=cpf)
                session.add(cliente); session.commit(); session.refresh(cliente)
            numero = typer.prompt('Número da apólice')
            premio = float(typer.prompt('Prêmio', default='0'))
            valor_seg = float(typer.prompt('Valor segurado', default='0'))
            data_em = parse_date_ddmmyyyy(typer.prompt('Data emissão (dd/mm/YYYY)'))
            seguro = session.query(Seguro).first()
            if not seguro:
                seguro = Seguro(nome='Padrão'); session.add(seguro); session.commit()
            ap = Apolice(numero=numero, cliente_id=cliente.id, seguro_id=seguro.id, premio=premio, valor_seguro=valor_seg, data_emissao=data_em)
            session.add(ap); session.commit()
            record(user, 'emitir_apolice', 'apolices', ap.numero, {'premio': premio, 'valor_seguro': valor_seg})
            console.print(f'[green]Apólice {numero} criada com sucesso.[/green]')
        elif cmd == 'c':
            if user.role != 'admin':
                console.print('[red]Apenas admin pode cancelar apólices.[/red]'); continue
            numero = typer.prompt('Número da apólice a cancelar')
            session = get_session()
            ap = session.query(Apolice).filter(Apolice.numero==numero).first()
            if not ap:
                console.print('[red]Apólice não encontrada.[/red]'); continue
            if ap.cancelada:
                console.print('[yellow]Apólice já cancelada.[/yellow]'); continue
            confirm = typer.confirm(f'Confirma CANCELAR a apólice {numero}?')
            if not confirm:
                console.print('Operação cancelada.'); continue
            ap.cancelada = True; ap.ativa = False; session.add(ap); session.commit()
            record(user, 'cancelar_apolice', 'apolices', ap.numero, {'motivo':'cancelamento pelo usuario'})
            console.print('[green]Apólice cancelada.[/green]')
        elif cmd == 'r':
            # registrar sinistro
            numero = typer.prompt('Número da apólice')
            session = get_session()
            ap = session.query(Apolice).filter(Apolice.numero==numero).first()
            if not ap:
                console.print('[red]Apólice não encontrada.[/red]'); continue
            data_ab = parse_date_ddmmyyyy(typer.prompt('Data abertura (dd/mm/YYYY)'))
            descricao = typer.prompt('Descrição')
            valor = float(typer.prompt('Valor (0 se desconhecido)', default='0'))
            sin = Sinistro(apolice_id=ap.id, data_abertura=data_ab, status='aberto', descricao=descricao, valor=valor)
            session.add(sin); session.commit()
            record(user, 'abrir_sinistro', 'sinistros', sin.id, {'valor': valor})
            console.print('[green]Sinistro registrado.[/green]')
        elif cmd == 'b':
            q = typer.prompt('Buscar por CPF / número apólice / nome')
            session = get_session()
            rows = session.query(Apolice).join(Cliente).filter((Cliente.cpf==q)|(Apolice.numero==q)|(Cliente.nome.ilike(f"%{q}%"))).all()
            table = Table(title='Resultados')
            table.add_column('Número'); table.add_column('Cliente'); table.add_column('CPF'); table.add_column('Ativa'); table.add_column('Cancelada')
            for a in rows:
                table.add_row(a.numero, a.cliente.nome, a.cliente.cpf, str(a.ativa), str(a.cancelada))
            console.print(table)
        elif cmd == 'g':
            # relatório simples: receita prevista mês (exemplo)
            mes = int(typer.prompt('Mês (1-12)')); ano = int(typer.prompt('Ano (YYYY)'))
            session = get_session()
            from sqlalchemy import func
            total = session.query(func.sum(Apolice.premio)).filter(Apolice.ativa==True, Apolice.cancelada==False).scalar() or 0
            console.print(f'[bold]Receita prevista (total atual):[/bold] R$ {total:.2f}')
        else:
            console.print('[red]Comando não reconhecido.[/red]')

if __name__ == '__main__':
    app()
