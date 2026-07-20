import sqlalchemy as sa
from app.db.db_setup import metadata

itemList = sa.Table(
    "itemList",
    metadata,
    sa.Column("id", sa.Integer, primary_key = True),
    sa.Column("item_id", sa.Integer, sa.ForeignKey("items.id")),
    sa.Column("price", sa.Float),
    sa.Column("quantity", sa.Integer)
)