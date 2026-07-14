from db.db_setup import sa, connection, metadata

news = sa.Table(
    "news",
    metadata,
    sa.Column("title", sa.String(255)),
    sa.Column("content", sa.String(255)),
    sa.Column("CreatedAt", sa.DateTime(), default = sa.func.current_timestamp()),
    sa.Column("UpdatedAt", sa.DateTime(), onupdate = sa.func.current_timestamp())
)