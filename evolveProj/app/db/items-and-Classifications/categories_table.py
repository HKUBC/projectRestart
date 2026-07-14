from db.db_setup import sa, connection, metadata

categories = sa.Table(
    "categories",
    metadata,
    sa.Column("id", sa.Integer(10), primary_key = True),
    sa.Column("name", sa.String(255)),
    sa.Column("item_Id", sa.Integer(10), sa.ForeignKey("items.id")),
    sa.Column("CreatedAt", sa.DateTime(), default = sa.func.current_timestamp()),
    sa.Column("UdatedAt", sa.DateTime(), onupdate = sa.func.current_timestamp())
)