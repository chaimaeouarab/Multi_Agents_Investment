from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_market_news(query: str) -> str:
    """Search for market news and trends"""
    try:
        response = tavily.search(query=query, search_depth="basic", max_results=5)
        results = []
        for result in response['results']:
            results.append(f"- {result['title']}\n  {result['content'][:200]}...\n  Source: {result['url']}\n")
        return "\n".join(results) if results else "No relevant news found."
    except Exception as e:
        return f"Search error: {str(e)}"