from mcp.server.fastmcp import FastMCP
import urllib.request
import json

mcp = FastMCP("search_server")

@mcp.tool()
def search_web(query: str) -> str:
    """Search the web for information about a topic."""
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(query)}"
        import urllib.parse
        req = urllib.request.Request(url, headers={"User-Agent": "AutoPPT-Agent/1.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read())
            return data.get("extract", "No information found.")[:500]
    except Exception as e:
        return f"Search unavailable. Use your own knowledge about: {query}"

if __name__ == "__main__":
    mcp.run()