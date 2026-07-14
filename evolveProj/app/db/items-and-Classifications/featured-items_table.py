from db.db_setup import sa, connection, metadata

featured_items = sa.Table(
    "featured_items",
    metadata,
    sa.Column("id", sa.Integer(10), primary_key = True),
    sa.Column("item_id", sa.Integer(10), sa.ForeignKey("items.id")),
    sa.Column("start_date", sa.DateTime()),
    sa.Column("end_date", sa.DateTime()),
    sa.Column("CreatedAt", sa.DateTime(), default = sa.func.current_timestamp()),
    sa.Column("UpdatedAt", sa.DateTime(), onupdate = sa.func.current_timestamp())
)