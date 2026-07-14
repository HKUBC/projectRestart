import sqlalchemy as sa
from user_information.user_table import user
#Creating db connection and metadata
engine = sa.create_engine('sqlite:///:memory:')
connection = engine.connect()
metadata = sa.MetaData()

def insert_user(firstName: str, lastName: str, email: str, password: str) -> None:
    query = user.insert().values(firstName = firstName, lastName = lastName, email = email, password = password)
    connection.execute(query)