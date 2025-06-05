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
        """
        Tool: 
        name='bash' 
        description='\n    Run commands in a bash shell\n    * When invoking this tool, the contents of the "command" parameter does NOT need to be XML-escaped.\n    * You don\'t have access to the internet via this tool.\n    * You do have access to a mirror of common linux and python packages via apt and pip.\n    * State is persistent across command calls and discussions with the user.\n    * To inspect a particular line range of a file, e.g. lines 10-25, try \'sed -n 10,25p /path/to/the/file\'.\n    * Please avoid commands that may produce a very large amount of output.\n    * Please run long lived commands in the background, e.g. \'sleep 10 &\' or start a server in the background.\n\n    
        Args:\n        command (str): The bash command to run.\n\n    
        Returns:\n        str: The output of the bash command\n    
        inputSchema={'properties': {'command': {'title': 'Command', 'type': 'string'}},'required': ['command'], 'type': 'object'} 
        """

        #result = await client.call_tool("tavily_single_search", {"query": "Who is Leo Messi?"})
        #print(f"bash result: {result}")
        result = await client.call_tool("tavily_concurrent_search_async", {"search_queries": ["Who is Leonardo Da Vinci?","what is the difference between CPU and GPU?"], "tavily_topic":"general","tavily_days":1})
        print(f"bash result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
