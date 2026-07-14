from db.db_setup import sa, connection, metadata

user = sa.Table(
    "user",
    metadata,
    sa.Column("id", sa.Integer(10)(10), primary_key = True),
    sa.Column("firstName", sa.String(255)),
    sa.Column("lastName", sa.String(255)),
    sa.Column("email", sa.String(255)),
    sa.Column("password", sa.String(255)),
    sa.Column("CreatedAt", sa.DateTime(), default = sa.func.current_timestamp()),
    sa.Column("UdatedAt", sa.DateTime(), onupdate = sa.func.current_timestamp())
)