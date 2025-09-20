import typer
from rich.console import Console
from rich.table import Table
from .db import init_db, get_session
from .auth import authenticate
from .utils import validar_cpf, validar_cpf_ou_erro, parse_date_ddmmyyyy, validar_datas_apolice, validar_datas_sinistro
from .audit import record
from .logger import get_logger
from .models import Cliente, Apolice, Sinistro, Seguro
from .exceptions import (
    CpfInvalido, ApoliceInexistente, ApoliceJaCancelada, SinistroInexistente, 
    OperacaoNaoPermitida, DataInvalida, ClienteInexistente, SeguroInexistente
)
from datetime import datetime
from . import repositories as repo
from pathlib import Path
import secrets
from .auth import create_user, hash_password

console = Console()
app = typer.Typer()
logger = get_logger()

def start_cli(db: str = 'data/seguros.db'):
    """Inicia a sessão CLI interativa simples (login + menu)."""
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
        console.print('\n[bold]Menu:[/bold] (E)mitir (R)egistrar Sinistro (F)echar Sinistro (U)Atualizar Cliente (C)ancelar Apólice (B)uscar (G)erar Relatório (Q)Sair')
        cmd = typer.prompt('Escolha').strip().lower()
        if cmd in ('q','sair'):
            console.print('Saindo...')
            break
        if cmd == 'e':
            try:
                if user.role != 'admin':
                    raise OperacaoNaoPermitida('emitir apólice', user.username)
                
                nome = typer.prompt('Nome do cliente')
                cpf = typer.prompt('CPF do cliente')
                cpf_limpo = validar_cpf_ou_erro(cpf)
                
                session = get_session()
                try:
                    cliente = repo.get_or_create_cliente_by_cpf(session, nome=nome, cpf=cpf_limpo)
                    
                    numero = typer.prompt('Número da apólice')
                    # Verificar se apólice já existe
                    if repo.get_apolice_by_numero(session, numero):
                        console.print('[red]Apólice com este número já existe.[/red]'); continue
                    
                    premio = float(typer.prompt('Prêmio', default='0'))
                    valor_seg = float(typer.prompt('Valor segurado', default='0'))
                    data_em = parse_date_ddmmyyyy(typer.prompt('Data emissão (dd/mm/YYYY)'))
                    data_venc = parse_date_ddmmyyyy(typer.prompt('Data vencimento (dd/mm/YYYY) - opcional', default=''))
                    
                    # Validar datas
                    validar_datas_apolice(data_em, data_venc)
                    
                    seguro = repo.get_or_create_default_seguro(session)
                    
                    ap = repo.criar_apolice(session, numero=numero, cliente_id=cliente.id, seguro_id=seguro.id,
                                             premio=premio, valor_seguro=valor_seg, data_emissao=data_em,
                                             data_vencimento=data_venc)
                    record(user, 'emitir_apolice', 'apolices', ap.numero, {'premio': premio, 'valor_seguro': valor_seg})
                    console.print(f'[green]Apólice {numero} criada com sucesso.[/green]')
                finally:
                    session.close()
            except (CpfInvalido, DataInvalida, OperacaoNaoPermitida) as e:
                console.print(f'[red]Erro: {e}[/red]')
            except Exception as e:
                console.print(f'[red]Erro inesperado: {e}[/red]')
                logger.error(f'Erro ao emitir apólice: {e}')
        elif cmd == 'c':
            try:
                if user.role != 'admin':
                    raise OperacaoNaoPermitida('cancelar apólice', user.username)
                
                numero = typer.prompt('Número da apólice a cancelar')
                session = get_session()
                try:
                    ap = repo.get_apolice_by_numero(session, numero)
                    if not ap:
                        raise ApoliceInexistente(numero)
                    if ap.cancelada:
                        raise ApoliceJaCancelada(numero)
                    
                    confirm = typer.confirm(f'Confirma CANCELAR a apólice {numero}?')
                    if not confirm:
                        console.print('Operação cancelada.'); continue
                    
                    repo.cancelar_apolice(session, ap)
                    record(user, 'cancelar_apolice', 'apolices', ap.numero, {'motivo':'cancelamento pelo usuario'})
                    console.print('[green]Apólice cancelada.[/green]')
                finally:
                    session.close()
            except (ApoliceInexistente, ApoliceJaCancelada, OperacaoNaoPermitida) as e:
                console.print(f'[red]Erro: {e}[/red]')
            except Exception as e:
                console.print(f'[red]Erro inesperado: {e}[/red]')
                logger.error(f'Erro ao cancelar apólice: {e}')
        elif cmd == 'r':
            try:
                numero = typer.prompt('Número da apólice')
                session = get_session()
                try:
                    ap = repo.get_apolice_by_numero(session, numero)
                    if not ap:
                        raise ApoliceInexistente(numero)
                    
                    data_ab = parse_date_ddmmyyyy(typer.prompt('Data abertura (dd/mm/YYYY)'))
                    descricao = typer.prompt('Descrição')
                    valor = float(typer.prompt('Valor (0 se desconhecido)', default='0'))
                    
                    # Validar datas
                    validar_datas_sinistro(data_ab)
                    
                    sin = repo.abrir_sinistro(session, apolice_id=ap.id, data_abertura=data_ab, descricao=descricao, valor=valor)
                    record(user, 'abrir_sinistro', 'sinistros', sin.id, {'valor': valor})
                    console.print('[green]Sinistro registrado.[/green]')
                finally:
                    session.close()
            except (ApoliceInexistente, DataInvalida) as e:
                console.print(f'[red]Erro: {e}[/red]')
            except Exception as e:
                console.print(f'[red]Erro inesperado: {e}[/red]')
                logger.error(f'Erro ao registrar sinistro: {e}')
        elif cmd == 'f':
            # Fechar sinistro
            try:
                session = get_session()
                try:
                    sinistro_id = int(typer.prompt('ID do sinistro a fechar'))
                    sin = session.query(Sinistro).filter(Sinistro.id == sinistro_id).first()
                    if not sin:
                        raise SinistroInexistente(sinistro_id)
                    data_fc = parse_date_ddmmyyyy(typer.prompt('Data fechamento (dd/mm/YYYY)'))
                    # Validar coerência com data de abertura existente
                    validar_datas_sinistro(sin.data_abertura, data_fc)
                    sin = repo.fechar_sinistro(session, sinistro_id, data_fc)
                    record(user, 'fechar_sinistro', 'sinistros', sinistro_id, {'data_fechamento': data_fc.isoformat()})
                    console.print('[green]Sinistro fechado com sucesso.[/green]')
                finally:
                    session.close()
            except (SinistroInexistente, DataInvalida) as e:
                console.print(f'[red]Erro: {e}[/red]')
            except Exception as e:
                console.print(f'[red]Erro inesperado: {e}[/red]')
                logger.error(f'Erro ao fechar sinistro: {e}')
        elif cmd == 'u':
            # Atualizar cadastro de cliente
            try:
                cpf = typer.prompt('CPF do cliente a atualizar')
                cpf_limpo = validar_cpf_ou_erro(cpf)
                nome = typer.prompt('Novo nome (enter para manter)', default='').strip() or None
                email = typer.prompt('Novo email (enter para manter)', default='').strip() or None
                telefone = typer.prompt('Novo telefone (enter para manter)', default='').strip() or None
                endereco = typer.prompt('Novo endereço (enter para manter)', default='').strip() or None
                session = get_session()
                try:
                    cliente = repo.update_cliente(session, cpf=cpf_limpo, nome=nome, email=email, telefone=telefone, endereco=endereco)
                    if not cliente:
                        raise ClienteInexistente(cpf_limpo)
                    record(user, 'atualizar_cliente', 'clientes', cliente.id, {
                        'cpf': cpf_limpo,
                        'nome': nome,
                        'email': email,
                        'telefone': telefone,
                        'endereco': endereco,
                    })
                    console.print('[green]Cliente atualizado com sucesso.[/green]')
                finally:
                    session.close()
            except (CpfInvalido, ClienteInexistente) as e:
                console.print(f'[red]Erro: {e}[/red]')
            except Exception as e:
                console.print(f'[red]Erro inesperado: {e}[/red]')
                logger.error(f'Erro ao atualizar cliente: {e}')
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
            try:
                session = get_session()
                try:
                    from sqlalchemy import func, text
                    
                    # Relatório 1: Receita total prevista
                    total_receita = session.query(func.sum(Apolice.premio)).filter(
                        Apolice.ativa==True, Apolice.cancelada==False
                    ).scalar() or 0
                    
                    # Relatório 2: Top 5 clientes por valor segurado
                    top_clientes = session.query(
                        Cliente.nome, 
                        func.sum(Apolice.valor_seguro).label('valor_total')
                    ).join(Apolice).filter(
                        Apolice.ativa==True, Apolice.cancelada==False
                    ).group_by(Cliente.id, Cliente.nome).order_by(
                        func.sum(Apolice.valor_seguro).desc()
                    ).limit(5).all()
                    
                    # Relatório 3: Sinistros por status
                    sinistros_status = session.query(
                        Sinistro.status, func.count(Sinistro.id).label('total')
                    ).group_by(Sinistro.status).all()
                    
                    # Exibir relatórios
                    console.print('\n[bold blue]📊 RELATÓRIOS RÁPIDOS[/bold blue]')
                    
                    console.print(f'\n[bold]💰 Receita Total Prevista:[/bold] R$ {total_receita:.2f}')
                    
                    if top_clientes:
                        table = Table(title="🏆 Top 5 Clientes por Valor Segurado")
                        table.add_column("Cliente", style="cyan")
                        table.add_column("Valor Segurado (R$)", style="green", justify="right")
                        for cliente, valor in top_clientes:
                            table.add_row(cliente, f"{valor:.2f}")
                        console.print(table)
                    
                    if sinistros_status:
                        table = Table(title="📋 Sinistros por Status")
                        table.add_column("Status", style="yellow")
                        table.add_column("Total", style="red", justify="right")
                        for status, total in sinistros_status:
                            table.add_row(status, str(total))
                        console.print(table)
                    
                    console.print('\n[dim]💡 Para relatórios completos, execute: python scripts/relatorios.py[/dim]')
                    
                finally:
                    session.close()
            except Exception as e:
                console.print(f'[red]Erro ao gerar relatórios: {e}[/red]')
                logger.error(f'Erro ao gerar relatórios: {e}')
        else:
            console.print('[red]Comando não reconhecido.[/red]')

