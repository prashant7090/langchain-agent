import asyncio
from deepagents import create_deep_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

from models import model
from tools import get_api_metrics, get_application_logs, rollback_deployment

from langgraph.checkpoint.memory import InMemorySaver



async def main():

    client = MultiServerMCPClient({
        "production": {
            "transport": "stdio",
            "command": "python",
            "args": ["mcp_server.py"],
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
        system_prompt="You are a production issue investigation assistant.",
        checkpointer=checkpointer,
        interrupt_on={
            "rollback_deployment": {
                "allowed_decisions": ["approve", "reject"]
            }
        }
    )

    result = await agent.ainvoke(
       {
            "messages": [{
                "role": "user",
            "content": "Investigate the production API issue."
            }]
        },
        config={
            "configurable": {
                "thread_id": "production-issue-001"
            }
        }
    )

    print(result["messages"][-1].content)
    for message in result["messages"]:
        print("\n---", type(message).__name__, "---")
        print(message.content)


if __name__ == "__main__":
    asyncio.run(main())