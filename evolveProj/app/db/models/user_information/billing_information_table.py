import sqlalchemy as sa
from app.db.db_setup import metadata

billingInformation = sa.Table(
    "billigInformation",
    metadata,
    sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
    sa.Column("card_info", sa.Integer)
)