import requests
from bs4 import BeautifulSoup
from utils import log

HEADERS = {"User-Agent": "Mozilla/5.0"}

def search_duckduckgo(query, num_results=3):
    url = "https://duckduckgo.com/html/"
    params = {"q": query}
    response = requests.post(url, data=params, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    links = []
    for result in soup.select(".result__a")[:num_results]:
        links.append({
            "title": result.get_text(),
            "url": result.get("href")
        })

    return links


def fetch_page_text(url, max_chars=3000):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=5)
        soup = BeautifulSoup(resp.text, "html.parser")
        text = " ".join(p.get_text() for p in soup.find_all("p"))
        return text[:max_chars]
    except Exception:
        return ""


def retrieve(search_query, num_results=3):
    log("RETRIEVAL", f"Searching for: {search_query}")
    links = search_duckduckgo(search_query, num_results)

    results = []
    for link in links:
        content = fetch_page_text(link["url"])
        results.append({
            "source": link["url"].split("/")[2],
            "title": link["title"],
            "url": link["url"],
            "content": content
        })

    return {"results": results}
