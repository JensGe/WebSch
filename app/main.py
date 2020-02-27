# internal packages
from app.common import example_generator as ex
from app.common import models

# external packages
from fastapi import FastAPI, Body, BackgroundTasks
from starlette.status import HTTP_201_CREATED


app = FastAPI(
    title="WebSch",
    description="A Scheduler for a distributed Web Fetcher System",
    version="0.0.1",
    redoc_url=None
)


@app.post(
    "/frontiers/",
    response_model=models.Frontier,
    tags=["Frontier"],
    summary="Get URL-Lists",
    response_description="The received URL-Lists",
)
async def get_frontier(
    request: models.CrawlRequest = Body(
        ...,
        example={
            "crawler_uuid": "12345678-90ab-cdef-0000-000000000000",
            "amount": 5,
            "length": 3,
            "tld": None,
        }
        )
):
    """
    Get a Sub List of the global Frontier

    - **crawler_uuid**: Your crawlers UUID
    - **amount**: The amount of URL-Lists you want to receive
    - **length**: The amount of URLs in each list
    - **tld** (optional): Filter the Response to contain only URLs of this Top-Level-Domain
    """
    example_urls = ex.generate_frontier(
        request.crawler_uuid, request.amount, request.length, request.tld
    )

    return example_urls


@app.post(
    "/crawler/",
    status_code=HTTP_201_CREATED,
    response_model=models.Crawler,
    response_model_exclude_unset=True,
    tags=["Crawler"],
    summary="Create a crawler",
    response_description="Information about the newly created crawler"
)
async def register_crawler(
    crawler: models.Crawler = Body(
        ...,
        example={
            "contact": "jens@example.com",
            "location": "Germany, Baden-Württemberg, Stuttgart",  # ToDo Location Codes verwenden
            "pref_tld": "de",
        },
    )
):
    """
    Create a Crawler

    - **contact**: The e-mail address of the crawlers owner
    - **location** (optional): The location where the crawler resides
    - **pref_tld** (optional): The Top-Level-Domain, which the crawler prefers to crawl
    """
    new_crawler = ex.create_new_crawler(crawler)
    return new_crawler


@app.put(
    "/crawler/",
    status_code=200,
    response_model=models.Crawler,
    response_model_exclude_unset=True,
    tags=["Crawler"],
    summary="Reset crawler information",
    response_description="Information about the crawler"
)
async def update_crawler(
    crawler: models.Crawler = Body(
        ...,
        example={
            "uuid": "12345678-90ab-cdef-0000-000000000000",
            "contact": "jens@example.com",
            "location": "USA, Texas, Houston",
            "pref_tld": "com",
        },
    )
):
    """
    Update a Crawler - Unprovided Fields will be reset

    - **crawler_uuid**: The crawlers UUID to update
    - **contact**: The e-mail address of the crawlers owner
    - **location** (optional): The location where the crawler resides
    - **pref_tld** (optional): The Top-Level-Domain, which the crawler prefers to crawl
    """
    updated_crawler = ex.update_crawler(crawler)
    return updated_crawler



@app.patch(
    "/crawler/",
    status_code=200,
    response_model=models.Crawler,
    response_model_exclude_unset=True,
    tags=["Crawler"],
    summary="Update a crawler",
    response_description="Information about the updated created crawler"
)
async def update_crawler(
    crawler: models.Crawler = Body(
        ...,
        example={
            "uuid": "12345678-90ab-cdef-0000-000000000000",
            "contact": "jens@example.com",
            "location": "USA, Texas, Houston",
            "pref_tld": "com",
        },
    )
):
    """
    Update a Crawler -  Unprovided Fields will be ignored

    - **crawler_uuid**: The crawlers UUID to update
    - **contact**: The e-mail address of the crawlers owner
    - **location** (optional): The location where the crawler resides
    - **pref_tld** (optional): The Top-Level-Domain, which the crawler prefers to crawl
    """
    updated_crawler = ex.update_crawler(crawler)
    return updated_crawler
