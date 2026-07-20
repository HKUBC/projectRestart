import sqlalchemy as sa


DATABASE_URL = "postgresql://harrisonkayihura@localhost:5432/proj310"
engine = sa.create_engine(DATABASE_URL)
metadata = sa.MetaData()