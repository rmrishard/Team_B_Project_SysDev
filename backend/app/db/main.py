from sqlalchemy import create_engine
from ..config.settings import settings

def setup_engine():
    db_url = f"{settings.db_driver}://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
    return create_engine(
        url=db_url,
        echo=True
    )