from dotenv import load_dotenv
import os

load_dotenv()

user = os.getenv('PSQL_USER')
password = os.getenv('PSQL_PASSWORD')
host = os.getenv('PSQL_HOST')
db = os.getenv('PSQL_NAME')
port = os.getenv('PSQL_PORT')