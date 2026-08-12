import sqlalchemy as sa
from app.db.db_setup import metadata

payment_system = sa.Table(
    "payment_system",
    metadata,
    sa.Column("id", sa.Integer, primary_key = True),
    sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
    sa.Column("method", sa.String(255)),
    sa.Column("confirmation", sa.Boolean())
)