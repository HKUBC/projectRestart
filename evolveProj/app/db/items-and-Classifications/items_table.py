from db.db_setup import sa, connection, metadata

items = sa.Table(
    "items",
    metadata,
    sa.Column("id", sa.Integer(10), primary_key = True),
    sa.Column("price", sa.Float),
    sa.Column("name", sa.String(255)),
    sa.Column("category_id", sa.Integer(10)(), sa.ForeignKey("categories.id")),
    sa.Column("tag", sa.String(20)),
    sa.Column("CreatedAt", sa.DateTime(), default = sa.func.current_timestamp()),
    sa.Column("UdatedAt", sa.DateTime(), onupdate = sa.func.current_timestamp())
)