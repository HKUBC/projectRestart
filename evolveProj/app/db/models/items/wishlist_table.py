import sqlalchemy as sa
from app.db.db_setup import metadata

wishlist = sa.Table(
    "wishlist",
    metadata,
    sa.Column("id", sa.Integer, primary_key = True),
   # sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
   # sa.Column("itemLis_id", sa.Integer, sa.ForeignKey("itemList.id")),
    sa.Column("total_price", sa.Float),
    sa.Column("created_at", sa.DateTime,default = sa.func.current_timestamp(),server_default=sa.func.current_timestamp()),
    sa.Column("updated_at", sa.DateTime,onupdate = sa.func.current_timestamp())
)