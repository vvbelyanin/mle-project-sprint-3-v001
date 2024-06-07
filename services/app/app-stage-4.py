"""
services/app/app-stage-4.py

This module sets up a FastAPI application with endpoints for health check, prediction, 
and random prediction. It integrates Prometheus instrumentation for monitoring CPU, 
disk, memory, and network usage, as well as histogram metrics for price predictions. 
The module also includes simulated error probabilities for testing purposes.

Dependencies:
    - fastapi: FastAPI framework for building APIs.
    - fastapi_handler: Custom handler for processing predictions.
    - prometheus_fastapi_instrumentator: Prometheus instrumentation for FastAPI.
    - prometheus_client: Prometheus client for custom metrics.
    - numpy: For creating histogram buckets.
    - psutil: For monitoring system resource usage.

Endpoints:
    - GET /: Health check endpoint that returns the status of the service.
    - POST /predict: Endpoint to get a prediction based on the provided model parameters.
    - GET /random: Endpoint to get a prediction based on randomly generated model parameters, 
      with simulated errors and resource usage metrics.

Usage Example:
    To run this FastAPI application, use the following command:
    uvicorn app-stage-4:app --host 127.0.0.1 --port 8000

    Example Requests:
    1. Health Check:
        curl -X GET "http://localhost:8000/"
    2. Get Random Prediction:
        curl -X GET "http://localhost:8000/random"
"""

import random
import time
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi_handler import FastApiHandler, gen_random_data
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Histogram, Gauge
import psutil

ERROR_PROBABILITY = 0.05

app = FastAPI()
app.handler = FastApiHandler()

instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

CPU_USAGE = Gauge('custom_cpu_usage_percent', 'CPU usage percent')
DISK_USAGE = Gauge('custom_disk_usage_percent', 'Disk usage percent')
MEMORY_USAGE = Gauge('custom_memory_usage_percent', 'Memory usage percent')
NETWORK_USAGE = Gauge('custom_network_usage_bytes_total', 'Network usage bytes')

price_predictions = Histogram(
    "price_predictions",
    "Histogram of predictions",
    buckets = np.arange(0, 2e8+1, 2e7).tolist()
    )

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
    This endpoint includes simulated errors for testing purposes and 
    updates Prometheus metrics for resource usage.

    Raises:
        HTTPException: Simulates a random failure with a {ERROR_PROBABILITY}% probability.

    Returns:
        tuple: A tuple containing the random parameters and the prediction result.
    """
    if random.random() < ERROR_PROBABILITY:
        raise HTTPException(status_code=500, detail="Random failure for testing purposes")
    time.sleep(random.random())
    random_params = gen_random_data()
    predicted_price = app.handler.handle(random_params)['score']
    price_predictions.observe(predicted_price)

    CPU_USAGE.set(psutil.cpu_percent(interval=1))
    DISK_USAGE.set(psutil.disk_usage('/').percent)
    MEMORY_USAGE.set(psutil.virtual_memory().percent)
    net_io = psutil.net_io_counters()
    NETWORK_USAGE.set(net_io.bytes_sent + net_io.bytes_recv)

    return (random_params, predicted_price)
