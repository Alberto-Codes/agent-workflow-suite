from google.adk.agents import SequentialAgent
from agent_workflow_suite.core.agents.transcription import root_agent as transcription_agent
from agent_workflow_suite.core.agents.sop_markdown import root_agent as sop_agent

video_pipeline_agent = SequentialAgent(
    name="video_pipeline_agent",
    sub_agents=[transcription_agent, sop_agent],
    description="Executes a sequence of transcription and sop generation.",
)

# For ADK tools compatibility, the root agent must be named `root_agent`
root_agent = video_pipeline_agent