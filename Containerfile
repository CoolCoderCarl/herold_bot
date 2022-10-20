FROM python:3.9-alpine as builder

COPY ["bot.py", "/opt/"]
COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt
RUN apk add screen

FROM builder

CMD ["sleep", "15800000"]