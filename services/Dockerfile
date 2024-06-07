FROM python:3.11-slim
COPY . /services
RUN pip3 install -r services/requirements.txt
WORKDIR  /services/app
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]