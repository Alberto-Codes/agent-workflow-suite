from google.adk.agents import Agent
from .prompts import AGENT_DESCRIPTION, AGENT_INSTRUCTION
from google.adk.tools.mcp_tool.mcp_toolset import (
    MCPToolset,
    StdioServerParameters,
    StdioConnectionParams,
)

# Configure Playwright MCP server
server_params = StdioServerParameters(
    command="npx",
    args=[
        "-y",
        "@playwright/mcp@latest",
        "--image-responses=allow",
        "--vision",
        "--output-dir=.data/mcp/playwright/output",
        "--user-data-dir=./data/mcp/playwright/user",
        "--browser=chrome"
    ],
)
connection_params = StdioConnectionParams(server_params=server_params, timeout=60)
toolset = MCPToolset(connection_params=connection_params)


execution_agent = Agent(
    model="gemini-2.5-pro",
    name="execution_agent",
    description=AGENT_DESCRIPTION,
    instruction=AGENT_INSTRUCTION,
    tools=[toolset],
)

# For ADK tools compatibility, the root agent must be named `root_agent`
root_agent = execution_agent
