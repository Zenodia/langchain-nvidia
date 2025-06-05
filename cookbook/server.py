from fastmcp import FastMCP
from dotenv import load_dotenv
from colorama import Fore
import asyncio
from tavily import TavilyClient, AsyncTavilyClient
load_dotenv()
tavily_client = TavilyClient()
tavily_async_client = AsyncTavilyClient()

mcp = FastMCP("SweBenchTools")
@mcp.tool()
def tavily_single_search(query):
    """ Search the web using the Tavily API.
    
    Args:
        query (str): The search query to execute
        
    Returns:
        dict: Tavily search response containing:
            - results (list): List of search result dictionaries, each containing:
                - title (str): Title of the search result
                - url (str): URL of the search result
                - content (str): Snippet/summary of the content
                - raw_content (str): Full content of the page if available"""
     
    return tavily_client.search(query, 
                         max_results=5, 
                         include_raw_content=True)

@mcp.tool()
async def tavily_concurrent_search_async(search_queries:list=None , tavily_topic :str=None, tavily_days:int=None):
    """
    Performs concurrent web searches using the Tavily API for multiple search queries in one go.

    Args:
        search_queries (List[SearchQuery]): List of search queries to process
        tavily_topic (str): Type of search to perform ('news' or 'general')
        tavily_days (int): Number of days to look back for news articles (only used when tavily_topic='news')

    Returns:
        List[dict]: List of search results from Tavily API, one per query

    Note:
        For news searches, each result will include articles from the last `tavily_days` days.
        For general searches, the time range is unrestricted.
    """
    print(Fore.MAGENTA + f" **async & parallel ** Tavily API Call , with search_queries= {search_queries} \n tavily_topic={tavily_topic} \n tavily_days:{tavily_days}   ", Fore.RESET)
    search_tasks = []
    for query in search_queries:
        if tavily_topic == "news":
            search_tasks.append(
                tavily_async_client.search(
                    query,
                    max_results=5,
                    include_raw_content=True,
                    topic="news",
                    days=tavily_days
                )
            )
        else:
            search_tasks.append(
                tavily_async_client.search(
                    query,
                    max_results=5,
                    include_raw_content=True,
                    topic="general"
                )
            )

    # Execute all searches concurrently
    search_docs = await asyncio.gather(*search_tasks)
    print(Fore.MAGENTA + f" **async & parallel ** Tavily API Call resulting documents {search_docs} ", Fore.RESET)
    return search_docs

mcp.run(transport="streamable-http",
        host="127.0.0.1",
        port=4200,
        log_level="debug",
        )

