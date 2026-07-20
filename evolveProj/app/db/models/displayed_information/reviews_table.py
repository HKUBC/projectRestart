import sqlalchemy as sa
from app.db.db_setup import metadata

reviews = sa.Table(
    #
    "reviews",
    metadata,
    sa.Column("id", sa.Integer, primary_key = True),
 #   sa.Column("item_id", sa.Integer, sa.ForeignKey("items.id")),
  #  sa.Column("user_id", sa.Integer,sa.ForeignKey("users.id")),
    sa.Column("content", sa.String(255)),
    sa.Column("created_at", sa.DateTime,default = sa.func.current_timestamp(),server_default=sa.func.current_timestamp()),
    sa.Column("updated_at", sa.DateTime,onupdate = sa.func.current_timestamp())
)