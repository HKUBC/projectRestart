import sqlalchemy as sa
from app.db.db_setup import metadata

faq = sa.Table(
    "faq",
    metadata,
    sa.Column("title", sa.String(255)),
    sa.Column("content", sa.String(255)),
    sa.Column("created_at", sa.DateTime,default = sa.func.current_timestamp(),server_default=sa.func.current_timestamp()),
    sa.Column("UpdatedAt", sa.DateTime, onupdate = sa.func.current_timestamp()),
    sa.Column("deleted_at",sa.DateTime, nullable= True)   
)
