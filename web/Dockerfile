FROM python:2
RUN apt-get update && apt-get install -y nginx

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

COPY nginx.conf /etc/nginx/sites-enabled/default

RUN apt-get install -y sqlite3 libsqlite3-dev
RUN mkdir /db
RUN /usr/bin/sqlite3 /db/test.db

CMD ["/bin/bash", "start.sh"]
EXPOSE 80
