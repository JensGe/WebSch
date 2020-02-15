FROM tiangolo/uvicorn-gunicorn-fastapi:latest

RUN pip install pydantic[email]

COPY ./app app
