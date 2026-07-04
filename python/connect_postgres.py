import os
import json
from contextlib import contextmanager
from collections.abc import Iterator

import psycopg2
from dotenv import load_dotenv
from psycopg import Connection


from pymemcache.client.base import Client 

cache = Client(("localhost", 11211)) # connect to the memcached server running on localhost at port 11211

load_dotenv()


#connection = psycopg2.connect(
#    host = 'localhost',
#    database = 'fresh_segments',
#    password = 'mypassword'
#)
#
#cursor = connection.cursor() # create a cursor object to interact with the database 
#cursor.execute('select * from fresh_segments.interest_map limit 10')
#
## fetch all the results from the query
#
#record = cursor.fetchall()
#print(record)


@contextmanager
def get_db_connection() -> Iterator[Connection]:
    database_url = os.getenv('DATABASE_URL')  # This is connecting to the fresh segments database using the DATABASE_URL environment variable
    with psycopg2.connect(database_url) as connection:
        yield connection


def get_interest_by_id(interest_id: int):
    cache_key = f"user:{interest_id}"

    # Try the cache first
    cached_user = cache.get(cache_key)

    if cached_user is not None:
        print("Cache hit")
        return json.loads(cached_user)

    print("Cache miss")

    conn = get_db_connection()
    
    try:
        with get_db_connection() as conn:
            
            with conn.cursor() as cur:
                cur.execute("""select interest_id, interest_name, interest_summary from
                fresh_segments.analytics_analytics.dim_interest where interest_id = %s""", (interest_id,))
                row = cur.fetchone()

                if row is None:
                    return None

                interest_data = {
                    "interest_id": row[0],
                    "interest_name": row[1],
                    "interest_summary": row[2]
                }

                cache.set(cache_key, json.dumps(interest_data), expire = 3600)
                
                return interest_data
    finally:
        conn.close()

            
if __name__ == "__main__":
    #with get_db_connection() as connection: # use the context manager to get a connection to the database
    #    with connection.cursor() as cursor:
    #        cursor.execute('select * from fresh_segments.interest_map limit 10')
    #        for row in cursor.fetchall():
    #            print(f"{row[0]}, {row[1]}, {row[2]}")               
    print(get_interest_by_id(123))
    print(get_interest_by_id(123))
