## setting the base image 
FROM python:3.8

## setting the workdir
WORKDIR /app

## copy the dependency file
COPY requirements.txt .

## install dependencies
RUN pip install -r requirements.txt

## copy the whole code
COPY . .

## make file executable
RUN chmod +x run.sh

## start the server 
CMD ["bash", "run.sh"]
