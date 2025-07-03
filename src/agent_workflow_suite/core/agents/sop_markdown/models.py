from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class SOPCategory(str, Enum):
    """Standard SOP categories based on ISO 13485 and industry standards."""
    
    OPERATIONAL = "operational"
    ADMINISTRATIVE = "administrative"
    TECHNICAL = "technical"
    SAFETY = "safety"
    QUALITY = "quality"
    TRAINING = "training"
    MAINTENANCE = "maintenance"
    EMERGENCY = "emergency"


class StepType(str, Enum):
    """Types of steps in SOP procedures."""
    
    ACTION = "action"
    DECISION = "decision"
    VERIFICATION = "verification"
    DOCUMENTATION = "documentation"
    SAFETY_CHECK = "safety_check"
    QUALITY_CONTROL = "quality_control"
    WAIT = "wait"


class RiskLevel(str, Enum):
    """Risk levels for SOP steps and procedures."""
    
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SOPMetadata(BaseModel):
    """Metadata for SOP document following ISO standards."""
    
    # Document identification
    sop_id: str = Field(..., description="Unique SOP identifier")
    title: str = Field(..., description="SOP title")
    version: str = Field(default="1.0", description="Document version")
    revision_date: datetime = Field(default_factory=datetime.now, description="Last revision date")
    
    # Authorship and approval
    author: str = Field(..., description="SOP author/creator")
    reviewer: Optional[str] = Field(None, description="SOP reviewer")
    approver: Optional[str] = Field(None, description="SOP approver")
    
    # Classification
    category: SOPCategory = Field(..., description="SOP category")
    department: str = Field(..., description="Responsible department")
    process_owner: str = Field(..., description="Process owner")
    
    # Scope and application
    purpose: str = Field(..., description="Purpose of the SOP")
    scope: str = Field(..., description="Scope of application")
    audience: List[str] = Field(default_factory=list, description="Target audience roles")
    
    # Compliance and references
    regulatory_refs: List[str] = Field(default_factory=list, description="Regulatory references")
    related_docs: List[str] = Field(default_factory=list, description="Related documents")
    
    # Processing metadata
    created_from_video: str = Field(..., description="Source video identifier")
    nl_agent_output: str = Field(..., description="Reference to nl_transcription output")
    playwright_output: str = Field(..., description="Reference to playwright_transcription output")


class SOPStep(BaseModel):
    """Individual step in SOP procedure."""
    
    step_num: str = Field(..., description="Step number (e.g., 1, 1.1, 1.2)")
    step_type: StepType = Field(..., description="Type of step")
    
    # Step content
    title: str = Field(..., description="Step title/summary")
    description: str = Field(..., description="Detailed step description")
    
    # Role and responsibility
    responsible_role: str = Field(..., description="Role responsible for this step")
    collaborating_roles: List[str] = Field(default_factory=list, description="Supporting roles")
    
    # Technical details
    tools_required: List[str] = Field(default_factory=list, description="Required tools/equipment")
    inputs: List[str] = Field(default_factory=list, description="Required inputs")
    outputs: List[str] = Field(default_factory=list, description="Expected outputs")
    
    # Quality and safety
    safety_warnings: List[str] = Field(default_factory=list, description="Safety warnings")
    quality_checks: List[str] = Field(default_factory=list, description="Quality control points")
    risk_level: RiskLevel = Field(default=RiskLevel.LOW, description="Risk level of step")
    
    # Technical automation (from playwright agent)
    automated_actions: List[str] = Field(default_factory=list, description="Automated actions possible")
    mcp_commands: List[str] = Field(default_factory=list, description="Playwright MCP commands")
    
    # Verification and documentation
    verification_method: Optional[str] = Field(None, description="How to verify completion")
    documentation_required: List[str] = Field(default_factory=list, description="Required documentation")
    
    # Timing and dependencies
    estimated_duration: Optional[str] = Field(None, description="Estimated time to complete")
    dependencies: List[str] = Field(default_factory=list, description="Dependencies on other steps")
    
    # Additional context from NL analysis
    user_insights: List[str] = Field(default_factory=list, description="User behavior insights")
    common_mistakes: List[str] = Field(default_factory=list, description="Common mistakes to avoid")


