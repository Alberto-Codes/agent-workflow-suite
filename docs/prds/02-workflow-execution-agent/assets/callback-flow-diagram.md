# AI Workflow Execution Agent - ADK Callback Flow

## Three-Level Callback Architecture

```mermaid
flowchart TD
    %% Workflow Start
    START([Workflow Execution Start]) --> INIT[Initialize Work Item]
    INIT --> L3_START[Level 3: Workflow Start Callback]

    %% Level 3 Workflow Callback
    L3_START --> WF_SETUP[Setup Audit Trail<br/>Initialize Metrics<br/>Create Log Context]
    WF_SETUP --> STEP_LOOP{Next Workflow Step?}

    %% Step Level Processing
    STEP_LOOP -->|Yes| L2_STEP[Level 2: Step Start Callback]
    L2_STEP --> STEP_SETUP[Progress Tracking<br/>QA Checkpoint Setup<br/>Business Rule Context]
    
    STEP_SETUP --> ACTION_LOOP{Next Action in Step?}

    %% Action Level Processing
    ACTION_LOOP -->|Yes| L1_PRE[Level 1: Pre-Action Callback]
    L1_PRE --> PRE_ACTIONS[Take Screenshot<br/>Validate Current State<br/>Log Action Intent]
    
    PRE_ACTIONS --> EXECUTE[Execute Playwright Action]
    EXECUTE --> L1_POST[Level 1: Post-Action Callback]
    
    L1_POST --> POST_ACTIONS[Take Screenshot<br/>Validate Action Success<br/>Update Action Log]
    
    POST_ACTIONS --> ACTION_VALIDATE{Action Successful?}
    ACTION_VALIDATE -->|No| ERROR_HANDLE[Error Detection<br/>Recovery Suggestion]
    ERROR_HANDLE --> RETRY_DECIDE{Retry Action?}
    RETRY_DECIDE -->|Yes| L1_PRE
    RETRY_DECIDE -->|No| STEP_FAIL[Mark Step Failed]
    
    ACTION_VALIDATE -->|Yes| ACTION_LOOP

    %% Step Completion
    ACTION_LOOP -->|No More Actions| L2_END[Level 2: Step End Callback]
    L2_END --> STEP_VALIDATE[QA Step Validation<br/>Business Logic Check<br/>Progress Update]
    
    STEP_VALIDATE --> STEP_SUCCESS{Step Validation Passed?}
    STEP_SUCCESS -->|No| STEP_FAIL
    STEP_SUCCESS -->|Yes| STEP_COMPLETE[Mark Step Complete]
    
    STEP_COMPLETE --> STEP_LOOP
    STEP_FAIL --> ESCALATE{Escalation Required?}
    ESCALATE -->|Yes| MANUAL_REVIEW[Flag for Manual Review]
    ESCALATE -->|No| STEP_LOOP

    %% Workflow Completion
    STEP_LOOP -->|No More Steps| L3_END[Level 3: Workflow End Callback]
    L3_END --> WF_VALIDATE[Final QA Validation<br/>Completion Verification<br/>Audit Trail Finalization]
    
    WF_VALIDATE --> WF_SUCCESS{Workflow Successful?}
    WF_SUCCESS -->|Yes| SUCCESS_ACTIONS[Generate Success Report<br/>Archive Evidence<br/>Update Metrics]
    WF_SUCCESS -->|No| FAILURE_ACTIONS[Generate Failure Report<br/>Capture Error Evidence<br/>Update Metrics]
    
    SUCCESS_ACTIONS --> COMPLETE([Workflow Complete])
    FAILURE_ACTIONS --> COMPLETE
    MANUAL_REVIEW --> COMPLETE

    %% Styling for better dark/light theme compatibility
    classDef level1 fill:#F44336,stroke:#D32F2F,stroke-width:2px,color:#ffffff
    classDef level2 fill:#673AB7,stroke:#512DA8,stroke-width:2px,color:#ffffff
    classDef level3 fill:#009688,stroke:#00695C,stroke-width:2px,color:#ffffff
    classDef decision fill:#FF9800,stroke:#F57C00,stroke-width:2px,color:#ffffff
    classDef action fill:#4CAF50,stroke:#388E3C,stroke-width:2px,color:#ffffff
    classDef endpoint fill:#E91E63,stroke:#C2185B,stroke-width:2px,color:#ffffff

    class L1_PRE,L1_POST,PRE_ACTIONS,POST_ACTIONS level1
    class L2_STEP,L2_END,STEP_SETUP,STEP_VALIDATE,STEP_COMPLETE level2
    class L3_START,L3_END,WF_SETUP,WF_VALIDATE,SUCCESS_ACTIONS,FAILURE_ACTIONS level3
    class ACTION_VALIDATE,STEP_SUCCESS,WF_SUCCESS,RETRY_DECIDE,ESCALATE decision
    class EXECUTE,ERROR_HANDLE,STEP_FAIL,MANUAL_REVIEW action
    class START,COMPLETE endpoint
```

## Callback Level Specifications

### Level 1: Action-Level Callbacks (@callback.on_action)