@app.command()
def run(db: str = 'data/seguros.db'):
    """Executa a CLI interativa (atalho de compatibilidade)."""
    start_cli(db=db)

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """Callback principal: inicia a CLI se nenhum subcomando for informado."""
    if ctx.invoked_subcommand is None:
        start_cli()

@app.command('create-admin')
def create_admin_cmd(
    username: str = typer.Option('admin', '--username', '-u', help='Username do admin'),
    email: str = typer.Option('admin@neoseguros.com', '--email', '-e', help='Email do admin'),
    force: bool = typer.Option(False, '--force', '-f', help='Força reset de senha se usuário já existir'),
):
    """Cria (ou reseta) um usuário admin e salva credenciais em data/initial_admin.txt."""
    init_db()
    session = get_session()
    pw = secrets.token_urlsafe(10)
    try:
        # Existe?
        from .models import User
        user = session.query(User).filter(User.username == username).first()
        created = False
        if user and not force:
            console.print(f"[yellow]Usuário '{username}' já existe. Use --force para resetar a senha.[/yellow]")
            return
        if user and force:
            user.password_hash = hash_password(pw)
            user.role = 'admin'
            if email:
                user.email = email
            session.add(user); session.commit(); session.refresh(user)
        if not user:
            user = create_user(username, pw, email=email, role='admin')
            created = True

        # Persistir credenciais em arquivo
        p = Path('data') / 'initial_admin.txt'
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(f"username={username}\npassword={pw}\nemail={email}\n")

        if created:
            console.print('[green]ADMIN CRIADO:[/green]')
        else:
            console.print('[green]ADMIN ATUALIZADO (senha resetada):[/green]')
        console.print(f'username: {username}')
        console.print(f'password: {pw}')
        logger.info(f"admin {'criado' if created else 'resetado'}: {username}")
    except Exception as e:
        session.rollback()
        logger.error(f'erro criar/resetar admin: {e}')
        console.print(f'[red]Erro: {e}[/red]')
    finally:
        session.close()

if __name__ == '__main__':
    app()
