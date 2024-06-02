from fastapi import FastAPI #, Body
from fastapi_handler import FastApiHandler

"""
Пример запуска из директории mle-sprint3/app:
uvicorn churn_app:app --reload --port 8081 --host 0.0.0.0
Для просмотра документации API и совершения тестовых запросов зайти на  http://127.0.0.1:8000/docs
"""

app = FastAPI()
app.handler = FastApiHandler()

@app.get("/")
def read_root():
    return {"status": "Alive"}

@app.post("/predict") 
def get_prediction_for_item(model_params: dict):
    return app.handler.handle(model_params) 