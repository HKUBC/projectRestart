from db.db_setup import sa, metadata

reviews = sa.Table(
    #
    "reviews",
    metadata,
    sa.Column("id", sa.Integer(10), primary_key = True),
    sa.Column("item_id", sa.Integer(10), sa.ForeignKey("items.id")),
    sa.Column("user_id", sa.Integer(10),sa.ForeignKey("users.id")),
    sa.Column("content", sa.String(255)),
    sa.Column("CreatedAt", sa.DateTime()(), default = sa.func.current_timestamp()),
    sa.Column("UpdatedAt", sa.DateTime()(), onupdate = sa.func.current_timestamp())
)