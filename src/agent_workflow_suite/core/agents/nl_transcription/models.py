from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class ActionType(str, Enum):
    """High-level action types for browser workflows."""
    
    NAVIGATE = "navigate"
    FORM = "form"
    REVIEW = "review"
    SEARCH = "search"
    DECIDE = "decide"
    VALIDATE = "validate"
    ERROR = "error"
    COMPLETE = "complete"


class Confidence(str, Enum):
    """Confidence levels for transcription accuracy."""
    
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Step(BaseModel):
    """A single workflow step with natural language interpretation."""
    
    num: int = Field(..., description="Step number")
    start: float = Field(..., description="Start time in seconds")
    end: float = Field(..., description="End time in seconds")
    action: ActionType = Field(..., description="Action category")
    
    # Core natural language fields
    desc: str = Field(..., description="What the worker did")
    intent: str = Field(..., description="Why they did it")
    
    # Optional observations
    reasoning: Optional[str] = Field(None, description="Thought process")
    notes: Optional[str] = Field(None, description="Behavior observations")
    confusion: Optional[str] = Field(None, description="Signs of confusion")
    
    # Context
    page: Optional[str] = Field(None, description="Page context")
    content: Optional[str] = Field(None, description="Content reviewed")
    
    # Quality
    confidence: Confidence = Field(default=Confidence.MEDIUM)


class Summary(BaseModel):
    """High-level workflow analysis."""
    
    task: str = Field(..., description="Task description")
    objective: str = Field(..., description="Primary objective")
    duration: float = Field(..., description="Total duration in seconds")
    
    # Key insights (simplified)
    decisions: List[str] = Field(default_factory=list, description="Key decisions")
    problems: List[str] = Field(default_factory=list, description="Problem-solving instances")
    learning: List[str] = Field(default_factory=list, description="Learning/adaptation evidence")
    
    # Assessment
    efficiency: str = Field(..., description="Efficiency assessment")
    expertise: str = Field(..., description="Worker expertise level")
    completion: str = Field(..., description="Task completion status")
    
    # Outcomes
    success: List[str] = Field(default_factory=list, description="Success indicators")
    challenges: List[str] = Field(default_factory=list, description="Challenges faced")


class Metadata(BaseModel):
    """Recording metadata."""
    
    id: str = Field(..., description="Recording ID")
    duration: float = Field(..., description="Duration in seconds")
    resolution: str = Field(..., description="Screen resolution")
    
    # Browser info
    browser: Optional[str] = Field(None, description="Browser type")
    version: Optional[str] = Field(None, description="Browser version")
    
    # Context
    websites: List[str] = Field(default_factory=list, description="Main websites accessed")
    apps: List[str] = Field(default_factory=list, description="Web applications used")
    
    # Timestamps
    recorded: datetime = Field(..., description="Recording time")
    processed: datetime = Field(default_factory=datetime.now)


class Quality(BaseModel):
    """Quality assessment of the interpretation."""
    
    overall: Confidence = Field(..., description="Overall confidence")
    clarity: str = Field(..., description="Intent clarity assessment")
    
    # Metrics
    clear_steps: int = Field(..., description="Steps with clear intent")
    unclear_steps: int = Field(..., description="Steps with unclear intent")
    
    # Issues
    unclear_moments: List[str] = Field(default_factory=list, description="Unclear moments")
    missing_context: List[str] = Field(default_factory=list, description="Missing context areas")
    
    # Processing
    process_time: float = Field(..., description="Processing time in seconds")
    model_version: str = Field(..., description="Analysis model version")


class Transcription(BaseModel):
    """Complete natural language transcription of browser recording."""
    
    # Core components
    metadata: Metadata = Field(..., description="Recording metadata")
    summary: Summary = Field(..., description="Workflow analysis")
    steps: List[Step] = Field(..., description="Step-by-step interpretation")
    quality: Quality = Field(..., description="Quality assessment")
    
    # Additional analysis
    thoughts: List[str] = Field(default_factory=list, description="Worker thought processes")
    patterns: List[str] = Field(default_factory=list, description="Behavioral patterns")
    expertise_signs: List[str] = Field(default_factory=list, description="Expertise indicators")
    
    # Context
    work_context: str = Field(..., description="Work context")
    complexity: List[str] = Field(default_factory=list, description="Complexity factors")
    
    # Version
    version: str = Field(default="1.0", description="Transcription version")

    def get_step(self, step_num: int) -> Optional[Step]:
        """Get step by number."""
        for step in self.steps:
            if step.num == step_num:
                return step
        return None
    
    def get_steps_by_action(self, action: ActionType) -> List[Step]:
        """Get steps by action type."""
        return [step for step in self.steps if step.action == action]
    
    def get_decision_steps(self) -> List[Step]:
        """Get steps involving decision making."""
        decision_steps = self.get_steps_by_action(ActionType.DECIDE)
        reasoning_steps = [step for step in self.steps if step.reasoning]
        
        # Combine and deduplicate
        all_steps = list(set(decision_steps + reasoning_steps))
        return sorted(all_steps, key=lambda x: x.num)
    
    def calc_efficiency_score(self) -> float:
        """Calculate basic efficiency score (0-1)."""
        if not self.steps:
            return 0.0
            
        total = len(self.steps)
        errors = len(self.get_steps_by_action(ActionType.ERROR))
        high_conf = len([s for s in self.steps if s.confidence == Confidence.HIGH])
        
        error_penalty = errors / total if total > 0 else 0
        confidence_bonus = high_conf / total if total > 0 else 0
        
        score = 0.5 + confidence_bonus - error_penalty
        return max(0.0, min(1.0, score))