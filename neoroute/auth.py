import bcrypt
from sqlalchemy.exc import IntegrityError
from .db import get_session
from .models import User

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, pw_hash: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode('utf-8'), pw_hash.encode('utf-8'))
    except Exception:
        return False

def create_user(username, password, email=None, role='comum'):
    session = get_session()
    try:
        user = User(username=username, password_hash=hash_password(password), email=email, role=role)
        session.add(user); session.commit(); session.refresh(user)
        return user
    except IntegrityError:
        session.rollback()
        raise
    finally:
        session.close()

def authenticate(username, password):
    session = get_session()
    try:
        user = session.query(User).filter(User.username==username).first()
        if not user: return None
        if verify_password(password, user.password_hash):
            return user
        return None
    finally:
        session.close()
