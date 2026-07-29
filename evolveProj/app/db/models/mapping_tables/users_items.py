import sqlalchemy as sa
from app.db.db_setup import metadata

item_orders = sa.Table(
    "items_orders",
    metadata,
    sa.Column(sa.ForeignKey("orders.id"), primary_key=True),
    sa.Column(sa.ForeignKey("items.id")),
    sa.Column("quantity",sa.Integer)
)