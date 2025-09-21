from google import genai
from google.genai import types
from config import settings
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from pydantic import BaseModel

from fastapi import FastAPI

class NewsSuggestion(BaseModel):
    video_name: str
    video_link: str

server_params = StdioServerParameters(
    command="python3 -m mcp_server.launch",
    args=["--port", str(settings.port)],
)

app = FastAPI()

client = genai.Client(api_key=settings.gemini_api_key)

async def run():
    async with stdio_client(server_params) as (read,write):
        async with ClientSession(read, write) as session:
            prompt = f"Find Flights from Atlanta to Las Vegas"
            await session.initialize()

            mcp_tools = await session.list_tools()

            tools = [
                types.Tool(
                    function_declarations=[
                                                {
                            "name": tool.name,
                            "description": tool.description,
                            "parameters": {
                                k: v
                                for k, v in tool.inputSchema.items()
                                if k not in ["additionalProperties", "$schema"]
                            },
                        }
                    ]
                )

                for tool in mcp_tools.tools
            ]

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents="Recommend three news articles about technology. Respond with their links and titles only.",
        config=types.GenerateContentConfig(
            temperature=0,
            response_mime_type="application/json",
            response_schema=list[NewsSuggestion],
            thinking_config=types.ThinkingConfig(thinking_budget=0),
            tools=tools
        )
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(run())