from sqlalchemy import MetaData, Integer, String, Float, TIMESTAMP, Table, Column
import datetime

metadata = MetaData()
currency_rates = Table(
    "currency_rates",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("currency", String, nullable=False),
    Column("rate", Float),
    Column("datetime", TIMESTAMP, default=datetime.datetime.utcnow)
)