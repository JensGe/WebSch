# internal packages
from app.common import example_generator as ex
from app.common import models

# external packages
from fastapi import FastAPI, Body
from starlette.status import HTTP_201_CREATED

app = FastAPI()


@app.post("/frontiers/", response_model=models.Frontier)
async def get_frontier(
    request: models.CrawlRequest = Body(
        ...,
        example={
            "crawler": "123e4567-e89b-12d3-a456-426655440000",
            "amount": 5,
            "length": 3,
            "tld": None,
        },
    )
):
    example_urls = ex.generate_frontier(
        request.crawler.location, request.amount, request.length
    )
    return example_urls


@app.post(
    "/crawler/",
    status_code=HTTP_201_CREATED,
    response_model=models.Crawler,
    response_model_exclude_unset=True,
)
async def register_crawler(
    crawler: models.Crawler = Body(
        ...,
        example={
            "contact": "jens@example.com",
            "location": "Germany - Hannover",
            "pref_tld": "de"
        },
    )
):
    new_crawler = ex.create_new_crawler(crawler)
    return new_crawler
