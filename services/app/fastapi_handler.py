"""
services/app/fastapi_handler.py

This module provides functionality to predict real estate prices 
based on various parameters using a pre-trained machine learning model. 
It includes a handler for FastAPI integration and utility functions to generate random 
test data.

Dependencies:
    - random: For generating random test data.
    - pickle: For loading the pre-trained model.
    - pprint: For pretty-printing dictionary data.

Classes:
    - FastApiHandler: A handler class to manage loading the model, validating parameters, 
      and making predictions.

Functions:
    - gen_random_data(): Generates random data for testing the prediction model.

Usage Example:
    To run this module, use the following command:
    python3 fastapi_handler.py

Example Requests:
    Initialize the handler and make a prediction:
        handler = FastApiHandler()
        test_params = {
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
        response = handler.handle(test_params)
        print(f"Response: {response}")
"""

from random import randint, uniform
import pickle
from pprint import pprint

REQUIRED_PARAMS = [
    'floor', 'is_apartment', 'kitchen_area', 'living_area', 'rooms',
    'total_area', 'building_id', 'build_year', 'building_type_int', 
    'latitude', 'longitude', 'ceiling_height', 'flats_count', 'floors_total', 
    'has_elevator'
    ]
MODEL_PATH = '../models/fitted_model.pkl'

class FastApiHandler:
    """
    A handler class to manage loading the model, validating parameters, and making predictions.

    Attributes:
        required_model_params (list): List of required parameters for the model.
        model (object): The pre-trained machine learning model.
    
    Methods:
        load_model(model_path: str): Loads the model from the specified path.
        price_predict(model_params: dict) -> float: Predicts the price based on model parameters.
        validate_params(model_params: dict) -> bool: Validates that all required parameters are present.
        handle(model_params: dict) -> dict: Handles the prediction request, validates parameters, and returns the prediction.
    """
    def __init__(self):
        """Initializes the handler and loads the model."""
        self.required_model_params = REQUIRED_PARAMS
        self.load_model(model_path=MODEL_PATH)

    def load_model(self, model_path: str):
        """
        Loads the model from the specified path.

        Args:
            model_path (str): The path to the model file.
        
        Raises:
            Exception: If the model fails to load.
        """
        try:
            with open(model_path, 'rb') as model_file:
                self.model = pickle.load(model_file)        
        except Exception as e:
            print(f"Failed to load model: {e}")

    def price_predict(self, model_params: dict) -> float:
        """
        Predicts the price based on model parameters.

        Args:
            model_params (dict): A dictionary of model parameters.
        
        Returns:
            float: The predicted price.
        """
        return self.model.predict(list(model_params.values()))

    def validate_params(self, model_params: dict) -> bool:
        """
        Validates that all required parameters are present.

        Args:
            model_params (dict): A dictionary of model parameters.
        
        Returns:
            bool: True if all parameters are present, False otherwise.
        """
        if set(model_params.keys()) == set(self.required_model_params):
            print("All model params exist")
        else:
            print("Not all model params exist")
            return False
        return True

    def handle(self, model_params: dict) -> dict:
        """
        Handles the prediction request, validates parameters, and returns the prediction.

        Args:
            model_params (dict): A dictionary of model parameters.
        
        Returns:
            dict: The response containing the prediction or an error message.
        """
        if not self.validate_params(model_params):
            return {"Error": "Problem with parameters"}

        print("Predicting for model_params:")
        pprint(model_params, sort_dicts=False)
        try:
            predicted_price = self.price_predict(model_params)
            return {"score": predicted_price}
        except Exception as e:
            print(f"Error while handling request: {e}")
            return {"Error": "Problem with request"}


def gen_random_data() -> dict:
    """
    Generates random data for testing the prediction model.

    Returns:
        dict: A dictionary of randomly generated model parameters.
    """
    return {
        "floor": randint(1, 100), 
        "is_apartment": randint(0, 1), 
        "kitchen_area": uniform(1, 100), 
        "living_area": uniform(1, 200), 
        "rooms": randint(1, 10), 
        "total_area": uniform(1, 300), 
        "building_id": randint(1, 20000), 
        "build_year": randint(1900, 2030),  
        "building_type_int": randint(1, 10), 
        "latitude": uniform(54, 56), 
        "longitude": uniform(36, 38), 
        "ceiling_height": uniform(1, 5), 
        "flats_count": randint(1, 1000), 
        "floors_total": randint(1, 100), 
        "has_elevator": randint(0, 1)
    }

if __name__ == "__main__":
    # Create a test request
    test_params = {
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

    # Create a request handler for the API
    handler = FastApiHandler()

    # Make a test request
    response = handler.handle(test_params)
    print(f"Response: {response}")
