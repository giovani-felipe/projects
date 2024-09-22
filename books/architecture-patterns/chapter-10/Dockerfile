FROM python:alpine

COPY requirements.txt /tmp
RUN pip install --no-cache-dir poetry

RUN mkdir -p /src
COPY src/ /src/
RUN pip install -e /src
COPY tests/ /tests/

WORKDIR /src
RUN python -m poetry install --no-cache --only main
ENV FLASK_APP=allocation/entrypoints/flask_app.py FLASK_DEBUG=1 PYTHONUNBUFFERED=1
CMD flask run --host=0.0.0.0 --port=80