import sqlalchemy as sa
from app.db.db_setup import metadata

order_items = sa.Table(
    "order_items",
    metadata,
    sa.Column("order_id",sa.ForeignKey("orders.id"), primary_key=True),
    sa.Column("item_id",sa.ForeignKey("items.id"), primary_key=True),
    sa.Column("quantity",sa.Integer, nullable=False)
)