import sqlalchemy as sa
from app.db.db_setup import metadata


orders = sa.Table(
    "orders",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True ),
    sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"))
)