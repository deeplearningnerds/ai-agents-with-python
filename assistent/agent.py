import asyncio
from agents import Agent, Runner, HostedMCPTool
from dotenv import load_dotenv

load_dotenv()

# System prompt
prompt = "You are a helpful assistant that can greet users."

# Tool definitions
mcp = HostedMCPTool(tool_config={
    "type": "mcp",
    "server_label": "dlnerds",
    "server_url": "https://mcp-dlnerds.fastmcp.app/mcp",
    "allowed_tools": [
        "greet_user"
    ],
    "require_approval": "never"
})

# agent
agent = Agent(
    name="Assistant",
    instructions=prompt,
    model="gpt-5",
    tools=[
        mcp
    ],
)

async def run_agent(agent_input: str):
    result = await Runner.run(
        starting_agent=agent,
        input=agent_input
    )
    return result.final_output


def query_agent(query: str):
    return asyncio.run(run_agent(query))


if __name__ == "__main__":
    agent_response = query_agent("Greet Alice")
    print(agent_response)
