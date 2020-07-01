from app.database import fetchers, db_models, pyd_models, sample_generator, frontier
from app.database import database
from app.common import http_exceptions as http_es

from fastapi import FastAPI, Depends, status, BackgroundTasks
from fastapi.routing import Response
from fastapi.middleware.gzip import GZipMiddleware

import os
from sqlalchemy.orm import Session
from typing import List

import logging

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

db_models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="WebSch",
    description="A Scheduler for a distributed Web Fetcher System",
    version="0.3.2",
    redoc_url=None,
)

app.add_middleware(GZipMiddleware, minimum_size=150)


# Dependency
def get_db():
    try:
        db = database.SessionLocal()
        yield db
    finally:
        db.close()


# Fetcher
@app.get(
    "/fetchers/",
    response_model=List[pyd_models.Fetcher],
    tags=["Fetcher", "Development Tools"],
    summary="List all Fetcher",
    response_description="A List of all Fetcher in the Database",
)
def read_fetcher(db: Session = Depends(get_db)):
    """
    List all Fetcher
    """
    all_fetcher = fetchers.get_all_fetcher(db)
    return all_fetcher


@app.post(
    "/fetchers/",
    status_code=status.HTTP_201_CREATED,
    response_model=pyd_models.Fetcher,
    response_model_exclude_unset=True,
    tags=["Fetcher"],
    summary="Create a Fetcher",
    response_description="Information about the newly created Fetcher",
)
def register_fetcher(
    fetcher: pyd_models.CreateFetcher,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """
    Create a Fetcher

    - **contact**: The e-mail address of the fetchers owner
    - **name**: A unique name for the fetcher per contact
    - **location** (optional): The location where the fetcher resides
    - **pref_tld** (optional): The Top-Level-Domain, which the fetcher prefers to crawl
    """
    new_fetcher = fetchers.create_fetcher(db, fetcher)

    if database.fqdn_hash_activated(db):
        background_tasks.add_task(database.refresh_fqdn_hashes, db)

    return new_fetcher


@app.put(
    "/fetchers/",
    status_code=status.HTTP_200_OK,
    response_model=pyd_models.Fetcher,
    response_model_exclude_unset=True,
    tags=["Fetcher"],
    summary="Reset fetcher information",
    response_description="Information about the fetcher",
)
def update_crawler(fetcher: pyd_models.UpdateFetcher, db: Session = Depends(get_db)):
    """
    Update a Fetcher - Unprovided Fields will be reset

    - **fetcher_uuid**: The fetchers UUID to update
    - **contact**: The e-mail address of the fetchers owner
    - **location** (optional): The location where the fetcher resides
    - **pref_tld** (optional): The Top-Level-Domain, which the fetcher prefers to crawl
    """
    updated_fetcher = fetchers.update_fetcher(db, fetcher)
    return updated_fetcher


@app.patch(
    "/fetchers/",
    status_code=status.HTTP_200_OK,
    response_model=pyd_models.Fetcher,
    response_model_exclude_unset=True,
    tags=["Fetcher"],
    summary="Update a fetcher",
    response_description="Information about the updated created fetcher",
)
def patch_fetcher(fetcher: pyd_models.UpdateFetcher, db: Session = Depends(get_db)):
    """
    Update a Fetcher -  Unprovided Fields will be ignored

    - **fetcher_uuid**: The fetchers UUID to update
    - **contact**: The e-mail address of the fetchers owner
    - **location** (optional): The location where the fetcher resides
    - **pref_tld** (optional): The Top-Level-Domain, which the fetcher prefers to crawl
    """

    patched_fetcher = fetchers.patch_fetcher(db, fetcher)
    return patched_fetcher


@app.delete(
    "/fetchers/",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Fetcher"],
    summary="Delete a Fetcher",
    response_description="No Content",
)
def delete_fetcher(
    fetcher: pyd_models.DeleteFetcher,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """
    Delete a specific Fetcher

    - **uuid**: UUID of the fetcher, which has to be deleted
    """
    fetchers.delete_fetcher(db, fetcher)

    if database.fqdn_hash_activated(db):
        background_tasks.add_task(database.refresh_fqdn_hashes, db)

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

    - **fetcher_uuid**: Your fetchers UUID
    - **amount** (default: 10): The amount of URL-Lists you want to receive
    - **length** (default: 0 = No Limit): The amount of URLs in each list
    - **long_term_prio_mode** (default: random): The modus in which the FQDN Frontier is prioritized
    - **long_term_part_mode** (default: none): The modus in which the FQDN Frontier is partitioned
    - **short_term_prio_mode** (default: random): The modus in which the URL Frontier is prioritized
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
    - **delete_fetchers (default: false): Deletes all Fetcher Records
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
    Includes Fetcher, FQDNs and URLs.

    - **fetcher_amount** (default: 3): Number of Fetcher to generate
    - **fqdn_amount** (default: 20): Number of Web Sites to generate
    - **min_url_amount** (default: 10): Minimum Pages per Web Site
    - **max_url_amount** (default: 100): Maximum Pages per Web Site
    - **visited_ratio** (default: 0.0): Pages which have been visited
    - **connection_amount** (default: 0): Amount of incoming Connections per Page
    - **fixed_crawl_delay** (default: None): Adjust the Crawl Delay for all Web Sites.
        Will be a distributed-randomized Value when no Value is chosen.
    """
    if request.min_url_amount > request.max_url_amount:
        http_es.raise_http_400(request.min_url_amount, request.max_url_amount)

    background_tasks.add_task(
        sample_generator.create_sample_fetcher, db, amount=request.fetcher_amount,
    )

    background_tasks.add_task(sample_generator.create_sample_frontier, db, request)

    if database.fqdn_hash_activated(db):
        background_tasks.add_task(database.refresh_fqdn_hashes, db)

    return Response(status_code=status.HTTP_202_ACCEPTED)


@app.get(
    "/stats/",
    response_model=pyd_models.StatsResponse,
    tags=["Development Tools"],
    summary="Get Statistics for Database",
)
def get_db_stats(db: Session = Depends(get_db)):
    """
    Returns Statistics from current Database Status
    """

    return frontier.get_db_stats(db)


@app.get(
    "/urls/",
    response_model=pyd_models.RandomUrls,
    tags=["Development Tools"],
    summary="Get Random Urls from Database",
)
def get_random_urls(request: pyd_models.GetRandomUrls, db: Session = Depends(get_db)):
    """
    Returns a requested amount of random URLs from the Database
    """
    return frontier.get_random_urls(db, request)


@app.get(
    "/settings/",
    response_model=pyd_models.FetcherSettings,
    tags=["Development Tools"],
    summary="Get Settings for Fetcher",
)
def get_fetcher_settings(db: Session = Depends(get_db)):
    """
    Returns the latest settings for every fetcher
    """
    return frontier.get_fetcher_settings(db)


@app.patch(
    "/settings/",
    response_model=pyd_models.FetcherSettings,
    tags=["Development Tools"],
    summary="Set Settings for Fetcher",
)
def create_fetcher_settings(
    request: pyd_models.FetcherSettings,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """
    Returns the latest settings for every fetcher
    """

    updated_fetcher_settings = frontier.set_fetcher_settings(request, db)

    if database.fqdn_hash_activated(db):
        background_tasks.add_task(database.refresh_fqdn_hashes, db)

    return updated_fetcher_settings
