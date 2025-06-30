# AI Workflow Execution Agent - System Architecture

## System Architecture Overview

```mermaid
graph TB
    %% Input Sources
    subgraph "Input Sources"
        WA[Workflow Artifacts<br/>from SRWA-2025]
        CSV[Work Queue<br/>CSV File]
        CONFIG[Execution<br/>Configuration]
    end

    %% Workflow Artifacts Detail
    subgraph "Workflow Artifacts"
        NLG[Natural Language<br/>Workflow Guide]
        PSC[Playwright<br/>Reference Script]
        SOP[Standard Operating<br/>Procedure]
    end

    %% Core Execution Engine
    subgraph "Execution Engine"
        AI[AI Agent<br/>Gemini Flash 2.0]
        WI[Workflow<br/>Interpreter]
        ATP[Adaptive Task<br/>Planner]
    end

    %% Playwright Tool Layer
    subgraph "Playwright Tool Wrappers"
        NAV[Navigation Tools<br/>URL, Page Loads]
        INT[Interaction Tools<br/>Click, Type, Select]
        ANA[Analysis Tools<br/>Screenshots, Elements]
        VAL[Validation Tools<br/>State Checks, Errors]
    end

    %% Browser Interface
    subgraph "Browser Environment"
        BROWSER[Headless/Headed<br/>Browser Instance]
        PAGES[Web Pages &<br/>Applications]
    end

    %% Callback System (ADK)
    subgraph "ADK Callback System"
        L1[Level 1: Action Callbacks<br/>Screenshot, Validation]
        L2[Level 2: Step Callbacks<br/>Progress, QA Checks]
        L3[Level 3: Workflow Callbacks<br/>Completion, Audit]
    end

    %% QA Validation Agent
    subgraph "QA Validation System"
        QAA[QA Reasoning<br/>Agent]
        SVA[Screenshot<br/>Validator]
        BLV[Business Logic<br/>Validator]
        ERR[Error Detection<br/>& Recovery]
    end

    %% Audit & Logging
    subgraph "Audit Trail System"
        LOGGER[Execution<br/>Logger]
        SCREEN[Screenshot<br/>Manager]
        EVIDENCE[Evidence<br/>Collector]
        REPORT[Report<br/>Generator]
    end

    %% Output Layer
    subgraph "Output Layer"
        COMPLETION[Work Completion<br/>CSV]
        SCREENSHOTS[Validation<br/>Screenshots]
        LOGS[Detailed<br/>Execution Logs]
        METRICS[Quality<br/>Metrics]
    end

    %% Data Flow Connections
    WA --> WI
    CSV --> AI
    CONFIG --> AI
    
    NLG --> WI
    PSC --> WI
    SOP --> WI
    
    WI --> AI
    AI --> ATP
    ATP --> NAV
    ATP --> INT
    ATP --> ANA
    ATP --> VAL
    
    NAV --> BROWSER
    INT --> BROWSER
    ANA --> BROWSER
    VAL --> BROWSER
    
    BROWSER --> PAGES
    
    %% Callback Triggers
    NAV --> L1
    INT --> L1
    ANA --> L1
    VAL --> L1
    
    ATP --> L2
    AI --> L3
    
    %% QA Integration
    L1 --> QAA
    L2 --> QAA
    L3 --> QAA
    
    QAA --> SVA
    QAA --> BLV
    QAA --> ERR
    
    SVA --> SCREEN
    BLV --> AI
    ERR --> ATP
    
    %% Audit Trail
    L1 --> LOGGER
    L2 --> LOGGER
    L3 --> LOGGER
    
    LOGGER --> EVIDENCE
    SCREEN --> EVIDENCE
    QAA --> EVIDENCE
    
    EVIDENCE --> REPORT
    
    %% Final Outputs
    REPORT --> COMPLETION
    SCREEN --> SCREENSHOTS
    LOGGER --> LOGS
    QAA --> METRICS

    %% Styling for better dark/light theme compatibility
    classDef input fill:#2196F3,stroke:#1976D2,stroke-width:2px,color:#ffffff
    classDef artifacts fill:#4CAF50,stroke:#388E3C,stroke-width:2px,color:#ffffff
    classDef execution fill:#FF9800,stroke:#F57C00,stroke-width:2px,color:#ffffff
    classDef tools fill:#E91E63,stroke:#C2185B,stroke-width:2px,color:#ffffff
    classDef browser fill:#673AB7,stroke:#512DA8,stroke-width:2px,color:#ffffff
    classDef callbacks fill:#009688,stroke:#00695C,stroke-width:2px,color:#ffffff
    classDef qa fill:#FFC107,stroke:#FFA000,stroke-width:2px,color:#000000
    classDef audit fill:#9C27B0,stroke:#7B1FA2,stroke-width:2px,color:#ffffff
    classDef output fill:#8BC34A,stroke:#689F38,stroke-width:2px,color:#ffffff

    class WA,CSV,CONFIG input
    class NLG,PSC,SOP artifacts
    class AI,WI,ATP execution
    class NAV,INT,ANA,VAL tools
    class BROWSER,PAGES browser
    class L1,L2,L3 callbacks
    class QAA,SVA,BLV,ERR qa
    class LOGGER,SCREEN,EVIDENCE,REPORT audit
    class COMPLETION,SCREENSHOTS,LOGS,METRICS output
```

## Component Specifications

### Input Processing
- **Workflow Artifacts**: Consume and interpret SRWA-2025 generated training data
- **Work Queue**: Process CSV files with configurable column mapping
- **Configuration**: Execution parameters, quality thresholds, retry policies

### Execution Engine
- **AI Agent**: Gemini Flash 2.0 for intelligent decision-making and adaptation
- **Workflow Interpreter**: Parse and understand artifact guidance
- **Adaptive Task Planner**: Dynamic workflow execution with real-time adaptation

### Playwright Tool Wrappers
- **Navigation Tools**: URL navigation, page load management, redirect handling
- **Interaction Tools**: Element interaction with validation and error handling
- **Analysis Tools**: Page inspection, element discovery, content extraction
- **Validation Tools**: State verification, error detection, completion confirmation

### ADK Callback Integration
- **Level 1 (Action)**: Automatic screenshots, immediate validation, error detection
- **Level 2 (Step)**: Progress tracking, QA checkpoints, business rule validation
- **Level 3 (Workflow)**: Completion verification, audit trail generation, metrics collection

### QA Validation System
- **QA Reasoning Agent**: Intelligent assessment of workflow progress and quality
- **Screenshot Validator**: Visual confirmation of UI states and expected outcomes
- **Business Logic Validator**: Ensure compliance with documented procedures
- **Error Detection**: Real-time issue identification with recovery suggestions

### Audit Trail System
- **Execution Logger**: Comprehensive action and decision logging
- **Screenshot Manager**: Automated capture, labeling, and organization
- **Evidence Collector**: Aggregate validation artifacts and compliance data
- **Report Generator**: Create audit-ready documentation packages

## Integration Points

### SRWA-2025 Dependencies
- **Artifact Format**: Standardized structure for workflow guidance consumption
- **Quality Indicators**: Confidence scores and reliability metrics from source
- **Business Logic**: Decision criteria and procedural guidance integration

### Browser Environment
- **Multi-Browser Support**: Chromium, Firefox, Safari compatibility
- **Session Management**: Cookie handling, authentication, state persistence
- **Resource Optimization**: Efficient browser instance management and cleanup

### External Systems
- **Work Queue Sources**: Integration with ticketing systems, databases, APIs
- **Validation Endpoints**: External verification systems and data sources
- **Reporting Destinations**: Audit systems, compliance platforms, dashboards