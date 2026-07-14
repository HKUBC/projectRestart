from db.db_setup import sa, connection, metadata

wishlist = sa.Table(
    "wishlist",
    metadata,
    sa.Column("id", sa.Integer(10), primary_key = True),
    sa.Column("user_id", sa.Integer(10), sa.ForeignKey("users.id")),
    sa.Column("itemLis_id", sa.Integer(10), sa.ForeignKey("itemList.id")),
    sa.Column("total_price", sa.Float),
    sa.Column("CreatedAt", sa.DateTime()(), default = sa.func.current_timestamp()),
    sa.Column("UpdatedAt", sa.DateTime()(), onupdate = sa.func.current_timestamp())
)