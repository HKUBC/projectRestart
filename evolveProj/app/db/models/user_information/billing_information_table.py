import sqlalchemy as sa
from app.db.db_setup import metadata

billingInformation = sa.Table(
    "billigInformation",
    metadata,
    #sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
    #sa.Column("address_line", sa.String(255), sa.ForeignKey("address.address_line")),
    sa.Column("card_info", sa.Integer)
)