# Screen Recording Workflow Analyzer - Multi-Agent Workflow

## Generator-Critic Pattern Sequence

```mermaid
sequenceDiagram
    participant O as Orchestrator
    participant VA as Video Analysis
    participant DG as Doc Generator
    participant PG as Playwright Generator  
    participant SG as SOP Generator
    participant DC as Doc Critic
    participant PC as Playwright Critic
    participant SC as SOP Critic
    participant CE as Code Executor
    participant QM as Quality Manager

    Note over O: Workflow Initialization
    O->>VA: Process Video Input
    VA->>O: Return Structured Analysis

    Note over O,SG: Initial Generation Phase
    par Generate All Artifacts
        O->>DG: Generate Documentation
        DG->>O: Natural Language Guide v1
    and
        O->>PG: Generate Playwright Script
        PG->>O: Automation Script v1
    and
        O->>SG: Generate SOP Document
        SG->>O: Procedure Document v1
    end

    Note over O,QM: Quality Validation Phase
    loop Iterative Refinement (Max 3 cycles)
        Note over DC,SC: Parallel Critique
        par Critique All Artifacts
            O->>DC: Validate Documentation
            DC->>O: Critique + Score
        and
            O->>PC: Validate Script
            PC->>O: Critique + Score
        and
            O->>SC: Validate SOP
            SC->>O: Critique + Score
        end

        Note over O: Quality Assessment
        O->>QM: Check Quality Thresholds
        QM->>O: Quality Status Report

        alt All Scores ≥ 0.85
            Note over O: Quality Threshold Met
            O->>CE: Validate Playwright Script
            CE->>O: Execution Results
            
            alt Script Execution Successful
                Note over O: Validation Complete
            else Script Issues Found
                CE->>PG: Send Fix Suggestions
                PG->>O: Improved Script
                O->>PC: Re-validate Script
                PC->>O: Updated Critique
            end
        else Quality Improvements Needed
            Note over O,SG: Refinement Required
            par Refine Based on Critique
                alt Doc Score < 0.85
                    O->>DG: Refine with Feedback
                    DG->>O: Improved Documentation
                end
            and
                alt Script Score < 0.85
                    O->>PG: Refine with Feedback
                    PG->>O: Improved Script
                end
            and
                alt SOP Score < 0.85
                    O->>SG: Refine with Feedback
                    SG->>O: Improved SOP
                end
            end
        end

        O->>QM: Check Convergence
        alt Quality Achieved or Max Iterations
            Note over O: Exit Refinement Loop
        else Continue Refinement
            Note over O: Next Iteration
        end
    end

    Note over O: Final Output Generation
    O->>QM: Generate Final Package
    QM->>O: Validated Artifacts

    Note over O: Success
    O-->>O: Archive Results & Metrics
```

## Agent Interaction Patterns

### Orchestrator Agent
- **Role**: Workflow coordination and decision management
- **Responsibilities**: Task distribution, quality monitoring, convergence detection
- **Communication**: Coordinates all agent interactions and maintains state

### Generator Agents
- **Documentation Generator**: Creates natural language workflow descriptions
- **Playwright Generator**: Produces automation scripts with business logic
- **SOP Generator**: Builds compliance documentation following templates

### Critic Agents
- **Documentation Critic**: Validates accuracy, completeness, and clarity
- **Playwright Critic**: Reviews script structure, reliability, and best practices
- **SOP Critic**: Ensures compliance with industry standards and completeness

### Specialized Agents
- **Code Executor**: Tests script viability and suggests improvements
- **Quality Manager**: Monitors thresholds and manages convergence criteria

## Communication Protocols

### Message Types
- **Task Assignment**: Orchestrator → Generator/Critic
- **Artifact Delivery**: Generator → Orchestrator
- **Critique Feedback**: Critic → Orchestrator → Generator
- **Quality Assessment**: Quality Manager → Orchestrator
- **Refinement Request**: Orchestrator → Generator (with feedback)

### Quality Metrics Exchange
- **Confidence Scores**: 0.0 - 1.0 scale for each artifact
- **Issue Categories**: Critical, Major, Minor classification
- **Improvement Suggestions**: Specific actionable feedback
- **Validation Evidence**: Screenshots, logs, test results

### Convergence Signals
- **Quality Achieved**: All scores meet threshold criteria
- **Max Iterations**: Iteration limit reached (safety mechanism)
- **Manual Override**: Human intervention required
- **System Error**: Technical failure requiring escalation