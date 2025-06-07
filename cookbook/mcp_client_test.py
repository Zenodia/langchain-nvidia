import asyncio

from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport
from fastmcp.tools import Tool


async def main():
    client = Client(transport=StreamableHttpTransport("http://127.0.0.1:4200/mcp"))
    async with client:
        tools: list[Tool] = await client.list_tools()
        for tool in tools:
            print(f"Tool: {tool}")

        #result = await client.call_tool("tavily_single_search", {"query": "Who is Leo Messi?"})
        #print(f"bash result: {result}")
        #result = await client.call_tool("tavily_concurrent_search_async", {"search_queries": ["Who is Leonardo Da Vinci?","what is the difference between CPU and GPU?"], "tavily_topic":"general","tavily_days":1})
        #print(type(result))
        #print(f" ---- \n result: \n\n {result} ----")
        


if __name__ == "__main__":
    asyncio.run(main())
