from typing import List

from app.common import example_generator as ex
# from app.common import models

from app.database import crud, models, schemas
from app.database.database import SessionLocal, engine

from fastapi import FastAPI, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status


models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="WebSch",
    description="A Scheduler for a distributed Web Fetcher System",
    version="0.0.3",
    redoc_url=None
)


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# Crawler

@app.get(
    "/crawler/",
    response_model=List[schemas.Crawler],
    tags=["Crawler"],
    summary="List all created Crawlers",
    response_description="A List of all Crawler in the Database"
)
def read_crawler(db: Session = Depends(get_db)):
    """
    List all Crawler

    - **crawler_uuid**
    """
    all_crawler = crud.get_all_crawler(db)
    return all_crawler


@app.post(
    "/crawler/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Crawler,
    response_model_exclude_unset=True,
    tags=["Crawler"],
    summary="Create a crawler",
    response_description="Information about the newly created crawler"
)
def register_crawler(
    crawler: schemas.CreateCrawler, db: Session = Depends(get_db)
):
    """
    Create a Crawler

    - **contact**: The e-mail address of the crawlers owner
    - **name**: A unique Name per Owner
    - **location** (optional): The location where the crawler resides
    - **pref_tld** (optional): The Top-Level-Domain, which the crawler prefers to crawl
    """
    new_crawler = crud.create_crawler(db, crawler)
    return new_crawler


@app.delete(
    "/crawler/",
    status_code=status.HTTP_200_OK,
    tags=["Crawler"],
    summary="Delete a Crawler",
    response_description="The deleted Crawler"
)
def delete_crawler(
    crawler: schemas.DeleteCrawler, db: Session = Depends(get_db)
):
    """
    Delete a specific Crawler

    - **uuid**: UUID of the crawler, which has to be deleted
    """
    deleted_crawler = crud.delete_crawler(db, crawler)
    return deleted_crawler


@app.delete(
    "/all_crawler/",
    status_code=status.HTTP_200_OK,
    tags=["Crawler"],
    summary="Delete all Crawler"
)
def delete_all_crawler(db: Session = Depends(get_db)
):
    """
    Delete a specific Crawler

    - **uuid**: UUID of the crawler, which has to be deleted
    """
    deleted_crawler = crud.delete_all_crawler(db)
    return deleted_crawler

############################
# Before DB
#
# @app.put(
#     "/crawler/",
#     status_code=200,
#     response_model=models.Crawler,
#     response_model_exclude_unset=True,
#     tags=["Crawler"],
#     summary="Reset crawler information",
#     response_description="Information about the crawler"
# )
# async def update_crawler(
#     crawler: models.Crawler = Body(
#         ...,
#         example={
#             "uuid": "12345678-90ab-cdef-0000-000000000000",
#             "contact": "jens@example.com",
#             "location": "USA, Texas, Houston",
#             "pref_tld": "com",
#         },
#     )
# ):
#     """
#     Update a Crawler - Unprovided Fields will be reset
#
#     - **crawler_uuid**: The crawlers UUID to update
#     - **contact**: The e-mail address of the crawlers owner
#     - **location** (optional): The location where the crawler resides
#     - **pref_tld** (optional): The Top-Level-Domain, which the crawler prefers to crawl
#     """
#     updated_crawler = ex.update_crawler(crawler)
#     return updated_crawler
#
#
#
# @app.patch(
#     "/crawler/",
#     status_code=200,
#     response_model=models.Crawler,
#     response_model_exclude_unset=True,
#     tags=["Crawler"],
#     summary="Update a crawler",
#     response_description="Information about the updated created crawler"
# )
# async def update_crawler(
#     crawler: models.Crawler = Body(
#         ...,
#         example={
#             "uuid": "12345678-90ab-cdef-0000-000000000000",
#             "contact": "jens@example.com",
#             "location": "USA, Texas, Houston",
#             "pref_tld": "com",
#         },
#     )
# ):
#     """
#     Update a Crawler -  Unprovided Fields will be ignored
#
#     - **crawler_uuid**: The crawlers UUID to update
#     - **contact**: The e-mail address of the crawlers owner
#     - **location** (optional): The location where the crawler resides
#     - **pref_tld** (optional): The Top-Level-Domain, which the crawler prefers to crawl
#     """
#     updated_crawler = ex.update_crawler(crawler)
#     return updated_crawler
#
#
# @app.post(
#     "/frontiers/",
#     response_model=models.Frontier,
#     tags=["Frontier"],
#     summary="Get URL-Lists",
#     response_description="The received URL-Lists",
# )
# async def get_frontier(
#     request: models.CrawlRequest = Body(
#         ...,
#         example={
#             "crawler_uuid": "12345678-90ab-cdef-0000-000000000000",
#             "amount": 5,
#             "length": 3,
#             "tld": None,
#         }
#         )
# ):
#     """
#     Get a Sub List of the global Frontier
#
#     - **crawler_uuid**: Your crawlers UUID
#     - **amount**: The amount of URL-Lists you want to receive
#     - **length**: The amount of URLs in each list
#     - **tld** (optional): Filter the Response to contain only URLs of this Top-Level-Domain
#     """
#     example_urls = ex.generate_frontier(
#         request.crawler_uuid, request.amount, request.length, request.tld
#     )
#
#     return example_urls