#### Pre-Action Callback
```python
@callback.on_action(trigger="before")
def pre_action_callback(context):
    # Automatic screenshot capture
    screenshot_path = take_screenshot(f"before_{context.action_name}")
    
    # Validate current page state
    current_state = validate_page_state()
    
    # Log action intent
    log_action_intent(context.action_name, context.parameters)
    
    return {
        "screenshot": screenshot_path,
        "state_valid": current_state.is_valid,
        "ready_for_action": True
    }
```

#### Post-Action Callback
```python
@callback.on_action(trigger="after")
def post_action_callback(context, result):
    # Capture result screenshot
    screenshot_path = take_screenshot(f"after_{context.action_name}")
    
    # Validate action success
    success_validated = validate_action_result(context.action_name, result)
    
    # Update execution log
    update_action_log(context.action_name, result, success_validated)
    
    # Error detection
    if not success_validated:
        error_info = detect_action_errors()
        suggest_recovery_actions(error_info)
        
    return {
        "screenshot": screenshot_path,
        "success": success_validated,
        "error_info": error_info if not success_validated else None
    }
```

### Level 2: Step-Level Callbacks (@callback.on_step)

#### Step Start Callback
```python
@callback.on_step(trigger="start")
def step_start_callback(context):
    # Initialize step tracking
    progress_tracker.start_step(context.step_name)
    
    # Setup QA checkpoint
    qa_checkpoint = setup_qa_validation(context.step_requirements)
    
    # Load business rule context
    business_rules = load_business_rules(context.step_name)
    
    return {
        "step_id": generate_step_id(),
        "qa_checkpoint": qa_checkpoint,
        "business_rules": business_rules
    }
```

#### Step End Callback
```python
@callback.on_step(trigger="end")
def step_end_callback(context, step_results):
    # QA validation of step completion
    qa_result = qa_agent.validate_step_completion(
        step_name=context.step_name,
        actions_taken=step_results.actions,
        expected_outcome=context.expected_outcome
    )
    
    # Business logic compliance check
    compliance_check = validate_business_rules(
        step_results, context.business_rules
    )
    
    # Update progress tracking
    progress_tracker.complete_step(context.step_name, qa_result.success)
    
    return {
        "qa_validation": qa_result,
        "compliance": compliance_check,
        "step_success": qa_result.success and compliance_check.passed
    }
```

### Level 3: Workflow-Level Callbacks (@callback.on_workflow)

#### Workflow Start Callback
```python
@callback.on_workflow(trigger="start")
def workflow_start_callback(context):
    # Initialize audit trail
    audit_trail = AuditTrail(
        workflow_id=context.workflow_id,
        work_item=context.work_item,
        artifacts_used=context.workflow_artifacts
    )
    
    # Setup metrics collection
    metrics_collector = MetricsCollector(context.workflow_id)
    
    # Create execution log context
    execution_log = ExecutionLog(context.workflow_id)
    
    return {
        "audit_trail": audit_trail,
        "metrics_collector": metrics_collector,
        "execution_log": execution_log
    }
```

#### Workflow End Callback
```python
@callback.on_workflow(trigger="end")
def workflow_end_callback(context, workflow_results):
    # Final QA validation
    final_validation = qa_agent.validate_workflow_completion(
        workflow_results, context.success_criteria
    )
    
    # Generate completion evidence
    evidence_package = collect_completion_evidence(
        screenshots=context.screenshots,
        logs=context.execution_log,
        validation_results=final_validation
    )
    
    # Finalize audit trail
    audit_trail.finalize(
        success=final_validation.success,
        evidence=evidence_package,
        completion_time=datetime.now()
    )
    
    # Generate reports
    completion_report = generate_completion_report(
        work_item=context.work_item,
        success=final_validation.success,
        evidence=evidence_package
    )
    
    return {
        "final_validation": final_validation,
        "evidence_package": evidence_package,
        "completion_report": completion_report
    }
```

## Callback Integration Benefits

### Automated Quality Assurance
- **Continuous Validation**: Every action and step automatically validated
- **Real-time Error Detection**: Immediate identification of workflow deviations
- **Evidence Collection**: Automatic screenshot and log generation
- **Business Rule Compliance**: Automated verification against documented procedures

### Comprehensive Audit Trail
- **Complete Documentation**: Every action logged with context and validation
- **Visual Evidence**: Screenshots at key workflow points
- **Compliance Reporting**: Automated generation of audit-ready documentation
- **Traceability**: Full path from work item to completion with evidence

### Intelligent Error Recovery
- **Automatic Detection**: Callback-triggered error identification
- **Recovery Suggestions**: AI-powered recommendations for corrective actions
- **Retry Logic**: Intelligent retry mechanisms with learned patterns
- **Escalation Management**: Automated escalation when recovery fails

### Performance Optimization
- **Metrics Collection**: Automatic performance and quality data gathering
- **Pattern Recognition**: Learn from successful and failed workflows
- **Optimization Opportunities**: Identify bottlenecks and improvement areas
- **Quality Improvement**: Continuous enhancement through feedback loops