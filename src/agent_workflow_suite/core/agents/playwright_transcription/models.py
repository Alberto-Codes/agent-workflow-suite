from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field


class PlaywrightAction(str, Enum):
    """Playwright MCP actions that can be detected from video."""
    
    # Core browser actions
    CLICK = "browser_click"
    TYPE = "browser_type"
    SELECT = "browser_select"
    CHECK = "browser_check"
    SCROLL = "browser_scroll"
    PRESS_KEY = "browser_press_key"
    
    # Navigation actions  
    NAVIGATE = "browser_navigate"
    NAVIGATE_BACK = "browser_navigate_back"
    NAVIGATE_FORWARD = "browser_navigate_forward"
    
    # File and dialog actions
    FILE_UPLOAD = "browser_file_upload"
    HANDLE_DIALOG = "browser_handle_dialog"
    
    # Wait actions
    WAIT_FOR = "browser_wait_for"
    
    # Tab management
    TAB_NEW = "browser_tab_new"
    TAB_SELECT = "browser_tab_select"
    TAB_CLOSE = "browser_tab_close"
    
    # Resource actions
    TAKE_SCREENSHOT = "browser_take_screenshot"
    
    # Vision mode actions
    SCREEN_CLICK = "browser_screen_click"
    SCREEN_TYPE = "browser_screen_type"
    SCREEN_DRAG = "browser_screen_drag"
    SCREEN_MOVE_MOUSE = "browser_screen_move_mouse"


class DetectionConfidence(str, Enum):
    """Confidence levels for action detection."""
    
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ElementSelector(BaseModel):
    """Detected element selector information."""
    
    type: str = Field(..., description="Selector type (xpath, css, text, etc.)")
    value: str = Field(..., description="Selector value")
    confidence: DetectionConfidence = Field(default=DetectionConfidence.MEDIUM)


class ActionStep(BaseModel):
    """A detected playwright action step."""
    
    num: int = Field(..., description="Step number")
    start: float = Field(..., description="Start timestamp in seconds")
    end: float = Field(..., description="End timestamp in seconds")
    action: PlaywrightAction = Field(..., description="Detected playwright action")
    
    # Technical details
    selector: Optional[ElementSelector] = Field(None, description="Element selector")
    coordinates: Optional[Dict[str, int]] = Field(None, description="Click/drag coordinates")
    text_input: Optional[str] = Field(None, description="Text typed or entered")
    key_pressed: Optional[str] = Field(None, description="Key pressed")
    url: Optional[str] = Field(None, description="URL navigated to")
    
    # Element context
    element_desc: Optional[str] = Field(None, description="Human-readable element description")
    page_context: Optional[str] = Field(None, description="Page where action occurred")
    
    # Action parameters (for MCP compatibility)
    mcp_params: Dict[str, Union[str, int, bool, List[str]]] = Field(
        default_factory=dict, 
        description="Parameters for MCP action"
    )
    
    # Detection quality
    confidence: DetectionConfidence = Field(default=DetectionConfidence.MEDIUM)
    detection_notes: Optional[str] = Field(None, description="Notes about detection quality")


class WorkflowSummary(BaseModel):
    """Technical summary of detected playwright workflow."""
    
    task_type: str = Field(..., description="Type of workflow detected")
    total_duration: float = Field(..., description="Total duration in seconds")
    total_actions: int = Field(..., description="Total number of actions detected")
    
    # Action breakdown
    action_counts: Dict[str, int] = Field(default_factory=dict, description="Count by action type")
    unique_pages: List[str] = Field(default_factory=list, description="Unique pages visited")
    form_interactions: int = Field(default=0, description="Number of form interactions")
    
    # Technical metrics
    avg_action_duration: float = Field(..., description="Average action duration")
    longest_wait: float = Field(default=0.0, description="Longest wait period detected")
    navigation_count: int = Field(default=0, description="Number of navigation actions")
    
    # Complexity indicators
    tab_operations: int = Field(default=0, description="Number of tab operations")
    file_uploads: int = Field(default=0, description="Number of file uploads")
    dialog_interactions: int = Field(default=0, description="Number of dialog interactions")


class RecordingMetadata(BaseModel):
    """Metadata for the screen recording."""
    
    id: str = Field(..., description="Recording ID")
    duration: float = Field(..., description="Duration in seconds")
    resolution: str = Field(..., description="Screen resolution")
    fps: int = Field(default=30, description="Frames per second")
    
    # Browser context
    browser_type: Optional[str] = Field(None, description="Browser type")
    browser_version: Optional[str] = Field(None, description="Browser version")
    viewport_size: Optional[str] = Field(None, description="Browser viewport size")
    
    # Recording context
    primary_domain: Optional[str] = Field(None, description="Primary domain accessed")
    detected_apps: List[str] = Field(default_factory=list, description="Web applications detected")
    
    # Timestamps
    recorded_at: datetime = Field(..., description="Recording timestamp")
    processed_at: datetime = Field(default_factory=datetime.now, description="Processing timestamp")


