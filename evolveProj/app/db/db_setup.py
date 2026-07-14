import sqlalchemy as sa
#Creating db connection and metadata
engine = sa.create_engine('sqlite:///:memory:')
connection = engine.connect()
metadata = sa.MetaData()

#User related tables





#Items and clasifications










# Reviews

#payment
payment_system = sa.Table(
    "payment_system",
    metadata,
    sa.Column("id", sa.Integer(10), primary_key = True),
    sa.Column("user_id", sa.Integer(10), sa.ForeignKey("users.id")),
    sa.Colum("method", sa.String(255)),
    sa.Column("confirmation", sa.Boolean())
)

# website tables




def insert_user(firstName: str, lastName: str, email: str, password: str) -> None:
    query = user.insert().values(firstName = firstName, lastName = lastName, email = email, password = password)
    connection.execute(query)