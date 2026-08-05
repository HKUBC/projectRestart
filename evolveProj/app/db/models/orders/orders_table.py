import sqlalchemy as sa
from app.db.db_setup import metadata


orders = sa.Table(
    "orders",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True ),
    sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
    sa.Column("status", sa.String(8)),
    sa.Column("TimeStamp", sa.DateTime,default = sa.func.current_timestamp(),server_default=sa.func.current_timestamp())
)