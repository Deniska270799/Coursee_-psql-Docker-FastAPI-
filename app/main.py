from app.routers import currency_router
from fastapi import FastAPI


app = FastAPI()
app.include_router(currency_router.router)






