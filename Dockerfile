FROM python:3.10

RUN pip freeze > requirements.txt
RUN pip  install -r requirements.txt
WORKDIR . /app
EXPOSE 8000
COPY ./app /app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
