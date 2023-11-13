from celery import Celery
from psql import save_currency_rates
import requests
import redis
import json
from psql import Base, engine

# Настройка Celery для использования Redis
celery_app = Celery("currency_worker", broker="redis://localhost:6379/0")
Base.metadata.create_all(bind=engine)
# Подключение к Redis
redis_instance = redis.StrictRedis(host='localhost', port=6379, db=0)


@celery_app.task
def fetch_currency_data():
    headers = {'apikey': 'cur_live_tqaFStL1h8RG0xuZacLeJF80ybstuNGMLvjjluuK'}
    res = requests.get('https://api.currencyapi.com/v3/latest', headers=headers)
    data = res.json()
    key_valute = ('RUB', 'EUR', 'BTC', 'CNY', 'USD')
    exchange_dollars = {}
    exchange_rub = {}
    for valute in key_valute:
        exchange_dollars[valute] = data['data'][valute]['value']
        exchange_rub[valute] = exchange_dollars['RUB'] / exchange_dollars[valute]
    print('Берём данные')
    # Сохранение данных в Redis
    redis_instance.set("currency_data", json.dumps(exchange_rub))
    # Сохранение данных в Postgress
    save_currency_rates(
        usd_rate=exchange_rub.get("USD", 0),
        eur_rate=exchange_rub.get("EUR", 0),
        btc_rate=exchange_rub.get("BTC", 0),
        cny_rate=exchange_rub.get("CNY", 0)
    )


# Настройка расписания для Celery
celery_app.conf.beat_schedule = {
    "fetch-currency-data-every-15-minutes": {
        "task": "celery_worker.fetch_currency_data",
        "schedule": 900.0,  # 15 минут в секундах
    }
}
