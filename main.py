from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import cloudscraper
from fake_useragent import UserAgent

app = FastAPI()


class URLRequest(BaseModel):
    url: str


def fetch(url):
    cloudscraper_mobile = cloudscraper.create_scraper(
        delay=10,
        browser={
            "browser": "chrome",
            "mobile": False,
            "platform": "ios",
            "custom": UserAgent().random,
        },
    )

    response = cloudscraper_mobile.get(url, timeout=15)

    return response.content.decode('utf-8')


@app.post("/fetch-url")
async def fetch_url(request: URLRequest):
    try:
        content = fetch(request.url)
        return {"content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
