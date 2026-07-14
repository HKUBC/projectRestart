from db.db_setup import sa, connection, metadata

itemList = sa.Table(
    "itemList",
    metadata,
    sa.Column("id", sa.Integer(10), primary_key = True),
    sa.Column("item_id", sa.Integer(10), sa.ForeignKey("items.id")),
    sa.Column("price", sa.Float),
    sa.Column("quantity", sa.Integer(10))
)