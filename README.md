# WebSch Overview

A distributed Web Crawling Schedulercomponent to distribute URLs from Frontier to multiple Fetcher. 

Distributed Fetcher ask for new URL Lists per REST API call.

# Techniques

The project runs on the following python packages (with the also following subdependencies):
- FastAPI (https://fastapi.tiangolo.com/) 
  - Starlette (https://www.starlette.io/)
    - uvicorn (https://www.uvicorn.org/).
  - pydantic (https://pydantic-docs.helpmanual.io/)

# Docker

- tiangolo/uvicorn-gunicorn-fastapi:latest

# Server Run

```code
uvicorn websch.app:app --reload
```


