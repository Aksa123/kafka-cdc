import psycopg
from dotenv import dotenv_values

ENV = dotenv_values('.env')
DB_SOURCE_HOST = ENV['DB_SOURCE_HOST']
DB_SOURCE_PORT = ENV['DB_SOURCE_PORT']
DB_SOURCE_NAME = ENV['DB_SOURCE_NAME']
DB_SOURCE_USER = ENV['DB_SOURCE_USER']
DB_SOURCE_PASSWORD = ENV['DB_SOURCE_PASSWORD']

DB_DESTINATION_HOST = ENV['DB_DESTINATION_HOST']
DB_DESTINATION_PORT = ENV['DB_DESTINATION_PORT']
DB_DESTINATION_NAME = ENV['DB_DESTINATION_NAME']
DB_DESTINATION_USER = ENV['DB_DESTINATION_USER']
DB_DESTINATION_PASSWORD = ENV['DB_DESTINATION_PASSWORD']

with psycopg.connect(host=DB_SOURCE_HOST, port=DB_SOURCE_PORT, dbname=DB_SOURCE_NAME, user=DB_SOURCE_USER, password=DB_SOURCE_PASSWORD) as conn_src:
    with conn_src.cursor() as cur:
        for q in ['models.sql', 'seeder.sql', 'publication.sql']:
            with open(q) as f:
                query = f.read()
            cur.execute(query)

with psycopg.connect(host=DB_DESTINATION_HOST, port=DB_DESTINATION_PORT, dbname=DB_DESTINATION_NAME, user=DB_DESTINATION_USER, password=DB_DESTINATION_PASSWORD) as conn_dst:
    with conn_dst.cursor() as cur:
        for q in ['models.sql']:
            with open(q) as f:
                query = f.read()
            cur.execute(query)

            