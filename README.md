# Network security project for phishing data

## Setup file creation

## Environment

El environment se crea de manera local con:
```
conda create -p .venv python=3.10
```
y se activa con:
```
conda activate ./.venv
```
Después, se pueden instalar las librerias.

## ETL Pipeline


el vido 127 explica lo que es un etl. hay que explicarlo aqui.

![alt text](image.png)

para eso se crea un clsuter en mongodb

el primer paso es la ingestion desde el csv a mongo db.

luego viene la data ingestion part

![alt text](image-1.png)


## data validation

data drif, data schema.

## Variables de entorno
en el archivo .env deberá haber las siguientes variables
MONGO_DB_URL