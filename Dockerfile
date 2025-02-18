FROM python:3.7-alpine

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk add protobuf-dev && \
 apk --purge del .build-deps


COPY . /code/
RUN protoc  -I=./protomodels --python_out=./protomodels ./protomodels/packets.proto
ENTRYPOINT python run.py