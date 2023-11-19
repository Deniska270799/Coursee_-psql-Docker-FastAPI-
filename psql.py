from datetime import datetime
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, Column, Integer, String, Float, TIMESTAMP
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


load_dotenv()  # Загружает переменные из .env
# Получаем переменные из окружения
user = os.getenv('PSQL_USER')
password = os.getenv('PSQL_PASSWORD')
host = os.getenv('PSQL_HOST')
db = os.getenv('PSQL_NAME')
port = os.getenv('PSQL_PORT')
DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
class CurrencyRates(Base):
    __tablename__ = 'currency_rates'
    id = Column(Integer, primary_key=True)
    currency = Column(String, nullable=False)
    rate = Column(Float)
    datetime = Column(TIMESTAMP)


def save_currency_rate(currency, rate):
    with SessionLocal() as session:
        new_rate = CurrencyRates(
            currency=currency,
            rate=rate,
            datetime=datetime.utcnow()  # Устанавливаем текущее время
        )
        session.add(new_rate)
        session.commit()


