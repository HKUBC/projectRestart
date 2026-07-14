from db.db_setup import sa, connection, metadata

address = sa.Table(
    "address",
    metadata,
    sa.Column("user_id", sa.Integer(10)(10), sa.ForeignKey("users.id")),
    sa.Column("address_line", sa.String(255)),
    sa.Column("suit_number", sa.String(255)),
    sa.Column("phone_number", sa.Integer(10)),
    sa.Column("CreatedAt", sa.DateTime(), default = sa.func.current_timestamp()),
    sa.Column("UpdatedAt", sa.DateTime(), onupdate = sa.func.current_timestamp())    
)