## Инструкции по запуску микросервиса
#### Этап 1. Написание FastAPI-микросервиса

```
# апгрейд менеджера пакетов
python3 -m pip install --upgrade pip

# создание виртуального окружения в папке .mle-sprint3-venv
python3 -m venv .mle-sprint3-venv

# активация виртуального окружения
source .mle-sprint3-venv/bin/activate

# установка необходимых пакетов
pip install -r requirements.txt

# генерация модели
# перед запуском создайте/проверьте наличие /.env файла 
# в каталоге с параметрами подключения к object storage:
cd services/models/
python create_model.py

# если необходимо, вернуться в основную папку
# переход в папку со скриптами
cd ../app/
# или 
cd services/app/

# проверка кода микросервиса с возвратом тестового предсказания
python fastapi_handler.py

# запуск ASGI-сервера со значениями по умолчанию --host 127.0.0.1 --port 8000
uvicorn app:app

# в другом терминале:
# отправка тестового GET-запроса, получение ответа {"status":"Alive"}
curl "http://127.0.0.1:8000/"

# отправка тестового POST-запроса, получение ответа {"score":12859673.47644087}
curl -X POST http://127.0.0.1:8000/predict \
     -H "Content-Type: application/json" \
     -d '{
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
     }'

# отправка запроса для получение случайного предсказания {"score": <...>}
curl "http://127.0.0.1:8000/random" 

# тестирование микросервиса в Swagger    
http://127.0.0.1:8000/docs

# если необходимо, переход в каталог services/app/
# запуск тестов, получение OK в случае успеха
python3 tests.py

# остановка ASGI-сервера в терминале, где он запущен по Ctrl-C
```

#### Этап 2. Контейнеризация микросервиса

```
# загрузка образа ОС с Python
docker pull python:3.11-slim

# если нужно, переход в папку services/
# создание контейнера с использованием файла Dockerfile
docker build -t my-fastapi-app:latest .

# и вывод списка образов для проверки
docker image ls

# запуск контейнера
docker run -d -p 8000:8000 my-fastapi-app:latest

# вывод списка запущенных контейнеров
docker container ps

# проверка работы микросервиса
curl "http://127.0.0.1:8000/"
curl "http://127.0.0.1:8000/random"

# остановка всех запущенных контейнеров
docker stop $(docker ps -a -q)

# создайте/проверьте наличие файла services/.env
# с заданной переменной окружения APP_PORT
# создание и запуск контейнера в режиме docker compose в фоновом (detached) режиме
docker compose up --build -d

# проверка работы микросервиса
curl "http://127.0.0.1:8000/"
curl "http://127.0.0.1:8000/random"

# остановка и удаление контейнера
docker compose down
```

#### Этап 3. Запуск сервисов для системы мониторинга

```
# сборка и запуск контейнера с обновленной конфигурацией в фоновом режиме
docker compose -f docker-compose-stage-3.yaml up --build -d

# проверка работы сервисов:    

# FastAPI-микросервис: 
http://127.0.0.1:8000/    

#Prometheus: 
http://127.0.0.1:9090/targets    

#Grafana: 
http://127.0.0.1:3000    

# остановка и удаление контейнера
docker compose -f docker-compose-stage-3.yaml down
```

#### Этап 4. Построение дашборда для мониторинга

```
# сборка и запуск контейнера с обновленной конфигурацией в фоновом режиме
docker compose -f docker-compose-stage-4.yaml up --build -d

# переход в папку со скриптами
cd app/
# запуск скрипта с имитацией нагрузки (1000 запросов)
python3 load_test.py

# Тестирование Grafana, Логин, пароль, Dashboards → My dashboard
http://127.0.0.1:3000    

# Прервать работу скрипта load_test.py можно по Ctrl-C

# Окончание работы с сервисом:
#переход в папку с Docker
cd ..
# остановка и удаление контейнера
docker compose -f docker-compose-stage-4.yaml down
```