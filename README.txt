Запуск main: (FastAPI + Redis)
	uvicorn main:app --reload
Запуск celery_worker: (Redis + Celery)
	celery -A celery_worker.celery_app worker --loglevel=info --beat
Пример использования эндпоинта для конвертации валют:
	http://127.0.0.1:8000/convert?currency=RUB&amount=1000

