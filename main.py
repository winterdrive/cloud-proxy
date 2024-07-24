import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import cloudscraper
from fake_useragent import UserAgent

app = FastAPI()


def fetch(url: str) -> str:
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
    response.raise_for_status()  # This will raise an exception for HTTP errors
    return response.text


class URLItem(BaseModel):
    url: str


@app.post("/fetch-url")
async def fetch_url(item: URLItem):
    try:
        content = fetch(item.url)
        return {"content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/ip")
async def get_ip():
    # https://www.whatismyip.com/
    ip = requests.get('https://api.ipify.org').text
    return {"message": ip}


if __name__ == '__main__':
    print(fetch("https://www.mirrormedia.mg/story/20240703yweb001"))
