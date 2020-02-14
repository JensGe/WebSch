from app.common import example_generator as ex

from fastapi import FastAPI

app = FastAPI()


# class DomainList(BaseModel):
#     domain: str
#     ip: Ip4 = None
#     description: str = None
#     urls: List[HttpUrl] = []
#
#
# class CrawlRequest(BaseModel):
#     id: UUID
#     request_date = datetime


@app.get("/downloadlists/")
async def get_download_lists(amount:int = 1, length: int = 10, tld: str = 'all'):
    example_urls = ex.create_url_lists(amount, length, tld)
    return example_urls
