[![Build Status](https://travis-ci.org/JensGe/WebSch.svg?branch=master)](https://travis-ci.org/JensGe/WebSch)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=JensGe_WebSch&metric=alert_status)](https://sonarcloud.io/dashboard?id=JensGe_WebSch)
[![codecov](https://codecov.io/gh/JensGe/WebSch/branch/master/graph/badge.svg)](https://codecov.io/gh/JensGe/WebSch)


[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=JensGe_WebSch&metric=ncloc)](https://sonarcloud.io/dashboard?id=JensGe_WebSch)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=JensGe_WebSch&metric=bugs)](https://sonarcloud.io/dashboard?id=JensGe_WebSch)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=JensGe_WebSch&metric=code_smells)](https://sonarcloud.io/dashboard?id=JensGe_WebSch)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=JensGe_WebSch&metric=duplicated_lines_density)](https://sonarcloud.io/dashboard?id=JensGe_WebSch)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=JensGe_WebSch&metric=sqale_index)](https://sonarcloud.io/dashboard?id=JensGe_WebSch)


# WebSch Overview

A distributed Web Crawling Schedulercomponent to distribute URLs from Frontier to multiple Fetcher. 

Distributed Fetcher ask for new URL Lists per REST API call.

# Specification

## Python Packages

The project is build on the python packages FastAPI (https://fastapi.tiangolo.com/). 
FastApi itself is build on the following packages:
- Starlette (https://www.starlette.io/)
- pydantic (https://pydantic-docs.helpmanual.io/)

## Docker Image

The Docker Image provided by FastAPI is used as well
- tiangolo/uvicorn-gunicorn-fastapi:latest

## Deployment

The project is deployed on an AWS EC2 Ubuntu Machine. 

[Link to Online Docs] http://ec2-3-16-31-169.us-east-2.compute.amazonaws.com/docs

# Commands

Re-Run local Docker-Image (Windows PowerShell)

```shell script
docker ps -q | % { docker stop $_ }
docker pull dockerjens23/websch
docker build -t websch .
docker run -d -p 80:80 websch
```

Re-Run remote Docker-Image (Ubuntu)
```shell script
sudo docker stop $(sudo docker ps -q)
sudo docker pull dockerjens23/websch
sudo docker run -d -p 80:80 dockerjens23/websch
```

Get Loginfo of running Container
```shell script
sudo docker logs --follow $(sudo docker ps -q)
```


# Linux Server Admin Commands

```shell script
# disk free (human-readable)
df -h
# list all docker container (inactive, too)
sudo docker ps -a
```

# Start Docker with PostgreSQL Credentials as Environment Variables

```shell script
sudo docker run --env-file ./env.list -p: 80:80
```

## Environment Variables file
```shell script
POSTGRES_ENV_USER=...
POSTGRES_ENV_PW=...
POSTGRES_ENV_URI=...
```



