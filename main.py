from fastapi import FastAPI, HTTPException
import redis
import json

app = FastAPI()

# Подключение к Redis
redis_instance = redis.StrictRedis(host='localhost', port=6379, db=0)


@app.get("/data", response_model=dict)
async def get_data():
    currency_data = redis_instance.get("currency_data")
    if currency_data:
        return json.loads(currency_data)
    else:
        raise HTTPException(status_code=404, detail="Данные о валютах не найдены")


@app.get("/convert/{rub_amount}", response_model=dict)
async def convert_currency(rub_amount: float):
    currency_data = redis_instance.get("currency_data")
    if not currency_data:
        raise HTTPException(status_code=404, detail="Данные о валютах не найдены")

    exchange_rates = json.loads(currency_data)
    converted_values = {}

    for currency, rate in exchange_rates.items():
        # Пропускаем RUB, так как пользователь уже передаёт сумму в рублях
        if currency != 'RUB':
            converted_values[currency] = rub_amount / rate

    return {
        "message": f"У вас {rub_amount} рублей",
        "converted_values": converted_values
    }


