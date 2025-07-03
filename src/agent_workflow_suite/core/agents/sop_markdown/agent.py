from google.adk.agents import Agent
from .models import SOPMarkdown

sop_markdown = Agent(
    model="gemini-2.0-flash",
    name="sop_markdown",
    description="""Generates standardized Standard Operating Procedure (SOP) markdown documents from screen recording analysis.

This agent integrates outputs from:
- nl_transcription: Natural language workflow analysis and user behavior insights
- playwright_transcription: Technical browser actions and automation sequences

Creates ISO 13485/ISO 9001 compliant SOP documentation with:
- Document control and metadata
- Step-by-step procedures with roles and responsibilities
- Risk assessments and safety controls
- Quality metrics and verification methods
- Integration of technical automation possibilities
- Change tracking and version control

Input: Video recording + nl_transcription output + playwright_transcription output
Output: Professional SOP markdown document ready for organizational use""",
    output_schema=SOPMarkdown,
    output_key="sop_markdown",
)

root_agent = sop_markdown 