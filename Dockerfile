FROM python:3.10-slim

WORKDIR /app

COPY /src/main.py /app
COPY /src/tictactoe.py /app

COPY .env /app
COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