class SOPSection(BaseModel):
    """Major section of SOP (e.g., Procedure, Preparation, etc.)."""
    
    section_num: str = Field(..., description="Section number")
    title: str = Field(..., description="Section title")
    description: Optional[str] = Field(None, description="Section overview")
    steps: List[SOPStep] = Field(default_factory=list, description="Steps in this section")
    
    # Section-level metadata
    estimated_duration: Optional[str] = Field(None, description="Total section duration")
    prerequisites: List[str] = Field(default_factory=list, description="Section prerequisites")
    deliverables: List[str] = Field(default_factory=list, description="Section deliverables")


class ProcessFlowElement(BaseModel):
    """Element in process flow diagram."""
    
    element_id: str = Field(..., description="Unique element identifier")
    element_type: str = Field(..., description="Element type (start, process, decision, end)")
    label: str = Field(..., description="Element label")
    connected_to: List[str] = Field(default_factory=list, description="Connected element IDs")
    
    # Visual positioning (for diagram generation)
    position_x: Optional[int] = Field(None, description="X coordinate for positioning")
    position_y: Optional[int] = Field(None, description="Y coordinate for positioning")


class QualityMetrics(BaseModel):
    """Quality and performance metrics for the SOP."""
    
    # Completion metrics
    success_criteria: List[str] = Field(default_factory=list, description="Success criteria")
    performance_indicators: List[str] = Field(default_factory=list, description="Key performance indicators")
    
    # Quality measures
    accuracy_requirements: Optional[str] = Field(None, description="Accuracy requirements")
    error_rates: Optional[str] = Field(None, description="Acceptable error rates")
    
    # Training and competency
    training_requirements: List[str] = Field(default_factory=list, description="Required training")
    competency_assessment: Optional[str] = Field(None, description="Competency assessment method")
    
    # Review and improvement
    review_frequency: str = Field(default="annually", description="Review frequency")
    improvement_suggestions: List[str] = Field(default_factory=list, description="Improvement suggestions")


class RiskAssessment(BaseModel):
    """Risk assessment for the SOP."""
    
    risk_category: RiskLevel = Field(..., description="Overall risk category")
    identified_risks: List[str] = Field(default_factory=list, description="Identified risks")
    mitigation_measures: List[str] = Field(default_factory=list, description="Risk mitigation measures")
    
    # Risk-specific controls
    safety_controls: List[str] = Field(default_factory=list, description="Safety control measures")
    quality_controls: List[str] = Field(default_factory=list, description="Quality control measures")
    environmental_controls: List[str] = Field(default_factory=list, description="Environmental controls")
    
    # Emergency procedures
    emergency_contacts: List[str] = Field(default_factory=list, description="Emergency contact information")
    escalation_procedures: List[str] = Field(default_factory=list, description="Escalation procedures")


class ChangeHistory(BaseModel):
    """Change history entry for version control."""
    
    version: str = Field(..., description="Version number")
    date: datetime = Field(..., description="Change date")
    author: str = Field(..., description="Change author")
    description: str = Field(..., description="Description of changes")
    approval_status: str = Field(default="pending", description="Approval status")
    approver: Optional[str] = Field(None, description="Approver name")


