import sqlalchemy as sa
from app.db.db_setup import metadata

users = sa.Table(
    "users",
    metadata,
    sa.Column("firstname", sa.String(255), nullable = False),
    sa.Column("lastname", sa.String(255), nullable = False),
    sa.Column("email", sa.String(255), nullable = False),
    sa.Column("id", sa.Integer, primary_key = True),
    sa.Column("password", sa.String(255), nullable = False),
    sa.Column("created_at", sa.DateTime,default = sa.func.current_timestamp(),server_default=sa.func.current_timestamp()),
    sa.Column("updated_at", sa.DateTime,onupdate = sa.func.current_timestamp()),
    sa.Column("deleted_at",sa.DateTime, nullable= True)
)