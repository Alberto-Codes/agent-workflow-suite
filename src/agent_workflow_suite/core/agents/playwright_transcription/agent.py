from google.adk.agents import Agent
from .models import PlaywrightTranscription

playwright_transcription = Agent(
    model="gemini-2.0-flash",
    name="playwright_transcription",
    description="Transcribes screen recordings to detect Playwright browser actions and generate MCP-compatible command sequences.",
    output_schema=PlaywrightTranscription,
    output_key="playwright_transcription",
)

root_agent = playwright_transcription