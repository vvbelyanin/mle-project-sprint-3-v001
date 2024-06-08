"""
services/app/app.py

This module sets up a FastAPI application with endpoints for health check, 
prediction, and random prediction. It uses a custom handler for processing 
predictions and generating random data.

Dependencies:
    - fastapi: FastAPI framework for building APIs.
    - fastapi_handler: Custom handler for processing predictions and generating random data.

Endpoints:
    - GET /: Health check endpoint that returns the status of the service.
    - POST /predict: Endpoint to get a prediction based on the provided model parameters.
    - GET /random: Endpoint to get a prediction based on randomly generated model parameters.

Usage Example:
    To run this FastAPI application, use the following command:
    uvicorn app:app --host 127.0.0.1 --port 8000

    Example Requests:
    1. Health Check:
        curl -X GET "http://localhost:8000/"

    2. Get Random Prediction:
        curl -X GET "http://localhost:8000/random"
"""

from fastapi import FastAPI
from fastapi_handler import FastApiHandler, gen_random_data

app = FastAPI()
app.handler = FastApiHandler()

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
    return (random_params, app.handler.handle(random_params))
