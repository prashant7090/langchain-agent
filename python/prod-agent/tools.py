from langchain.tools import tool

@tool
def get_deployment_info():
    """Get information about the latest production deployment."""
    return {
        "version": "v2.5.0",
        "deployed_at": "2026-08-28 10:30",
        "status": "success"
    }