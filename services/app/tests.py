"""
services/app/tests.py

This module contains unit tests for the FastAPI application 
using the unittest framework and FastAPI's TestClient.
The tests cover the root endpoint, prediction endpoint 
with various scenarios, and validation of the application's 
response to both correct and incorrect input data.

Dependencies:
    - unittest: For structuring and running tests.
    - fastapi.testclient: For testing FastAPI applications.
    - app: The FastAPI application module being tested.

Classes:
    - TestOnline: Contains test cases to validate the endpoints of the FastAPI application.

Methods:
    - setUp(): Prepares test data before each test.
    - test_root(): Tests the root endpoint for expected status code and response.
    - test_predict_empty_data(): Tests the predict endpoint with empty data and expects a 405 status code.
    - test_predict_random_data(): Tests the predict endpoint with random data and checks if the score is a float.
    - test_predict_error_data(): Tests the predict endpoint with various invalid data scenarios.
    - test_predict_ok(): Tests the predict endpoint with valid data and checks for the correct response.

Usage Example:
    To run these tests, use the following command:
    python -m unittest tests.py
"""

import unittest
from fastapi.testclient import TestClient
from app import app

class TestOnline(unittest.TestCase):
    """
    Contains test cases to validate the endpoints of the FastAPI application.

    Methods:
        setUp(): Prepares test data before each test.
        test_root(): Tests the root endpoint for expected status code and response.
        test_predict_empty_data(): Tests the predict endpoint with empty data and expects a 405 status code.
        test_predict_random_data(): Tests the predict endpoint with random data and checks if the score is a float.
        test_predict_error_data(): Tests the predict endpoint with various invalid data scenarios.
        test_predict_ok(): Tests the predict endpoint with valid data and checks for the correct response.
    """
    
    def setUp(self):
        """
        Prepares test data before each test. This data includes required parameters for making predictions.
        """
        self.test_data = {
            "floor": 1,
            "is_apartment": 0,
            "kitchen_area": 7.0,
            "living_area": 27.0,
            "rooms": 2,
            "total_area": 40.0,
            "building_id": 764,
            "build_year": 1936,
            "building_type_int": 1,
            "latitude": 55.74044418334961,
            "longitude": 37.52492141723633,
            "ceiling_height": 3.0,
            "flats_count": 63,
            "floors_total": 7,
            "has_elevator": 1
        }

    def test_root(self):
        """
        Tests the root endpoint ("/") for expected status code and response content.
        Expects status code 200 and response {"status": "Alive"}.
        """
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "Alive"})

    def test_predict_empty_data(self):
        """
        Tests the predict endpoint ("/predict") with empty data and expects a 405 status code.
        """
        response = client.get("/predict")
        self.assertEqual(response.status_code, 405)

    def test_predict_random_data(self):
        """
        Tests the predict endpoint ("/random") with random data and checks 
        if the score in the response is a float.
        """
        response = client.get("/random")
        self.assertIsInstance(response.json()[1]['score'], float)

    def test_predict_error_data(self):
        """
        Tests the predict endpoint ("/predict") with various invalid data scenarios 
        including empty data, missing parameters, extra parameters, incorrect 
        parameter names, and incorrect data formats.
        """
        # Empty json
        response = client.post("/predict", json={})
        self.assertEqual(response.json(), {"Error": "Problem with parameters"})

        # Lack of params
        error_data = self.test_data.copy()
        del error_data['floor']
        response = client.post("/predict", json=error_data)
        self.assertEqual(response.json(), {'Error': 'Problem with parameters'})

        # Excess of params
        error_data = self.test_data.copy()
        error_data["extra_data"] = 42
        response = client.post("/predict", json=error_data)
        self.assertEqual(response.json(), {'Error': 'Problem with parameters'})

        # Wrong params name
        error_data = self.test_data.copy()
        del error_data['floor']
        error_data['floor_other'] = 1
        response = client.post("/predict", json=error_data)
        self.assertEqual(response.json(), {'Error': 'Problem with parameters'})

        # Wrong data format
        error_data = self.test_data.copy()
        error_data['floor'] = 'one'
        response = client.post("/predict", json=error_data)
        self.assertEqual(response.json(), {'Error': 'Problem with request'})

    def test_predict_ok(self):
        """
        Tests the predict endpoint ("/predict") with valid data and checks for the correct response.
        Expects status code 200 and a valid prediction score.
        """
        with TestClient(app) as client:
            response = client.post("/predict", json=self.test_data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {'score': 12859673.47644087})

if __name__ == '__main__':
    client = TestClient(app)
    unittest.main()
