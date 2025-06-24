import asyncio
import json
import os

import openai
from dotenv import load_dotenv
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport
from mcp.types import Tool


async def main():
    mcp_client = Client(transport=StreamableHttpTransport("http://127.0.0.1:4200/mcp"))
    llm_client = openai.AzureOpenAI(api_key=os.getenv("OPENAI_API_KEY", "EMPTY"),
                                    api_version="2024-02-15-preview",
                                    azure_endpoint="https://llm-proxy.perflab.nvidia.com")
    async with mcp_client:
        messages = []
        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                print("Exiting...")
                break
            messages.append({"role": "user", "content": user_input})
            response = llm_client.chat.completions.create(
                model="claude-3-7-sonnet-20250219",
                messages=messages,
                max_tokens=64_000,
                tools=await get_tool_dict(mcp_client),
                tool_choice="auto",
            )

            response_message = response.choices[0].message
            if response_message:
                print(response_message.content)
                messages.append(response_message)
            if response_message.tool_calls:
                for tool_call in response_message.tool_calls:
                    tool_output = await mcp_client.call_tool(tool_call.function.name,
                                                             json.loads(tool_call.function.arguments))
                    message = {"role": "tool",
                               "tool_call_id": tool_call.id,
                               "name": tool_call.function.name,
                               "content": tool_output[0].text}
                    print(message)
                    messages.append(message)


async def get_tool_dict(mcp_client):
    mcp_tools: list[Tool] = await mcp_client.list_tools()
    return [{"type": "function",
             "function": {"name": mcp_tool.name,
                          "description": mcp_tool.description,
                          "parameters": mcp_tool.inputSchema,
                          }
             }
            for mcp_tool in mcp_tools
            ] if mcp_tools else None


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
