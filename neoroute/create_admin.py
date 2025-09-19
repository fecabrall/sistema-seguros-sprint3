import secrets
from .db import init_db
from .auth import create_user
from pathlib import Path
from .logger import get_logger
logger = get_logger()

def run(username='admin', email='admin@neoseguros.com'):
    init_db()
    pw = secrets.token_urlsafe(10)
    try:
        u = create_user(username, pw, email=email, role='admin')
        p = Path('data') / 'initial_admin.txt'; p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(f"username={username}\npassword={pw}\nemail={email}\n")
        print('ADMIN CRIADO:')
        print('username:', username)
        print('password:', pw)
        logger.info(f'admin criado: {username}')
    except Exception as e:
        logger.error(f'erro criar admin: {e}')
        print('erro:', e)

if __name__ == '__main__':
    run()
