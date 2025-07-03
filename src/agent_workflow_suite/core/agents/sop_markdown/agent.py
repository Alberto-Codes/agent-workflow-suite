import json
from datetime import datetime
import google.genai.types as types
from google.adk.agents import Agent
from .models import SOPMarkdown
from google.adk.agents.callback_context import CallbackContext


async def after_agent_callback(callback_context: CallbackContext):
    """Save generated SOP markdown after agent completes execution."""
    try:
        print(f"🔍 After agent callback triggered, checking state for output_key...")
        
        # Access the structured output via the output_key after agent completion
        sop_data = callback_context.state.get("sop_markdown")
        print(f"🔍 SOP data found in state: {sop_data is not None}")
        
        if sop_data:
            try:
                # Convert dict back to SOPMarkdown model (ADK stores it as dict/JSON)
                sop_obj = SOPMarkdown(**sop_data)
                print(f"🔍 Successfully converted dict to SOPMarkdown object")
                
                # Generate the actual markdown content from the structured data
                markdown_content = sop_obj.generate_markdown_content()
                
                # Generate filename with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                # Create artifacts using types.Part objects
                markdown_part = types.Part.from_bytes(
                    data=markdown_content.encode('utf-8'),
                    mime_type="text/markdown"
                )
                
                json_part = types.Part.from_bytes(
                    data=sop_obj.model_dump_json(indent=2).encode('utf-8'),
                    mime_type="application/json"
                )
                
                summary_data = {
                    "timestamp": timestamp,
                    "sop_title": sop_obj.metadata.title,
                    "step_count": len(sop_obj.sections[0].steps) if sop_obj.sections else 0,
                    "document_version": sop_obj.metadata.version,
                    "regulatory_refs": sop_obj.metadata.regulatory_refs
                }
                
                summary_part = types.Part.from_bytes(
                    data=json.dumps(summary_data, indent=2).encode('utf-8'),
                    mime_type="application/json"
                )
                
                # Save all artifacts
                version = await callback_context.save_artifact(f"sop_{timestamp}.md", markdown_part)
                version = await callback_context.save_artifact(f"sop_structured_{timestamp}.json", json_part)
                version = await callback_context.save_artifact(f"sop_summary_{timestamp}.json", summary_part)
                
                await callback_context.load_artifact(f"sop_{timestamp}.md", 0)
                await callback_context.load_artifact(f"sop_structured_{timestamp}.json", 0)
                await callback_context.load_artifact(f"sop_summary_{timestamp}.json", 0)

                print(f"✅ SOP artifacts saved successfully with timestamp {timestamp}")
                
            except Exception as conversion_error:
                print(f"❌ Error converting dict to SOPMarkdown: {conversion_error}")
                print(f"🔍 Raw data type: {type(sop_data)}")
                print(f"🔍 Raw data sample: {str(sop_data)[:500]}...")
                
        else:
            print(f"❌ No SOPMarkdown data found in state")
            print(f"🔍 State contents: {callback_context.state}")
            
    except Exception as e:
        print(f"❌ Error in after_agent_callback: {e}")
        import traceback
        traceback.print_exc()


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
    after_agent_callback=after_agent_callback
)

root_agent = sop_markdown 