import sqlalchemy as sa
from app.db.db_setup import metadata

items = sa.Table(
    "items",
    metadata,
    sa.Column("id", sa.Integer, primary_key = True),
    sa.Column("price", sa.Float),
    sa.Column("name", sa.String(255)),
    sa.Column("category_id", sa.Integer, sa.ForeignKey("categories.id")),
    sa.Column("tag", sa.String(20)),
    sa.Column("created_at", sa.DateTime,default = sa.func.current_timestamp(),server_default=sa.func.current_timestamp()),
    sa.Column("updated_at", sa.DateTime,onupdate = sa.func.current_timestamp()),
    sa.Column("deleted_at",sa.DateTime, nullable= True)
)