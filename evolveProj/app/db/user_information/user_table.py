#from evolveProj.app.db.db_setup import sa, connection, metadata
import sqlalchemy as sa
#Creating db connection and metadata
engine = sa.create_engine("postgresql://harrisonkayihura@localhost:5432/proj310")
connection = engine.connect()
metadata = sa.MetaData()

users = sa.Table(
    "users",
    metadata,
    sa.Column("firstName", sa.String),
    sa.Column("lastName", sa.String),
    sa.Column("email", sa.String),
    sa.Column("id", sa.Integer, primary_key = True),
    sa.Column("password", sa.String),
    sa.Column("CreatedAt", sa.DateTime, default = sa.func.current_timestamp()),
    sa.Column("UdatedAt", sa.DateTime,onupdate = sa.func.current_timestamp())
)