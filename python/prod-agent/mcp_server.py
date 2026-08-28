from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Production Server")

@mcp.tool()
def get_deployment_info() -> dict:
    """Get latest production deployment information."""
    return {
        "version": "v2.5.0",
        "status": "success",
        "deployed_at": "2026-08-28 10:30"
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")