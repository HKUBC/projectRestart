import sqlalchemy as sa
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DATABASE_URL = "postgresql://harrisonkayihura@localhost:5432/proj310"
engine = sa.create_engine(DATABASE_URL)
metadata = sa.MetaData()


LocalSession = sessionmaker[Session](autocommit = False, autoflush = False, bind = engine )
Base = declarative_base()
def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

