FROM python:3.11.5

WORKDIR /app

COPY . /app

COPY ../.env /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD [ "python", "app.py" ]