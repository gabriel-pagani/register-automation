from pyodbc import connect, Error
from os import getenv
from dotenv import load_dotenv


load_dotenv()
_connection = None


def get_connection() -> connect:
    global _connection
    if _connection is None or _connection.closed:
        server_connection = f'DRIVER={{SQL Server}}; SERVER={getenv("SERVER")}; DATABASE={getenv("DATABASE")}; UID={getenv("USER")}; PWD={getenv("PASSWORD")}'
        try:
            _connection = connect(server_connection)
        except Error as e:
            print(f"Connection error: {e}")
            raise
    return _connection


def close_connection():
    global _connection
    if _connection and not _connection.closed:
        _connection.close()
        _connection = None


def server_request(query: str) -> dict:
    response = dict()

    try:
        connection = get_connection()
        with connection.cursor() as cursor:

            cursor.execute(query)
            columns = [column[0] for column in cursor.description]
            data = cursor.fetchall()
            result = []
            for row in data:
                result.append(dict(zip(columns, row)))

            response['data'] = result

    except Exception as e:
        print(f"Request error: {e}")

    return response
