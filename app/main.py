from config import redis_host, redis_port, redis_db
from fastapi import FastAPI, HTTPException
import json
from app.db.psql import SessionLocal
from pydantic import BaseModel, validator
import redis
from sqlalchemy import text
from typing import Dict


class CurrencyRatesResponse(BaseModel):
    rates: Dict[str, float]

    @validator('rates', pre=True)
    def parse_rates(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v

class Currency_Convert(BaseModel):
    currency: str
    amount: float

app = FastAPI()
redis_instance = redis.StrictRedis(host=redis_host, port=int(redis_port), db=int(redis_db))

@app.get("/data", response_model=CurrencyRatesResponse)
async def get_data():
    currency_data = redis_instance.get("currency_data")
    if currency_data:
        return CurrencyRatesResponse(rates=currency_data)
    else:
        raise HTTPException(status_code=404, detail="Данные о валютах не найдены")


@app.post("/convert")
async def convert_currency(request: Currency_Convert):
    currency_data = redis_instance.get("currency_data")
    if not currency_data:
        with SessionLocal() as session:
            # Сырой SQL-запрос для получения последних курсов валют
            sql_query = text("""
                    SELECT DISTINCT ON (currency) currency, rate
                    FROM currency_rates
                    ORDER BY currency, datetime DESC
                """)
            result = session.execute(sql_query)
            exchange_rates = {row.currency: row.rate for row in result}
    else:
        exchange_rates = json.loads(currency_data)

    if request.currency not in exchange_rates:
        raise HTTPException(status_code=404, detail=f"Курс для валюты {request.currency} не найден")

    converted_values = {}
    amount_in_usd = request.amount / exchange_rates[request.currency] if request.currency != "USD" else request.amount
    for other_currency in exchange_rates:
        if other_currency != request.currency:
            converted_amount = amount_in_usd * exchange_rates[other_currency]
            converted_values[other_currency] = converted_amount

    return {
        "your_currency": request.currency,
        "your_amount": request.amount,
        "converted_currencies": converted_values
    }






