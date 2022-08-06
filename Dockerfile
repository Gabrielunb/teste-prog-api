FROM python:3.10

WORKDIR /app
COPY ./app/pedidos.json ./app/pedidos.json
COPY ./requirements.txt ./app/requirements.txt
RUN pip  install -r ./app/requirements.txt

EXPOSE 8000
COPY ./app /app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]