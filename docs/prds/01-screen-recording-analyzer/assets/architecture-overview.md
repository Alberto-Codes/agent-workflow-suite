# Screen Recording Workflow Analyzer - Architecture Overview

## System Architecture Diagram

```mermaid
graph TB
    %% Input Layer
    subgraph "Input Layer"
        VI[Screen Recording<br/>MP4/WebM<br/>2-5 minutes]
        CONFIG[Configuration<br/>Templates & Schemas]
    end

    %% Processing Layer
    subgraph "Processing Layer"
        VP[Video Processor<br/>Frame Extraction]
        GA[Gemini Flash 2.0<br/>Analysis Engine]
        BLE[Business Logic<br/>Extractor]
    end

    %% Generator Agents
    subgraph "Generator Agents"
        DGA[Documentation<br/>Generator Agent]
        PGA[Playwright<br/>Generator Agent]
        SGA[SOP<br/>Generator Agent]
    end

    %% Critic Agents
    subgraph "Critic Agents"
        DCA[Documentation<br/>Critic Agent]
        PCA[Playwright<br/>Critic Agent]
        SCA[SOP<br/>Critic Agent]
    end

    %% Validation Layer
    subgraph "Validation Layer"
        CEA[Code Execution<br/>Agent]
        QT[Quality<br/>Thresholds]
        IR[Iterative<br/>Refinement]
    end

    %% Output Layer
    subgraph "Output Artifacts"
        NL[Natural Language<br/>Workflow Guide]
        PS[Playwright<br/>Reference Script]
        SOP[Standard Operating<br/>Procedure]
    end

    %% Data Flow
    VI --> VP
    CONFIG --> GA
    VP --> GA
    GA --> BLE
    BLE --> DGA
    BLE --> PGA
    BLE --> SGA

    DGA --> DCA
    PGA --> PCA
    SGA --> SCA

    DCA --> IR
    PCA --> IR
    SCA --> IR

    PGA --> CEA
    CEA --> QT
    IR --> QT

    QT --> NL
    QT --> PS
    QT --> SOP

    %% Feedback Loops
    DCA -.->|Feedback| DGA
    PCA -.->|Feedback| PGA
    SCA -.->|Feedback| SGA
    CEA -.->|Code Fixes| PGA

    %% Styling
    classDef input fill:#e1f5fe
    classDef processing fill:#f3e5f5
    classDef generator fill:#e8f5e8
    classDef critic fill:#fff3e0
    classDef validation fill:#fce4ec
    classDef output fill:#e0f2f1

    class VI,CONFIG input
    class VP,GA,BLE processing
    class DGA,PGA,SGA generator
    class DCA,PCA,SCA critic
    class CEA,QT,IR validation
    class NL,PS,SOP output
```

## Component Responsibilities

### Input Layer
- **Screen Recording**: Raw video input containing browser workflow
- **Configuration**: Templates, schemas, and processing parameters

### Processing Layer
- **Video Processor**: Frame extraction and preprocessing
- **Gemini Flash 2.0**: Core AI analysis engine for multimodal processing
- **Business Logic Extractor**: Specialized component for decision pattern recognition

### Generator Agents
- **Documentation Generator**: Creates natural language workflow descriptions
- **Playwright Generator**: Produces automation script templates
- **SOP Generator**: Builds compliance documentation

### Critic Agents
- **Documentation Critic**: Validates accuracy and completeness of workflow descriptions
- **Playwright Critic**: Reviews script quality and viability
- **SOP Critic**: Ensures compliance with industry standards

### Validation Layer
- **Code Execution Agent**: Tests and debugs generated scripts
- **Quality Thresholds**: Configurable acceptance criteria
- **Iterative Refinement**: Orchestrates improvement cycles

### Output Artifacts
- **Natural Language Guide**: Human-readable workflow with metadata
- **Playwright Script**: Automation code template
- **Standard Operating Procedure**: Compliance documentation