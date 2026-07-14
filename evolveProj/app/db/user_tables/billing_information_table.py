from db.db_setup import sa, connection, metadata

billingInformation = sa.Table(
    "billigInformation",
    metadata,
    sa.Column("user_id", sa.Integer(10), sa.ForeignKey("users.id")),
    sa.Column("address_line", sa.String(255), sa.ForeignKey("address.address_line")),
    sa.Column("card_info", sa.Integer(10))
)