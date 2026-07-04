import psycopg2
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

POSTGRES_DSN = "dbname=fresh_segments user=postgres password=mypassword host=localhost port=5432"
ES_URL = "http://localhost:9200"
INDEX_NAME = "interests"

es = Elasticsearch(ES_URL)

rows_query = """
SELECT
    interest_id,
    interest_name,
    interest_summary
FROM fresh_segments.analytics_analytics.dim_interest
"""

def generate_docs():
    conn = psycopg2.connect(POSTGRES_DSN)

    try:
        with conn.cursor() as cur:
            cur.execute(rows_query)

            for id_, name, description in cur:
                yield {
                    "_index": INDEX_NAME,
                    "_id": str(id_),
                    "_source": {
                        "id": id_,
                        "name": name,
                        "description": description,
                    },
                }
    finally:
        conn.close()

success, failed = bulk(es, generate_docs(), raise_on_error=False)

print(f"Indexed {success} rows into Elasticsearch")

if failed:
    print("Some rows failed:")
    print(failed[:5])
    
