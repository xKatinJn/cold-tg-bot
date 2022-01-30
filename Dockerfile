FROM python:3.8

COPY . /cold-tg-bot
WORKDIR /cold-tg-bot

RUN pip install --no-cache-dir -r requirements.txt

ENV BOT_API_TOKEN=YOUR_BOT_TOKEN
EXPOSE 80

CMD [ "python", "main.py" ]
