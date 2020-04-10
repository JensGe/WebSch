from typing import List

from app.database import crawlers, db_models, pyd_models, sample_generator, frontier
from app.database import database
from app.common import http_exceptions as http_es


from fastapi import FastAPI, Depends, status, BackgroundTasks
from fastapi.routing import Response
from fastapi.middleware.gzip import GZipMiddleware

from sqlalchemy.orm import Session


db_models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="WebSch",
    description="A Scheduler for a distributed Web Fetcher System",
    version="0.2.3",
    redoc_url=None,
)

app.add_middleware(GZipMiddleware, minimum_size=1000)


# Dependency
def get_db():
    try:
        db = database.SessionLocal()
        yield db
    finally:
        db.close()


# Crawler
@app.get(
    "/crawlers/",
    response_model=List[pyd_models.Crawler],
    tags=["Crawler", "Development Tools"],
    summary="List all Crawlers",
    response_description="A List of all Crawler in the Database",
)
def read_crawler(db: Session = Depends(get_db)):
    """
    List all Crawler
    """
    all_crawler = crawlers.get_all_crawler(db)
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
    new_crawler = crawlers.create_crawler(db, crawler)
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
    updated_crawler = crawlers.update_crawler(db, crawler)
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

    patched_crawler = crawlers.patch_crawler(db, crawler)
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
    crawlers.delete_crawler(db, crawler)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post(
    "/frontiers/",
    status_code=status.HTTP_200_OK,
    response_model=pyd_models.FrontierResponse,
    tags=["Frontier"],
    summary="Get URL-Lists",
    response_description="The received URL-Lists",
)
def get_frontier(request: pyd_models.FrontierRequest, db: Session = Depends(get_db)):
    """
    Get a Sub List of the global Frontier

    - **crawler_uuid**: Your crawlers UUID
    - **amount** (default: 0): The amount of URL-Lists you want to receive
    - **length** (default: 0): The amount of URLs in each list
    - **tld** (optional): Filter the Response to contain only URLs of this TLD
    - **prio_mode** (default: None): tbd.
    - **part_mode** (default: None): tbd.
    """
    fqdn_frontier = frontier.get_fqdn_frontier(db, request)
    return fqdn_frontier


# Development Tools
@app.delete(
    "/database/", tags=["Development Tools"], summary="Delete Example Database",
)
async def delete_example_db(
    request: pyd_models.DeleteDatabase,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """
    Deletes the complete Example Database

    - **delete_url_refs** (default: false): Deletes all URL References
    - **delete_crawlers (default: false): Deletes all Crawler Records
    - **delete_urls (default: false): Deletes all URL Records
    - **delete_fqdns (default: false): Deletes all FQDN Records
    - **delete_reserved_fqdns (default: false): Deletes all Reservations
    """

    background_tasks.add_task(database.reset, db, request)

    return Response(status_code=status.HTTP_202_ACCEPTED)


@app.post("/database/", tags=["Development Tools"], summary="Generate Example Database")
async def generate_example_db(
    request: pyd_models.GenerateRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """
    Creates and uploads Example-Data to the Database for testing purposes.
    Includes Crawler, FQDNs and URLs.

    - **crawler_amount** (default: 3): Number of Crawler to generate
    - **fqdn_amount** (default: 20): Number of Web Sites to generate
    - **min_url_amount** (default: 10): Minimum Pages per Web Site
    - **max_url_amount** (default: 100): Maximum Pages per Web Site
    - **visited_ratio** (default: 1.0): Pages which have been visited
    - **connection_amount** (default: 0): Amount of incoming Connections per Page
    - ~~**blacklisted_ratio** (default: 0): Percentage of blacklisted Pages~~
    - ~~**bot_excluded_ratio** (default. 0): Percentage of bot-excluded Pages~~

    """
    if request.min_url_amount > request.max_url_amount:
        http_es.raise_http_400(request.min_url_amount, request.max_url_amount)

    background_tasks.add_task(
        sample_generator.create_sample_crawler, db, amount=request.crawler_amount,
    )

    background_tasks.add_task(
        sample_generator.create_sample_frontier,
        db,
        fqdns=request.fqdn_amount,
        min_url_amount=request.min_url_amount,
        max_url_amount=request.max_url_amount,
        visited_ratio=request.visited_ratio,
        connection_amount=request.connection_amount,
    )

    return Response(status_code=status.HTTP_202_ACCEPTED)


@app.get(
    "/stats/",
    response_model=pyd_models.StatsResponse,
    tags=["Development Tools"],
    summary="Get Statistics for Database",
)
def get_db_stats(db: Session = Depends(get_db)):
    """
    Returns Statistic from current Database Status
    """

    return frontier.get_db_stats(db)
