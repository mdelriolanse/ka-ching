from mcp.server.fastmcp import FastMCP
from config import DEFAULT_PORT
import argparse
from services.search_service import search_news

def create_mcp_server(port=DEFAULT_PORT):

    mcp = FastMCP("YoutubeSearch", port=port)
    
    register_tools(mcp)

    return mcp

def register_tools(mcp):

    @mcp.tool()
    async def search_videos_tool(query: str) -> list[dict]:
        
        """
        Search for Youtube videos using SerpAPI.
        """
        
        return await search_news(query)


    
    @mcp.tool()
    def server_status():

        return {"status": "running"}


def main():
    parser = argparse.ArgumentParser(description="Model Context Protocol Youtube Search Service")

    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    args = parser.parse_args()

    mcp = create_mcp_server(port = args.port)

    server_type = "sse" if args.connection_type == "http" else "stdio"

    mcp.run(server_type=server_type)

if __name__ == "__main__":
    main()