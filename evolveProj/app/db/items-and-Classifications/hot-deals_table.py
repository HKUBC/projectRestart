from db.db_setup import sa, connection, metadata

hot_deals = sa.Table(
    "hot_deals",
    metadata,
    sa.Column("id", sa.Integer(10), primary_key = True),
    sa.Column("name", sa.String(255)),
    sa.Column("item_id", sa.Integer(10), sa.ForeignKey("items.id")),
    sa.Column("discount_percentage", sa.Float),
    sa.Column("start_date", sa.DateTime()),
    sa.Column("end_date", sa.DateTime()()),
    sa.Column("CreatedAt", sa.DateTime()(), default = sa.func.current_timestamp()),
    sa.Column("UpdatedAt", sa.DateTime()(), onupdate = sa.func.current_timestamp())
)
