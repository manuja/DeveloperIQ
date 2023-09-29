# Dockerfile

FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip install requests
RUN pip3 install pymysql


COPY . .

EXPOSE 5000

CMD ["python", "app.py"]