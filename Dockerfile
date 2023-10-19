FROM python:3.11-slim

WORKDIR /cobra

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY *.py /cobra
COPY ./config/ /cobra/config/

RUN pip install sockets && pip install requests

CMD ["python", "cobra-integration-server.py"]