class DetectionQuality(BaseModel):
    """Quality assessment of playwright action detection."""
    
    overall_confidence: DetectionConfidence = Field(..., description="Overall detection confidence")
    detection_method: str = Field(..., description="Method used for detection")
    
    # Quality metrics
    high_confidence_actions: int = Field(..., description="Actions with high confidence")
    low_confidence_actions: int = Field(..., description="Actions with low confidence")
    undetected_segments: int = Field(default=0, description="Segments where no actions detected")
    
    # Detection challenges
    occlusion_issues: List[str] = Field(default_factory=list, description="Areas with occlusion")
    timing_uncertainties: List[str] = Field(default_factory=list, description="Timing uncertainties")
    selector_ambiguities: List[str] = Field(default_factory=list, description="Ambiguous selectors")
    
    # Processing info
    processing_time: float = Field(..., description="Processing time in seconds")
    model_version: str = Field(..., description="Detection model version")


class PlaywrightTranscription(BaseModel):
    """Complete playwright action transcription from screen recording."""
    
    # Core components
    metadata: RecordingMetadata = Field(..., description="Recording metadata")
    summary: WorkflowSummary = Field(..., description="Workflow summary")
    actions: List[ActionStep] = Field(..., description="Detected playwright actions")
    quality: DetectionQuality = Field(..., description="Detection quality assessment")
    
    # MCP compatibility
    mcp_script: List[str] = Field(default_factory=list, description="Generated MCP commands")
    test_generation_ready: bool = Field(default=False, description="Ready for test generation")
    
    # Additional context
    workflow_patterns: List[str] = Field(default_factory=list, description="Detected workflow patterns")
    optimization_suggestions: List[str] = Field(default_factory=list, description="Script optimization suggestions")
    
    # Version
    version: str = Field(default="1.0", description="Transcription format version")

    def get_action(self, step_num: int) -> Optional[ActionStep]:
        """Get action by step number."""
        for action in self.actions:
            if action.num == step_num:
                return action
        return None
    
    def get_actions_by_type(self, action_type: PlaywrightAction) -> List[ActionStep]:
        """Get all actions of a specific type."""
        return [action for action in self.actions if action.action == action_type]
    
    def get_navigation_actions(self) -> List[ActionStep]:
        """Get all navigation-related actions."""
        nav_types = [
            PlaywrightAction.NAVIGATE, 
            PlaywrightAction.NAVIGATE_BACK, 
            PlaywrightAction.NAVIGATE_FORWARD
        ]
        return [action for action in self.actions if action.action in nav_types]
    
    def get_interaction_actions(self) -> List[ActionStep]:
        """Get all user interaction actions."""
        interaction_types = [
            PlaywrightAction.CLICK,
            PlaywrightAction.TYPE, 
            PlaywrightAction.SELECT,
            PlaywrightAction.CHECK,
            PlaywrightAction.SCROLL,
            PlaywrightAction.PRESS_KEY
        ]
        return [action for action in self.actions if action.action in interaction_types]
    
    def generate_mcp_commands(self) -> List[str]:
        """Generate MCP-compatible command list."""
        commands = []
        for action in self.actions:
            if action.action == PlaywrightAction.CLICK and action.selector:
                commands.append(f"browser_click(selector='{action.selector.value}')")
            elif action.action == PlaywrightAction.TYPE and action.text_input:
                commands.append(f"browser_type(text='{action.text_input}')")
            elif action.action == PlaywrightAction.NAVIGATE and action.url:
                commands.append(f"browser_navigate(url='{action.url}')")
            # Add more command generation logic as needed
        return commands
    
    def calc_detection_score(self) -> float:
        """Calculate detection accuracy score (0-1)."""
        if not self.actions:
            return 0.0
            
        total = len(self.actions)
        high_conf = len([a for a in self.actions if a.confidence == DetectionConfidence.HIGH])
        low_conf = len([a for a in self.actions if a.confidence == DetectionConfidence.LOW])
        
        # Weight high confidence positively, low confidence negatively
        score = (high_conf * 1.0 + (total - high_conf - low_conf) * 0.5) / total
        return max(0.0, min(1.0, score))