import sqlalchemy as sa
from app.db.db_setup import metadata

address = sa.Table(
    "address",
    metadata,
    #sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
    sa.Column("address_line", sa.String(255)),
    sa.Column("suit_number", sa.String(255)),
    sa.Column("phone_number", sa.Integer),
    sa.Column("created_at", sa.DateTime,default = sa.func.current_timestamp(),server_default=sa.func.current_timestamp()),
    sa.Column("updated_at", sa.DateTime,onupdate = sa.func.current_timestamp())
)