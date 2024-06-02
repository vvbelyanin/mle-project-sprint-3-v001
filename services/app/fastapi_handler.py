#import os
#import pandas as pd
#from sqlalchemy import create_engine
#from catboost import CatBoostRegressor
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
    def __init__(self):
        self.required_model_params = REQUIRED_PARAMS
        self.load_model(model_path=MODEL_PATH)

    def load_model(self, model_path: str):
        try:
            with open(model_path, 'rb') as model_file:
                self.model = pickle.load(model_file)        
        except Exception as e:
            print(f"Failed to load model: {e}")

    def price_predict(self, model_params: dict) -> float:
        return self.model.predict(list(model_params.values()))
        
    def validate_params(self, model_params: dict) -> bool:
        if set(model_params.keys()) == set(self.required_model_params):
                print("All model params exist")
        else:
                print("Not all model params exist")
                return False
        return True
                
    def handle(self, model_params):
        try:
            if not self.validate_params(model_params):
                print("Error while handling request")
                response = {"Error": "Problem with parameters"}
            else:
                print("Predicting for model_params:")
                pprint(model_params, sort_dicts=False)
                predicted_price = self.price_predict(model_params)
                response = {"score": predicted_price}
        except Exception as e:
            print(f"Error while handling request: {e}")
            return {"Error": "Problem with request"}
        else:
            return response
        
    
if __name__ == "__main__":

    # создаём тестовый запрос
    test_params = {
        "floor": 'one', 
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
        "has_elevator": 1}

    # создаём обработчик запросов для API
    handler = FastApiHandler()

    # делаем тестовый запрос
    response = handler.handle(test_params)
    print(f"Response: {response}")