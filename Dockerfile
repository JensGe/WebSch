FROM tiangolo/uvicorn-gunicorn-fastapi:latest

RUN pip install pydantic[email]
RUN pip install pytest
RUN pip install sqlalchemy

COPY ./app app
