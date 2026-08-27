from deepagents import create_deep_agent
from models import model

agent = create_deep_agent(
    model=model,
    system_prompt="You are a production issue investigation assistant."
)

result = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "Why might a production API become slow after deployment?"
        }
    ]
})

print(result["messages"][-1].content)