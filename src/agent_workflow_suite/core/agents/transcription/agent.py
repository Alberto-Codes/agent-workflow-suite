from google.adk.agents import ParallelAgent
from agent_workflow_suite.core.agents.nl_transcription import root_agent as nl_transcription
from agent_workflow_suite.core.agents.playwright_transcription import root_agent as playwright_transcription

transcription_agent = ParallelAgent(
    name="transcription_agent",
    sub_agents=[nl_transcription, playwright_transcription],
    description="Executes a sequence of natural language and playwright transcription.",
)

root_agent = transcription_agent