import sqlalchemy as sa
from app.db.db_setup import metadata

hot_deals = sa.Table(
    "hot_deals",
    metadata,
    sa.Column("id", sa.Integer, primary_key = True),
    sa.Column("name", sa.String(255)),
    sa.Column("item_id", sa.Integer, sa.ForeignKey("items.id")),
    sa.Column("discount_percentage", sa.Float),
    sa.Column("start_date", sa.DateTime()),
    sa.Column("end_date", sa.DateTime()),
    sa.Column("created_at", sa.DateTime,default = sa.func.current_timestamp(),server_default=sa.func.current_timestamp()),
    sa.Column("updated_at", sa.DateTime,onupdate = sa.func.current_timestamp())
)
