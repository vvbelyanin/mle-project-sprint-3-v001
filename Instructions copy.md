## Инструкции по запуску микросервиса
#### Этап 1. Написание FastAPI-микросервиса

:open_file_folder: mle-project-sprint-3-v001/


```
# апгрейд менеджера пакетов
python3 -m pip install --upgrade pip

# создание виртуального окружения в папке .mle-sprint3-venv
python3 -m venv .mle-sprint3-venv

# активация виртуального окружения
source .mle-sprint3-venv/bin/activate

# установка необходимых пакетов
pip install -r requirements.txt

# файловая структура проекта
```
:open_file_folder: mle-project-sprint-3-v001/

```
# модель находится в файле sevices/models/fitted_model.pkl, ее можно повторно генерировать
# перед запуском создайте/проверьте наличие /.env файла в каталоге проекта со следущими переменными:
# DB_DESTINATION_HOST
# DB_DESTINATION_PORT
# DB_DESTINATION_NAME
# DB_DESTINATION_USER
# DB_DESTINATION_PASSWORD
cd services/models/
python create_model.py

# если необходимо, вернуться в основную папку
# переход в папку со скриптами
cd ../app/
# или 
cd services/app/
```

Код класса-обработчика `FastApiHandler` был реализован в файле services/app/[fastapi_handler.py](https://github.com/vvbelyanin/mle-project-sprint-3-v001/blob/main/services/app/fastapi_handler.py).
Метод `validate_params()` класса проверяет параметры модели на соответствие списку требуемых полей.     
Функция `gen_random_data()` генерирует случайные параметры модели.
     
Код микросервиса реализован в services/app/[app.py](https://github.com/vvbelyanin/mle-project-sprint-3-v001/blob/main/services/app/app.py).
Определено три эндпоинта:    
/ - возвращение статуса "Alive"    
/predict - возврат значения предсказания модели для заданных входных параметров    
/random - возврат значения предсказания модели для случайных параметров    
```
# проверка кода микросервиса с возвратом тестового предсказания
python fastapi_handler.py

# запуск ASGI-сервера
# со значениями по умолчанию --host 127.0.0.1 --port 8000
uvicorn app:app

# переход в другой терминал
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
```

По адресу http://127.0.0.1:8000/docs  - тестирование микросервиса в Swagger    
GET - ресурс "/" выдает "Alive"    
GET - ресурс "/random" выдает случайный score    
POST - ресурс "/predict" выдает score модели либо сообщения об ошибках в зависимости от входных данных:
 - {"Error": "Problem with parameters"}
 - {"Error": "Problem with request"}
 - 422 Error: Unprocessable Entity в случае ошибки в JSON

Для проверки работы микросервиса создан скрипт sevices/app/[tests.py](https://github.com/vvbelyanin/mle-project-sprint-3-v001/blob/main/services/app/tests.py), тестирующий все эндпоинты и различные варианты ошибок входных параметров модели.

```

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

# создайте/проверьте наличие файла services/.env с заданной переменной окружения APP_PORT
# создание и запуск контейнера в режиме docker compose в фоновом (detached) режиме
# используется файл docker-compose.yaml
docker compose up --build -d

# проверка работы микросервиса
curl "http://127.0.0.1:8000/"
curl "http://127.0.0.1:8000/random"

# остановка и удаление контейнера
docker compose down
```

#### Этап 3. Запуск сервисов для системы мониторинга
  
- На этом этапе в [docker-compose.yaml](https://github.com/vvbelyanin/mle-project-sprint-3-v001/blob/main/services/docker-compose.yaml) добавлено описание сервисов prometheus и grafana, 
новый файл: services/[docker-compose-stage-3.yaml](https://github.com/vvbelyanin/mle-project-sprint-3-v001/blob/main/services/docker-compose-stage-3.yaml)    
- Новый Dockerfile: services/[Dockerfile-stage-3](https://github.com/vvbelyanin/mle-project-sprint-3-v001/blob/main/services/Dockerfile-stage-3)    
- Обновленный код микросервиса находится в файле services/app/[app-stage-3.py](https://github.com/vvbelyanin/mle-project-sprint-3-v001/blob/main/services/app/app-stage-3.py) с добавленным экспортёром с помощью `prometheus_fastapi_instrumentator`
- Создан файл конфигурации prometheus services/prometheus/prometheus.yml, предусмотрено его сохранение в томе Docker
- Создан каталог services/grafana/ (см. этап 4)
- В файл services/.env помещены значения переменных `GRAFANA_USER`, `GRAFANA_PASS`
```
# сборка и запуск контейнера с обновленной конфигурацией в фоновом режиме
docker compose -f docker-compose-stage-3.yaml up --build -d
```
После запуска контейнера можно проверить работу сервисов по адресам:    
FastAPI-микросервис: http://127.0.0.1:8000/    
Prometheus: http://127.0.0.1:9090/targets    
Grafana: http://127.0.0.1:3000    
В интерфейсе Grafana нужно ввести  логин и пароль и откроется главная страница
```
# остановка и удаление контейнера
docker compose -f docker-compose-stage-3.yaml down
```

#### Этап 4. Построение дашборда для мониторинга

- В файле [Monitoring.md](https://github.com/vvbelyanin/mle-project-sprint-3-v001/blob/main/Monitoring.md) приведены набор и описание ML-метрики реального времени, используемые для мониторинга работы микросервиса
- В файл с кодом микросервиса добавлены метрики prometheus_client Gauge, Histogram, обновления сохранены в services/app/[app-stage-4.py](https://github.com/vvbelyanin/mle-project-sprint-3-v001/blob/main/services/app/app-stage-4.py)
- Обновлены и сохранены файлы services/[Dockerfile-stage-4](https://github.com/vvbelyanin/mle-project-sprint-3-v001/blob/main/services/Dockerfile-stage-4) и services/[docker-compose-stage-4.yaml](https://github.com/vvbelyanin/mle-project-sprint-3-v001/blob/main/services/docker-compose-stage-4.yaml)
- В файле services/app/[load_test.py](https://github.com/vvbelyanin/mle-project-sprint-3-v001/blob/main/services/app/load_test.py) содержится код, имитирующий нагрузку на сервис, а именно обращения к ресурсам /metrics и /random с интервалами до 1 с
- В код микросервиса добавлен код для имитации ошибок с заданной вероятностью, а также задержки до 1 с:
```
raise HTTPException(status_code=500, detail="Random failure for testing purposes")
time.sleep(random.random())
```
- Для гарантии сохранения информации при каждом перестроении контейнера, информация об источнике данных prometheus и дашборде сохраняется средствами Grafana provisioning. Для этого созданы файлы в соответствующих каталогах: /services/grafana/provisioning/dashboards/[dashboard.yaml](https://github.com/vvbelyanin/mle-project-sprint-3-v001/blob/main/services/grafana/provisioning/dashboards/dashboard.yaml) и /services/garfana/provisioning/datasources/[datasource.yaml](https://github.com/vvbelyanin/mle-project-sprint-3-v001/blob/main/services/grafana/provisioning/datasources/datasource.yaml)
- Сохраненный дашборд находится в файле /services/garfana/provisioning/dashboards/[dashboard.json](https://github.com/vvbelyanin/mle-project-sprint-3-v001/blob/main/services/grafana/provisioning/dashboards/dashboard.json)
- Скриншот дашборда находится в файле /services/garfana/provisioning/dashboards/[screenshot.jpg](https://github.com/vvbelyanin/mle-project-sprint-3-v001/blob/main/services/grafana/provisioning/dashboards/screenshot.jpg) и продублирован в [Monitoring.md](https://github.com/vvbelyanin/mle-project-sprint-3-v001/blob/main/Monitoring.md)
```
# сборка и запуск контейнера с обновленной конфигурацией в фоновом режиме
docker compose -f docker-compose-stage-4.yaml up --build -d

# переход в папку со скриптами
cd app/
# запуск скрипта с имитацией нагрузки (1000 запросов)
python3 load_test.py
```
Тестирование Grafana: http://127.0.0.1:3000    
Нужно ввести  логин и пароль, затем выбрать в боковом меню: Dashboards → My dashboard
Описание дашборда см. в [Monitoring.md](https://github.com/vvbelyanin/mle-project-sprint-3-v001/blob/main/Monitoring.md)
Прервать работу скрипта load_test.py можно по Ctrl-C

После окончания работы с сервисом:
```
#переход в папку с Docker
cd ..
# остановка и удаление контейнера
docker compose -f docker-compose-stage-4.yaml down
```