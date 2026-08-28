from langchain.tools import tool


@tool
def get_api_metrics():
    """Get checkout API performance metrics."""
    return {
        "current_latency_ms": 1850,
        "normal_latency_ms": 250,
        "error_rate": "2.8%"
    }


@tool
def get_application_logs():
    """Get recent checkout API application logs."""
    return [
        "DB query timeout: 1200ms",
        "Connection pool exhausted",
        "Slow query detected: SELECT orders..."
    ]    

@tool
def rollback_deployment(version: str) -> str:
    """Rollback production to a specified version."""
    return f"Rollback to {version} completed successfully."