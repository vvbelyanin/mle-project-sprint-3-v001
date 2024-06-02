import unittest
from fastapi.testclient import TestClient
from app import app

class TestOnline(unittest.TestCase):
    # Функция, которая выполняется перед каждым тестом
    # Подготавливаем данные, на которых будем тестировать приложение
    def setUp(self):
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

    # Проверяем работу корневой страницы. Ожидаем получить код 200 и сообщение "Alive"
    def test_root(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),  {"status": "Alive"})

    def test_predict_empty_data(self):
        response = client.get("/predict")
        self.assertEqual(response.status_code, 405)

    # Проверка случаев, когда данные в post-запросе не проходят валидацию
    def test_predict_error_data(self):
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
        

   # Responce to correct data
    def test_predict_ok(self):
        with TestClient(app) as client:
            response = client.post("/predict", json=self.test_data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {'score': 12859673.47644087})

if __name__ == '__main__':
    client = TestClient(app)
    unittest.main()
