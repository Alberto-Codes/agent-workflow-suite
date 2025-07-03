from google.adk.agents import Agent
from .models import Transcription

nl_transcription = Agent(
    model="gemini-2.0-flash",
    name="nl_transcription",
    description="Transcribes natural language to text.",
    output_schema=Transcription,
    output_key="nl_transcription",

)

root_agent = nl_transcription