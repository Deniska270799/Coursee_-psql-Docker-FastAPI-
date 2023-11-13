import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Float, Integer, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()  # Загружает переменные из .env
# Получаем переменные из окружения
user = os.getenv('PSQL_USER')
password = os.getenv('PSQL_PASSWORD')
host = os.getenv('PSQL_HOST')
db = os.getenv('PSQL_NAME')
DATABASE_URL = f"postgresql://{user}:{password}@{host}/{db}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
metadata = MetaData()

currency_rates = Table(
    "currency_rates",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("usd_rate", Float),
    Column("eur_rate", Float),
    Column("btc_rate", Float),
    Column("cny_rate", Float),
)

class CurrencyRates(Base):
    __table__ = currency_rates

Base.metadata.create_all(bind=engine)

def save_currency_rates(usd_rate, eur_rate, btc_rate, cny_rate):
    with SessionLocal() as session:
        db_currency_rates = CurrencyRates(
            usd_rate=usd_rate,
            eur_rate=eur_rate,
            btc_rate=btc_rate,
            cny_rate=cny_rate
        )
        session.add(db_currency_rates)
        session.commit()

