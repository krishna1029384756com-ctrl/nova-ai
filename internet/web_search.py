"""Simple web search helper for NOVA."""
import requests


def web_search(query, max_results=5):
    url = "https://html.duckduckgo.com/html/"
    try:
        response = requests.get(url, params={"q": query}, timeout=10, headers={"User-Agent": "NOVA-AI/1.0"})
        response.raise_for_status()
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        results = []
        for item in soup.select(".result")[:max_results]:
            link = item.select_one(".result__a")
            snippet = item.select_one(".result__snippet")
            if link:
                results.append({"title": link.get_text(" ", strip=True), "url": link.get("href"), "snippet": snippet.get_text(" ", strip=True) if snippet else ""})
        return results
    except Exception:
        return []


def display_results(results):
    for index, result in enumerate(results, 1):
        print(f"{index}. {result['title']}\n   {result['url']}\n   {result['snippet']}")
