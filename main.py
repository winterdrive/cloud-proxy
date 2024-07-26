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


def fetch_content(url: str) -> str:
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
    return response.content


def fetch_content_utf8(url: str) -> str:
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
    return response.content.decode('utf-8')


def fetch_content_by_playwright(url: str) -> str:
    from playwright.sync_api import sync_playwright
    try:
        with sync_playwright() as playwright:
            iphone_13 = playwright.devices['iPhone 13']
            browser = playwright.webkit.launch(headless=True)
            context = browser.new_context(
                locale='zh-TW',
                timezone_id='Asia/Taipei',
                java_script_enabled=True,
                **iphone_13
            )

            # Create a new browser page
            page = context.new_page()
            page.goto(url, timeout=60000)
            response = page.content()

            # Close the browser
            browser.close()
            return response

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class URLItem(BaseModel):
    url: str


@app.post("/fetch-url")
async def fetch_url(item: URLItem):
    try:
        content = fetch(item.url)
        return content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/fetch-url-content-utf8")
async def fetch_url_content_utf8(item: URLItem):
    try:
        content = fetch_content_utf8(item.url)
        return content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/fetch-url-content")
async def fetch_url_content(item: URLItem):
    try:
        content = fetch_content(item.url)
        return content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/fetch-url-playwright")
async def fetch_url_playwright(item: URLItem):
    try:
        content = fetch_content_by_playwright(item.url)
        return content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/ip")
async def get_ip():
    # https://www.whatismyip.com/
    ip = requests.get('https://api.ipify.org').text
    return {"message": ip}


if __name__ == '__main__':
    print(fetch("https://www.mirrormedia.mg/story/20240703yweb001"))
