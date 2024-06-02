FROM python:3.11-slim
LABEL author=${LABEL}
COPY . ./services
WORKDIR services
RUN pip3 install -r requirements.txt
EXPOSE ${APP_PORT}
#VOLUME /models
CMD uvicorn app:app --reload --port ${APP_PORT} --host 127.0.0.1