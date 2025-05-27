from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .logger_conf import logger

DATABASE_URL = ""

engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        logger.critical(f"Database Error: {e}")
    finally:
        db.close()
