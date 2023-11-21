from celery import Celery
from config import redis_host, redis_port, redis_db, api_key
import json
from psql import save_currency_rate
import requests
import redis


redis_instance = redis.StrictRedis(host=redis_host, port=int(redis_port), db=int(redis_db))
# Настройка Celery для использования Redis
celery_app = Celery("currency_worker", broker=f"redis://{redis_host}:{redis_port}/{redis_db}")
# Список валют
key_currencies = ('RUB', 'EUR', 'BTC', 'CNY', 'USD')


@celery_app.task
def fetch_currency_data():
    headers = {'apikey': api_key}
    res = requests.get('https://api.currencyapi.com/v3/latest', headers=headers)
    data = res.json()
    exchange_rates = {}
    for currency in key_currencies:
        rate = data['data'][currency]['value']
        save_currency_rate(currency, rate)  # Сохранение в PostgreSQL
        exchange_rates[currency] = rate
    # Сохранение курсов валют в Redis
    redis_instance.set("currency_data", json.dumps(exchange_rates), ex=15)  # 10 минут в секундах


# Настройка расписания для Celery
celery_app.conf.beat_schedule = {
    "fetch-currency-data-every-15-minutes": {
        "task": "celery_worker.fetch_currency_data",
        "schedule": 30.0,  # 15 минут в секундах
    }
}
