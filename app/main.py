from .common import example_generator as ex

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


@app.get("/downloadlist/")
async def get_download_list(length: int = 10, tld: str = 'all'):
    example_urls = ex.generate_tld_url_list(length, tld)
    return example_urls
