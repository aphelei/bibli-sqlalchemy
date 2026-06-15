from sqlalchemy import create_engine
from contextlib import contextmanager
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from os import getenv


class Base(DeclarativeBase):
    pass


# load_dotenv()

# url = getenv("DB_URL")
# url = "postgresql+psycopg://aphe:@127.0.0.1:5432/bibli"
engine = create_engine("sqlite:///debo.db")
# engine = create_engine(url=url, echo=False)

session_local = sessionmaker(
    autoflush=True,
    bind=engine,
    expire_on_commit=False,  # attention avec les data class !!!
)


def init_db(delete=False):
    if delete:
        Base.metadata.drop_all(bind=engine)
        print("[INFOS] : Table supprimée !!")
    Base.metadata.create_all(bind=engine)
    print("[INFOS] : Table Créee !!")


@contextmanager
def get_db_session():
    """à gérer les ession proprement"""
    session = session_local()
    try:
        yield session
        session.commit()
    except Exception as e:
        print(f"[Erreur] : {e}")
        session.rollback()
    finally:
        session.close()
