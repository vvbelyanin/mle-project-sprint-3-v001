"""
services/app/app-stage-3.py

This module sets up a FastAPI application with endpoints for health check, 
prediction, and random prediction. It also integrates Prometheus 
instrumentation for monitoring.

Dependencies:
    - fastapi: FastAPI framework for building APIs.
    - fastapi_handler: Custom handler for processing predictions.
    - prometheus_fastapi_instrumentator: Prometheus instrumentation for FastAPI.

Endpoints:
    - GET /: Health check endpoint that returns the status of the service.
    - POST /predict: Endpoint to get a prediction based on the provided model parameters.
    - GET /random: Endpoint to get a prediction based on randomly generated model parameters.

Usage Example:
    To run this FastAPI application, use the following command:
    uvicorn my_fastapi_app:app --host 0.0.0.0 --port 8000

    Example Requests:
    Health Check:
        curl -X GET "http://localhost:8000/"

    Get Random Prediction:
        curl -X GET "http://localhost:8000/random"

"""

from fastapi import FastAPI
from fastapi_handler import FastApiHandler, gen_random_data
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
app.handler = FastApiHandler()

instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

@app.get("/")
def read_root() -> dict:
    """
    Health check endpoint that returns the status of the service.

    Returns:
        dict: A dictionary with a status key indicating the service is alive.
    """
    return {"status": "Alive"}

@app.post("/predict")
def get_prediction_for_item(model_params: dict) -> dict:
    """
    Get a prediction based on the provided model parameters.

    Args:
        model_params (dict): A dictionary containing model parameters.

    Returns:
        dict: The prediction result from the model handler.
    """
    return app.handler.handle(model_params)

@app.get("/random")
def get_random_prediction() -> tuple:
    """
    Get a prediction based on randomly generated model parameters.

    Returns:
        tuple: A tuple containing the random parameters and the prediction result.
    """
    random_params = gen_random_data()
    predicted_price = app.handler.handle(random_params)['score']
    return (random_params, predicted_price)
