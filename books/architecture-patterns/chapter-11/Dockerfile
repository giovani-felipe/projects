FROM python:alpine

RUN pip install --no-cache-dir poetry
COPY dist/architecture_patterns-*.tar.gz /tmp
RUN pip install /tmp/architecture_patterns-*.tar.gz
