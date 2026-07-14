from db.db_setup import sa, connection, metadata

# ? maybe not can be combined with wishlist, but called by different methods
orders = sa.Table(
    "orders",
    metadata,
    sa.Column("id", sa.Integer(10), primary_key = True),
    sa.Column("user_id", sa.Integer(10), sa.ForeignKey("users.id")),
    sa.Column("item_id", sa.Integer(10), sa.ForeignKey("items.id")),
    sa.Column("Quantity", sa.Integer(10)),
    sa.Column("CreatedAt", sa.DateTime(), default = sa.func.current_timestamp()),
    sa.Column("UpdatedAt", sa.DateTime(), onupdate = sa.func.current_timestamp())
)