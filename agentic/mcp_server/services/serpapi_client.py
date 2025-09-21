import asyncio
import json
from config.settings import serp_api_key
from typing import Dict, Any
from serpapi import GoogleSearch
from mcp_flight_search.utils.logging import logger
from mcp_flight_search.config import SERP_API_KEY

async def run_search(params: Dict[str, Any]):
    """
    Run SerpAPI search asynchronously.
    
    Args:
        params: Parameters for the SerpAPI search
        
    Returns:
        Search results from SerpAPI
    """
    try:
        result = await asyncio.to_thread(lambda: GoogleSearch(params).get_dict())
        return result["news_results"] if "news_results" in result else result
    except Exception as e:
        return {"error": str(e)}

def prepare_news_search_params(query: str) -> Dict[str, Any]:

    params = {
        "q": query,
        "tmb": "nws",
        "api_key": SERP_API_KEY
    }

    return params