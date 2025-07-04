from google.adk.agents import SequentialAgent
from agent_workflow_suite.core.agents.transcription import (
    root_agent as transcription_agent,
)
from agent_workflow_suite.core.agents.sop_markdown import (
    root_agent as sop_agent,
    after_agent_callback,
)
from agent_workflow_suite.core.agents.worker import root_agent as worker_agent


video_pipeline_agent = SequentialAgent(
    name="video_pipeline_agent",
    sub_agents=[transcription_agent, sop_agent, worker_agent],
    description="Executes a sequence of transcription and sop generation.",
    # after_agent_callback=after_agent_callback
)

# For ADK tools compatibility, the root agent must be named `root_agent`
root_agent = video_pipeline_agent
