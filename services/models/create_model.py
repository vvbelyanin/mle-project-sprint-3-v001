"""
services/models/create_model.py

This module provides the generation and fitting of a model for FastAPI-microservice

Dependencies:
    - os (to get environment variables)
    - sqlalchemy, pandas (for reading data from PostgreSQL)
    - catboost (for using CatBoostRegressor model)
    - pickle (to serialize and save model)
"""

import os
import pickle
import pandas as pd
from sqlalchemy import create_engine
from catboost import CatBoostRegressor

TABLE_NAME = 'clean_flats'
RANDOM_STATE = 42
MODEL_NAME = 'fitted_model.pkl'

con = create_engine(
    f"postgresql://{os.getenv('DB_DESTINATION_USER')}:"
    f"{os.getenv('DB_DESTINATION_PASSWORD')}@"
    f"{os.getenv('DB_DESTINATION_HOST')}:"
    f"{os.getenv('DB_DESTINATION_PORT')}/"
    f"{os.getenv('DB_DESTINATION_NAME')}"
    )

df = pd.read_sql(sql=f'SELECT * FROM {TABLE_NAME}', con=con).drop(['id', 'flat_id'], axis=1)
X, y = df.drop('price', axis=1), df['price']

model = CatBoostRegressor(verbose=0, random_state=RANDOM_STATE)
model.fit(X, y)

with open(MODEL_NAME, 'wb') as model_file:
    pickle.dump(model, model_file)

print(f'Fitted model saved to {os.getcwd()}/{MODEL_NAME}')
