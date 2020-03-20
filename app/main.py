from typing import List

from app.database import crud, db_models, pyd_models, sample_generator
from app.database.database import SessionLocal, engine


from fastapi import FastAPI, Body, Depends, HTTPException
from fastapi.routing import Response
from fastapi.middleware.gzip import GZipMiddleware

from sqlalchemy.orm import Session
from starlette import status

db_models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="WebSch",
    description="A Scheduler for a distributed Web Fetcher System",
    version="0.1.3",
    redoc_url=None,
)

app.add_middleware(GZipMiddleware, minimum_size=500)


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# Crawler
@app.get(
    "/crawlers/",
    response_model=List[pyd_models.Crawler],
    tags=["Crawler"],
    summary="List all Crawlers",
    response_description="A List of all Crawler in the Database",
)
def read_crawler(db: Session = Depends(get_db)):
    """
    List all Crawler
    """
    all_crawler = crud.get_all_crawler(db)
    return all_crawler


@app.post(
    "/crawlers/",
    status_code=status.HTTP_201_CREATED,
    response_model=pyd_models.Crawler,
    response_model_exclude_unset=True,
    tags=["Crawler"],
    summary="Create a crawler",
    response_description="Information about the newly created crawler",
)
def register_crawler(crawler: pyd_models.CreateCrawler, db: Session = Depends(get_db)):
    """
    Create a Crawler

    - **contact**: The e-mail address of the crawlers owner
    - **name**: A unique Name per Owner
    - **name**: A unique name for the crawler per contact
    - **location** (optional): The location where the crawler resides
    - **pref_tld** (optional): The Top-Level-Domain, which the crawler prefers to crawl
    """
    new_crawler = crud.create_crawler(db, crawler)
    return new_crawler


@app.put(
    "/crawlers/",
    status_code=status.HTTP_200_OK,
    response_model=pyd_models.Crawler,
    response_model_exclude_unset=True,
    tags=["Crawler"],
    summary="Reset crawler information",
    response_description="Information about the crawler",
)
def update_crawler(crawler: pyd_models.UpdateCrawler, db: Session = Depends(get_db)):
    """
    Update a Crawler - Unprovided Fields will be reset

    - **crawler_uuid**: The crawlers UUID to update
    - **contact**: The e-mail address of the crawlers owner
    - **location** (optional): The location where the crawler resides
    - **pref_tld** (optional): The Top-Level-Domain, which the crawler prefers to crawl
    """
    updated_crawler = crud.update_crawler(db, crawler)
    return updated_crawler


@app.patch(
    "/crawlers/",
    status_code=status.HTTP_200_OK,
    response_model=pyd_models.Crawler,
    response_model_exclude_unset=True,
    tags=["Crawler"],
    summary="Update a crawler",
    response_description="Information about the updated created crawler",
)
def patch_crawler(crawler: pyd_models.UpdateCrawler, db: Session = Depends(get_db)):
    """
    Update a Crawler -  Unprovided Fields will be ignored

    - **crawler_uuid**: The crawlers UUID to update
    - **contact**: The e-mail address of the crawlers owner
    - **location** (optional): The location where the crawler resides
    - **pref_tld** (optional): The Top-Level-Domain, which the crawler prefers to crawl
    """

    patched_crawler = crud.patch_crawler(db, crawler)
    return patched_crawler


@app.delete(
    "/crawlers/",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Crawler"],
    summary="Delete a Crawler",
    response_description="No Content",
)
def delete_crawler(crawler: pyd_models.DeleteCrawler, db: Session = Depends(get_db)):
    """
    Delete a specific Crawler

    - **uuid**: UUID of the crawler, which has to be deleted
    """
    crud.delete_crawler(db, crawler)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post(
    "/frontiers/",
    status_code=status.HTTP_200_OK,
    response_model=pyd_models.FrontierResponse,
    tags=["Frontier"],
    summary="Get URL-Lists",
    response_description="The received URL-Lists",
)
def get_frontier(request: pyd_models.CrawlRequest, db: Session = Depends(get_db)):
    """
    Get a Sub List of the global Frontier

    - **crawler_uuid**: Your crawlers UUID
    - **amount** (default: 1): The amount of URL-Lists you want to receive
    - **length** (default: 10): The amount of URLs in each list
    - **tld** (optional): Filter the Response to contain only URLs of this Top-Level-Domain
    """
    fqdn_frontier = crud.get_fqdn_frontier(db, request)
    return fqdn_frontier


@app.post(
    "/database/",
    response_model=pyd_models.GenerateResponse,
    tags=["Development Tools"],
    summary="Generate Example Database",
)
def generate_example_db(
    request: pyd_models.GenerateRequest, db: Session = Depends(get_db)
):
    """
    Cleans the Database and generates a new example Database for testing purposes
    """
    crud.reset(db)
    sample_data = {}

    sample_crawler = sample_generator.create_sample_crawler(
        db, amount=request.crawler_amount
    )
    sample_data["crawler"] = sample_crawler

    sample_frontier = sample_generator.create_sample_frontier(
        db,
        fqdns=request.fqdn_amount,
        min_url_amount=request.min_url_amount,
        max_url_amount=request.max_url_amount,
    )
    sample_data["frontier"] = sample_frontier["frontier"]
    sample_data["url_list"] = sample_frontier["url_list"]
    return sample_data
