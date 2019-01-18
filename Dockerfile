FROM python:3.7.2-alpine3.8

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apk update && \
    apk upgrade && \
    apk add bash

ADD requirements.txt .
RUN pip3 install -r requirements.txt

ADD . .
RUN python3 setup.py install

ADD entrypoint.sh /entrypoint.sh

CMD ["/entrypoint.sh"]