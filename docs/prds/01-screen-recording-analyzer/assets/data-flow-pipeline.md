# Screen Recording Workflow Analyzer - Data Flow Pipeline

## Data Processing Flow

```mermaid
flowchart TD
    %% Input Stage
    START([Video Upload]) --> VALIDATE{Video Valid?<br/>Format, Duration, Size}
    VALIDATE -->|No| ERROR[Error: Invalid Input]
    VALIDATE -->|Yes| EXTRACT[Extract Key Frames<br/>1-2 FPS Sampling]

    %% Analysis Stage
    EXTRACT --> ANALYZE[Gemini Flash 2.0<br/>Multimodal Analysis]
    ANALYZE --> STRUCT[Structured Output<br/>Generation]
    
    %% Business Logic Extraction
    STRUCT --> ACTIONS[Action Sequence<br/>Extraction]
    STRUCT --> INTENT[Intent Classification<br/>& Decision Patterns]
    STRUCT --> CONTEXT[Context Analysis<br/>& Business Rules]

    %% Artifact Generation
    ACTIONS --> GEN1[Generate<br/>Documentation]
    INTENT --> GEN2[Generate<br/>Playwright Script]
    CONTEXT --> GEN3[Generate<br/>SOP Document]

    %% Quality Validation Loop
    GEN1 --> CRITIC1{Documentation<br/>Quality Check}
    GEN2 --> CRITIC2{Script<br/>Quality Check}
    GEN3 --> CRITIC3{SOP<br/>Quality Check}

    %% Decision Points
    CRITIC1 -->|Score < 0.85| REFINE1[Refine Documentation]
    CRITIC2 -->|Score < 0.85| REFINE2[Refine Script]
    CRITIC3 -->|Score < 0.85| REFINE3[Refine SOP]

    REFINE1 --> CRITIC1
    REFINE2 --> CRITIC2
    REFINE3 --> CRITIC3

    CRITIC1 -->|Score ≥ 0.85| EXEC_CHECK{Playwright Script?}
    CRITIC2 -->|Score ≥ 0.85| CODE_EXEC[Code Execution<br/>Validation]
    CRITIC3 -->|Score ≥ 0.85| FINAL

    %% Code Execution Path
    CODE_EXEC --> EXEC_RESULT{Execution<br/>Successful?}
    EXEC_RESULT -->|No| AUTO_FIX[Generate<br/>Fixes]
    AUTO_FIX --> CRITIC2
    EXEC_RESULT -->|Yes| EXEC_CHECK

    %% Convergence Check
    EXEC_CHECK --> CONVERGE{Max Iterations<br/>Reached?}
    CONVERGE -->|No, Continue| ITERATION[Iteration + 1]
    ITERATION --> CRITIC1
    CONVERGE -->|Yes, Stop| FINAL

    %% Final Output
    FINAL[Final Artifacts<br/>Package]
    FINAL --> OUTPUT1[Natural Language<br/>Workflow Guide]
    FINAL --> OUTPUT2[Playwright<br/>Reference Script]
    FINAL --> OUTPUT3[Standard Operating<br/>Procedure]

    %% Error Handling
    ERROR --> END([Process End])
    FINAL --> SUCCESS([Success])

    %% Styling
    classDef input fill:#e3f2fd
    classDef process fill:#f1f8e9
    classDef decision fill:#fff3e0
    classDef output fill:#e8f5e8
    classDef error fill:#ffebee
    classDef success fill:#e0f2f1

    class START,EXTRACT input
    class ANALYZE,STRUCT,ACTIONS,INTENT,CONTEXT,GEN1,GEN2,GEN3,REFINE1,REFINE2,REFINE3,CODE_EXEC,AUTO_FIX,ITERATION,FINAL process
    class VALIDATE,CRITIC1,CRITIC2,CRITIC3,EXEC_CHECK,EXEC_RESULT,CONVERGE decision
    class OUTPUT1,OUTPUT2,OUTPUT3 output
    class ERROR error
    class SUCCESS success
```

## Data Flow Specifications

### Input Validation
- **Format Check**: MP4, WebM, AVI formats supported
- **Duration Limits**: 2-5 minute recordings only
- **Quality Thresholds**: Minimum resolution and frame rate requirements

### Analysis Pipeline
- **Frame Sampling**: Extract key frames at 1-2 FPS for efficiency
- **Multimodal Processing**: Combine visual and audio analysis
- **Structured Output**: JSON schema-compliant data extraction

### Business Logic Processing
- **Action Sequencing**: Chronological workflow step identification
- **Intent Classification**: Purpose and reasoning behind each action
- **Context Analysis**: Environmental factors and business rules

### Quality Assurance Flow
- **Iterative Refinement**: Up to 3 improvement cycles per artifact
- **Quality Thresholds**: Configurable acceptance criteria (default 0.85)
- **Code Validation**: Special handling for executable scripts

### Convergence Criteria
- **Score Threshold**: All artifacts must achieve minimum quality score
- **Iteration Limit**: Maximum refinement cycles to prevent infinite loops
- **Manual Override**: Option for human review and approval

### Output Generation
- **Parallel Processing**: All three artifacts generated simultaneously
- **Version Control**: Track refinement iterations and changes
- **Validation Evidence**: Include quality scores and critique feedback