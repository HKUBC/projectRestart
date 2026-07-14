from db.db_setup import sa, metadata

payment_system = sa.Table(
    "payment_system",
    metadata,
    sa.Column("id", sa.Integer(10), primary_key = True),
    sa.Column("user_id", sa.Integer(10), sa.ForeignKey("users.id")),
    sa.Colum("method", sa.String(255)),
    sa.Column("confirmation", sa.Boolean())
)