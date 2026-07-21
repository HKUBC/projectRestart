import sqlalchemy as sa
from app.db.db_setup import metadata

featured_items = sa.Table(
    "featured_items",
    metadata,
    sa.Column("id", sa.Integer, primary_key = True),
    sa.Column("item_id", sa.Integer, sa.ForeignKey("items.id")),
    sa.Column("start_date", sa.DateTime()),
    sa.Column("end_date", sa.DateTime()),
    sa.Column("created_at", sa.DateTime,default = sa.func.current_timestamp(),server_default=sa.func.current_timestamp()),
    sa.Column("updated_at", sa.DateTime,onupdate = sa.func.current_timestamp())
)