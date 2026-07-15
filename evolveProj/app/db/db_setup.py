import sqlalchemy as sa
from user_information.user_table import users



def insert_users(firstname: str, lastname: str, email: str, password: str, connection ) -> None:
    query = users.insert().values(
        firstname = firstname, 
        lastname = lastname, 
        email = email,
        password = password,
        )
    print(query)
    connection.execute(query)


def select_users(firstname: str, email: str, connection) -> sa.engein.Result:
    query = users.select().where(users.c.firstname == firstname and users.c.email == email)
    result = connection.execute(query)
    return result.fetchone()


def main() -> None:
    #Creating db connection and metadata
    engine = sa.create_engine("postgresql://harrisonkayihura@localhost:5432/proj310")
    connection = engine.connect()
    metadata = sa.MetaData()
    metadata.create_all(engine)
    insert_users("Harrison", "Kayihura", "123@gmail.com","password", connection)
    print(select_users("Harrison", "123@gmail.com", connection))
    connection.close()

if __name__ == "__main__":
    main()