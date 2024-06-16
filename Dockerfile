FROM python:3.10-slim
WORKDIR /app

COPY . /app

VOLUME /app/data
RUN pip3 install -r requirements.txt

RUN chmod +x /app/main.py


CMD ["python3","/app/main.py"]