class SOPMarkdown(BaseModel):
    """Complete SOP markdown document following international standards."""
    
    # Core document structure
    metadata: SOPMetadata = Field(..., description="SOP metadata and document control")
    sections: List[SOPSection] = Field(..., description="Main SOP sections")
    
    # Supporting documentation
    process_flow: List[ProcessFlowElement] = Field(default_factory=list, description="Process flow diagram elements")
    quality_metrics: QualityMetrics = Field(..., description="Quality and performance metrics")
    risk_assessment: RiskAssessment = Field(..., description="Risk assessment")
    
    # References and appendices
    definitions: Dict[str, str] = Field(default_factory=dict, description="Definitions and terminology")
    abbreviations: Dict[str, str] = Field(default_factory=dict, description="Abbreviations")
    references: List[str] = Field(default_factory=list, description="External references")
    appendices: List[str] = Field(default_factory=list, description="Supporting appendices")
    
    # Version control
    change_history: List[ChangeHistory] = Field(default_factory=list, description="Document change history")
    
    # Integration metadata
    source_analysis: Dict[str, str] = Field(default_factory=dict, description="Source analysis metadata")
    generation_notes: List[str] = Field(default_factory=list, description="Generation notes and limitations")
    
    # Document format version
    format_version: str = Field(default="1.0", description="SOP format version")

    def get_section(self, section_num: str) -> Optional[SOPSection]:
        """Get section by number."""
        for section in self.sections:
            if section.section_num == section_num:
                return section
        return None
    
    def get_all_steps(self) -> List[SOPStep]:
        """Get all steps across all sections."""
        all_steps = []
        for section in self.sections:
            all_steps.extend(section.steps)
        return all_steps
    
    def get_steps_by_role(self, role: str) -> List[SOPStep]:
        """Get all steps assigned to a specific role."""
        all_steps = self.get_all_steps()
        return [step for step in all_steps if step.responsible_role == role]
    
    def get_critical_steps(self) -> List[SOPStep]:
        """Get all critical risk level steps."""
        all_steps = self.get_all_steps()
        return [step for step in all_steps if step.risk_level == RiskLevel.CRITICAL]
    
    def calculate_total_duration(self) -> str:
        """Calculate estimated total duration."""
        # Simple implementation - could be enhanced
        total_minutes = 0
        for section in self.sections:
            if section.estimated_duration:
                # Parse duration string (assumes "X minutes" format)
                try:
                    duration_parts = section.estimated_duration.split()
                    if len(duration_parts) >= 2 and duration_parts[1].lower() in ['minutes', 'mins', 'min']:
                        total_minutes += int(duration_parts[0])
                except:
                    pass
        
        if total_minutes > 0:
            hours = total_minutes // 60
            minutes = total_minutes % 60
            if hours > 0:
                return f"{hours} hours {minutes} minutes"
            else:
                return f"{minutes} minutes"
        return "Duration not calculated"
    
    def generate_markdown_content(self) -> str:
        """Generate the complete markdown content for the SOP."""
        lines = []
        
        # Document header
        lines.append(f"# {self.metadata.title}")
        lines.append("")
        lines.append(f"**Document ID:** {self.metadata.sop_id}")
        lines.append(f"**Version:** {self.metadata.version}")
        lines.append(f"**Date:** {self.metadata.revision_date.strftime('%Y-%m-%d')}")
        lines.append(f"**Author:** {self.metadata.author}")
        lines.append("")
        
        # Table of contents would go here
        lines.append("## Table of Contents")
        lines.append("")
        for i, section in enumerate(self.sections, 1):
            lines.append(f"{i}. {section.title}")
        lines.append("")
        
        # Purpose and scope
        lines.append("## 1. Purpose")
        lines.append(self.metadata.purpose)
        lines.append("")
        lines.append("## 2. Scope")
        lines.append(self.metadata.scope)
        lines.append("")
        
        # Main sections
        for i, section in enumerate(self.sections, 3):
            lines.append(f"## {i}. {section.title}")
            if section.description:
                lines.append(section.description)
                lines.append("")
            
            for step in section.steps:
                lines.append(f"### {step.step_num}. {step.title}")
                lines.append(f"**Responsible Role:** {step.responsible_role}")
                lines.append("")
                lines.append(step.description)
                lines.append("")
                
                if step.safety_warnings:
                    lines.append("**⚠️ Safety Warnings:**")
                    for warning in step.safety_warnings:
                        lines.append(f"- {warning}")
                    lines.append("")
        
        return "\n".join(lines) 