from duckduckgo_search import DDGS


def web_search(query, max_results=5):
    """
    Search the web and return search results.
    """

    results = []

    try:
        with DDGS() as ddgs:
            search_results = ddgs.text(
                query,
                max_results=max_results
            )

            for result in search_results:
                results.append({
                    "title": result.get("title", ""),
                    "url": result.get("href", ""),
                    "description": result.get("body", "")
                })

    except Exception as error:
        print(f"NOVA WEB ERROR: {error}")

    return results


def display_results(results):

    if not results:
        print("NOVA: No search results found.")
        return

    print()
    print("========================================")
    print("          NOVA WEB RESULTS")
    print("========================================")

    for number, result in enumerate(results, start=1):

        print(f"\n[{number}] {result['title']}")
        print(f"URL: {result['url']}")
        print(f"{result['description']}")

    print("\n========================================")