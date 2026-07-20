import sqlalchemy as sa
from app.db.db_setup import metadata

categories = sa.Table(
    "categories",
    metadata,
    sa.Column("id", sa.Integer, primary_key = True),
    sa.Column("category", sa.String(255)),
    sa.Column("item_Id", sa.Integer, sa.ForeignKey("items.id")),
    sa.Column("created_at", sa.DateTime,default = sa.func.current_timestamp(),server_default=sa.func.current_timestamp()),
    sa.Column("updated_at", sa.DateTime,onupdate = sa.func.current_timestamp())
)