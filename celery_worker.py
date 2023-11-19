from celery import Celery
from dotenv import load_dotenv
import json
import os
from psql import save_currency_rate
import requests
import redis


# Подключение к Redis
load_dotenv()
redis_host = os.getenv('REDIS_HOST')
redis_port = os.getenv('REDIS_PORT')
redis_db = os.getenv('REDIS_DB')
redis_instance = redis.StrictRedis(host=redis_host, port=int(redis_port), db=int(redis_db))
# Настройка Celery для использования Redis
celery_app = Celery("currency_worker", broker=f"redis://{redis_host}:{redis_port}/{redis_db}")
# Список валют
key_currencies = ('RUB', 'EUR', 'BTC', 'CNY', 'USD')


@celery_app.task
def fetch_currency_data():
    key = os.getenv('KEY')
    headers = {'apikey': key}
    res = requests.get('https://api.currencyapi.com/v3/latest', headers=headers)
    data = res.json()
    exchange_rates = {}
    for currency in key_currencies:
        rate = data['data'][currency]['value']
        save_currency_rate(currency, rate)  # Сохранение в PostgreSQL
        exchange_rates[currency] = rate
    # Сохранение курсов валют в Redis
    redis_instance.set("currency_data", json.dumps(exchange_rates), ex=6)  # 10 минут в секундах


# Настройка расписания для Celery
celery_app.conf.beat_schedule = {
    "fetch-currency-data-every-15-minutes": {
        "task": "celery_worker.fetch_currency_data",
        "schedule": 9.0,  # 15 минут в секундах
    }
}
