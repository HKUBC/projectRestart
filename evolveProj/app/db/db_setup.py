import sqlalchemy as sa
from user_information.user_table import users
#Creating db connection and metadata


def insert_users(firstName: str, lastName: str, email: str, id: int, password: str, connection ) -> None:
    query = users.insert().values(firstName = firstName, lastName = lastName, email = email, password = password)
    connection.execute(query)


def select_users(firstName: str, email: str, connection) -> sa.engein.Result:
    query = users.select().where(users.firstName == firstName and users.email == email)
    result = connection.execute(query)
    return result.fetchone()


def main() -> None:
    
    engine = sa.create_engine("postgresql://harrisonkayihura@localhost:5432/proj310")
    #engine = sa.create_engine("sqlitte:///:memory:")
    print("Hello World")
    connection = engine.connect()
    metadata = sa.MetaData()
    metadata.create_all(engine)
    insert_users("Harrison", "Kayihura", "123@gmail.com",1234,"password", connection)
    print(select_users("Harrison", "123@gmail.com", connection))
    connection.close()

if __name__ == "__main__":
    main()