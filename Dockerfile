FROM python:3.11

WORKDIR /cobra

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY *.py /cobra

RUN pip install sockets
RUN pip install requests

CMD ["python", "server_demo.py"]