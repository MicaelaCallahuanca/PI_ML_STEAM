FROM tiangolo/uvicorn-gunicorn:python3.11-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

ENV CSV_FILE_PATH=C:/Users/micai/OneDrive/Escritorio/PI_ML_STEAM/dataframe_final.csv

EXPOSE 8000

CMD [ "uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]