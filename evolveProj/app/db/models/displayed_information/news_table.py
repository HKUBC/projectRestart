import sqlalchemy as sa
from app.db.db_setup import metadata

news = sa.Table(
    "news",
    metadata,
    sa.Column("title", sa.String(255)),
    sa.Column("content", sa.String(255)),
    sa.Column("created_at", sa.DateTime,default = sa.func.current_timestamp(),server_default=sa.func.current_timestamp()),
    sa.Column("updated_at", sa.DateTime,onupdate = sa.func.current_timestamp())
)