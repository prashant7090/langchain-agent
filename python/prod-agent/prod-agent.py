import asyncio
from pathlib import Path

from deepagents import create_deep_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

from models import model
from tools import get_api_metrics, get_application_logs, rollback_deployment

from langgraph.checkpoint.memory import InMemorySaver


async def main():

    server_script = str(Path(__file__).resolve().with_name("mcp_server.py"))

    client = MultiServerMCPClient({
        "production": {
            "transport": "stdio",
            "command": "python",
            "args": [server_script],
            "cwd": str(Path(__file__).resolve().parent),
        }
    })

    mcp_tools = await client.get_tools()

    checkpointer = InMemorySaver()

    agent = create_deep_agent(
        model=model,
        tools=[
            get_api_metrics,
            get_application_logs,
            *mcp_tools,
            rollback_deployment
        ],
        system_prompt="You are a production issue investigation assistant. If the evidence indicates a rollback is needed, call rollback_deployment with the appropriate version",
        checkpointer=checkpointer,
    )

    config = {
        "configurable": {
            "thread_id": "production-issue-001"
        }
    }

    result = await agent.ainvoke(
        {
            "messages": [{
                "role": "user",
                "content": "Investigate the production API issue."
            }]
        },
        config=config,
    )

    print("\n=== FINAL RESPONSE ===")
    for message in result["messages"]:
        if hasattr(message, "content") and message.content:
            print(f"\n--- {type(message).__name__} ---")
            print(message.content)

    for message in result["messages"]:
        if getattr(message, "name", None) == "rollback_deployment":
            print("\n=== ROLLBACK LOG ===")
            print(message.content)


if __name__ == "__main__":
    asyncio.run(main())