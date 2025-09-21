from typing import List, Dict, Optional, Any
from mcp_flight_search.services.serpapi_client import run_search, prepare_news_search_params

async def search_news(query) -> List[Dict[str, str]]:
    """
    Search for news articles using SerpAPI News.
    
    Args:
        query: The search query string.
        
    Returns:
        A list of news articles with details.
    """

    params = prepare_news_search_params(query)
    search_results = await run_search(params)

    # Check for errors
    if "error" in search_results:
        return {"error": search_results["error"]}

    return format_news_results(search_results)
    
    

def format_news_results(search_results: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Format raw flight search results into a standardized format.
    
    Args:
        search_results: Raw search results from SerpAPI
        
    Returns:
        Formatted list of news article information
    """
    articles = search_results.get("articles", [])

    # Format news article data
    formatted_articles = []
    for i, article in enumerate(articles):
        if not article.get("title"):
            continue
        
        formatted_articles.append({
            "title": article.get("title", "No Title"),
            "link": article.get("link", "")
        })
        
    return formatted_articles 