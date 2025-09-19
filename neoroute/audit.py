import json
from .db import get_session
from .models import AuditLog
from .logger import get_logger
logger = get_logger()

def record(user, operation, table_name=None, entity_id=None, details=None):
    session = get_session()
    try:
        d = json.dumps(details, ensure_ascii=False) if details is not None else None
        log = AuditLog(user_id=(user.id if user else None), username=(user.username if user else None),
                       operation=operation, table_name=table_name, entity_id=str(entity_id) if entity_id else None,
                       details=d)
        session.add(log); session.commit()
        logger.info(f"AUDIT user={(user.username if user else 'anon')} op={operation} table={table_name} id={entity_id}")
    except Exception as e:
        session.rollback(); logger.error(f"falha audit: {e}")
    finally:
        session.close()
