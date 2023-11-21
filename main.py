from celery_worker import key_currencies
from config import redis_host, redis_port, redis_db
from fastapi import FastAPI, HTTPException, Query
import json
from psql import SessionLocal, CurrencyRates
from pydantic import BaseModel, validator
import redis
from typing import Dict


class CurrencyRatesResponse(BaseModel):
    rates: Dict[str, float]

    @validator('rates', pre=True)
    def parse_rates(cls, v):
        if isinstance(v, str):
            return json.loads(v)
        return v

app = FastAPI()
redis_instance = redis.StrictRedis(host=redis_host, port=int(redis_port), db=int(redis_db))

@app.get("/data", response_model=CurrencyRatesResponse)
async def get_data():
    currency_data = redis_instance.get("currency_data")
    if currency_data:
        return CurrencyRatesResponse(rates=currency_data)
    else:
        raise HTTPException(status_code=404, detail="Данные о валютах не найдены")


@app.get("/convert")
async def convert_currency(currency: str = Query(...), amount: float = Query(...)):
    currency_data = redis_instance.get("currency_data")
    if not currency_data:
        with SessionLocal() as session:
            recent_rates = session.query(CurrencyRates).order_by(CurrencyRates.datetime.desc()).limit(len(key_currencies)).all()
            exchange_rates = {rate.currency: rate.rate for rate in recent_rates}
    else:
        exchange_rates = json.loads(currency_data)

    if currency not in exchange_rates:
        raise HTTPException(status_code=404, detail=f"Курс для валюты {currency} не найден")

    converted_values = {}
    amount_in_usd = amount / exchange_rates[currency] if currency != "USD" else amount
    for other_currency in exchange_rates:
        if other_currency != currency:
            converted_amount = amount_in_usd * exchange_rates[other_currency]
            converted_values[other_currency] = converted_amount

    key = f"{currency}_{amount}"
    return {key: converted_values}



