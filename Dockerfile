FROM python:3.8

ENV PYTHONUNBUFFERED 1

WORKDIR /basic_linguistic_indicators

RUN mkdir ./dist

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8080

ENV PORT 8080

CMD flask run --host=0.0.0.0 -p $PORT
