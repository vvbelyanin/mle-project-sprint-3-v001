"""
services/app/load_test_script.py

This script performs load testing on a local FastAPI application 
by sending a series of GET requests to two endpoints: '/random' 
and '/metrics'. The script sends a specified number of requests to 
each endpoint, pausing for a random duration between each request.

Dependencies:
    - time: For pausing execution between requests.
    - random: For generating random wait times between requests.
    - requests: For sending HTTP requests.

Usage Example:
    To run this script, use the following command:
    python load_test.py
"""

import time
import random
import requests


NUM_REQUESTS = 1000

for i in range(NUM_REQUESTS):
    print(f'\rRequest: {i+1} of {NUM_REQUESTS}', end='', flush=True)
    requests.get('http://localhost:8000/random', timeout=10)
    time.sleep(random.random())
    requests.get('http://localhost:8000/metrics', timeout=10)
    time.sleep(random.random())
