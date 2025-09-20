import secrets
from .db import init_db
from .auth import create_user
from pathlib import Path
from .logger import get_logger
logger = get_logger()

def run(username='admin', email='admin@neoseguros.com', password='admin1234@'):
    init_db()
    try:
        u = create_user(username, password, email=email, role='admin')
        p = Path('data') / 'initial_admin.txt'; p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(f"username={username}\npassword={password}\nemail={email}\n")
        print('ADMIN CRIADO:')
        print('username:', username)
        print('password:', password)
        logger.info(f'admin criado: {username}')
    except Exception as e:
        logger.error(f'erro criar admin: {e}')
        print('erro:', e)

if __name__ == '__main__':
    run()
