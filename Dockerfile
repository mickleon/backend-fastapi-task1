FROM python:3.13.13-alpine

ENV PATH="${PATH}:/root/.local/bin"
COPY ./src /app/src
COPY main.py /app/
COPY entrypoint.sh /app/
COPY alembic /app/alembic
COPY alembic.ini /app/
COPY requirements.txt /app/
COPY sqlite.db /app/
COPY ./images /images

ENV PYTHONPATH /app/src
WORKDIR /app
RUN pip install -r ./requirements.txt
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000
