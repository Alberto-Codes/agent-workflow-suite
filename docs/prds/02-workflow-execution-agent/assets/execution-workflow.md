# AI Workflow Execution Agent - Execution Workflow

## Work Item Processing Flow

```mermaid
flowchart TD
    %% Initialization
    START([System Start]) --> LOAD_CONFIG[Load Configuration<br/>& Artifacts]
    LOAD_CONFIG --> VALIDATE_INPUTS{Validate Inputs?}
    VALIDATE_INPUTS -->|Failed| CONFIG_ERROR[Configuration Error<br/>Exit System]
    VALIDATE_INPUTS -->|Success| LOAD_QUEUE[Load Work Queue<br/>from CSV]

    %% Work Queue Processing
    LOAD_QUEUE --> QUEUE_VALIDATE{Queue Valid?}
    QUEUE_VALIDATE -->|Failed| QUEUE_ERROR[Queue Error<br/>Fix and Retry]
    QUEUE_VALIDATE -->|Success| WORK_LOOP{Next Work Item?}

    %% Individual Work Item Processing
    WORK_LOOP -->|Yes| GET_ITEM[Get Next Work Item]
    GET_ITEM --> ITEM_VALIDATE{Item Valid?}
    ITEM_VALIDATE -->|Failed| SKIP_ITEM[Skip Item<br/>Log Error]
    ITEM_VALIDATE -->|Success| INIT_BROWSER[Initialize Browser<br/>Session]

    %% Browser Setup
    INIT_BROWSER --> BROWSER_READY{Browser Ready?}
    BROWSER_READY -->|Failed| BROWSER_ERROR[Browser Error<br/>Retry or Skip]
    BROWSER_READY -->|Success| INTERPRET_ARTIFACTS[Interpret Workflow<br/>Artifacts]

    %% Artifact Interpretation
    INTERPRET_ARTIFACTS --> PLAN_EXECUTION[Plan Execution<br/>Strategy]
    PLAN_EXECUTION --> START_WORKFLOW[Start Workflow<br/>Execution]

    %% Workflow Execution with Callbacks
    START_WORKFLOW --> WF_CALLBACK_START[Workflow Start<br/>Callback]
    WF_CALLBACK_START --> STEP_ITERATOR{Next Step?}

    %% Step Processing Loop
    STEP_ITERATOR -->|Yes| STEP_CALLBACK_START[Step Start<br/>Callback]
    STEP_CALLBACK_START --> INTERPRET_STEP[Interpret Step<br/>from Artifacts]
    INTERPRET_STEP --> ACTION_ITERATOR{Next Action?}

    %% Action Processing Loop
    ACTION_ITERATOR -->|Yes| ACTION_CALLBACK_PRE[Pre-Action<br/>Callback]
    ACTION_CALLBACK_PRE --> SCREENSHOT_PRE[Take Screenshot<br/>Validate State]
    SCREENSHOT_PRE --> EXECUTE_ACTION[Execute Playwright<br/>Action]

    %% Action Execution Decision Tree
    EXECUTE_ACTION --> ACTION_RESULT{Action Success?}
    ACTION_RESULT -->|Success| ACTION_CALLBACK_POST[Post-Action<br/>Callback]
    ACTION_RESULT -->|Failed| ERROR_ANALYSIS[Analyze Error<br/>& Context]

    %% Error Handling
    ERROR_ANALYSIS --> ERROR_TYPE{Error Type?}
    ERROR_TYPE -->|Element Not Found| ADAPT_SELECTOR[Adapt Element<br/>Selection Strategy]
    ERROR_TYPE -->|Page Not Ready| WAIT_RETRY[Wait & Retry<br/>Action]
    ERROR_TYPE -->|Business Logic| CONSULT_ARTIFACTS[Consult Artifacts<br/>for Guidance]
    ERROR_TYPE -->|Critical Error| ESCALATE_ERROR[Escalate to<br/>Manual Review]

    %% Recovery Attempts
    ADAPT_SELECTOR --> RETRY_ACTION[Retry Action with<br/>New Strategy]
    WAIT_RETRY --> RETRY_ACTION
    CONSULT_ARTIFACTS --> ADAPTIVE_EXECUTE[Execute with<br/>Adapted Approach]
    RETRY_ACTION --> RETRY_LIMIT{Retry Limit<br/>Reached?}
    RETRY_LIMIT -->|No| EXECUTE_ACTION
    RETRY_LIMIT -->|Yes| ESCALATE_ERROR
    ADAPTIVE_EXECUTE --> ACTION_RESULT

    %% Successful Action Processing
    ACTION_CALLBACK_POST --> SCREENSHOT_POST[Take Screenshot<br/>Validate Result]
    SCREENSHOT_POST --> QA_ACTION_CHECK[QA Agent<br/>Action Validation]
    QA_ACTION_CHECK --> QA_ACTION_RESULT{QA Validation<br/>Passed?}
    QA_ACTION_RESULT -->|Failed| QA_ACTION_RETRY[QA-Suggested<br/>Corrective Action]
    QA_ACTION_RETRY --> EXECUTE_ACTION
    QA_ACTION_RESULT -->|Passed| ACTION_ITERATOR

    %% Step Completion
    ACTION_ITERATOR -->|No More Actions| STEP_CALLBACK_END[Step End<br/>Callback]
    STEP_CALLBACK_END --> QA_STEP_CHECK[QA Agent<br/>Step Validation]
    QA_STEP_CHECK --> QA_STEP_RESULT{Step Validation<br/>Passed?}
    QA_STEP_RESULT -->|Failed| STEP_RECOVERY[Step Recovery<br/>or Skip]
    QA_STEP_RESULT -->|Passed| STEP_COMPLETE[Mark Step<br/>Complete]
    STEP_COMPLETE --> STEP_ITERATOR

    %% Workflow Completion
    STEP_ITERATOR -->|No More Steps| WF_CALLBACK_END[Workflow End<br/>Callback]
    WF_CALLBACK_END --> FINAL_QA[Final QA<br/>Validation]
    FINAL_QA --> FINAL_VALIDATION{Workflow<br/>Successful?}

    %% Success Path
    FINAL_VALIDATION -->|Success| COLLECT_EVIDENCE[Collect Success<br/>Evidence]
    COLLECT_EVIDENCE --> GENERATE_REPORT[Generate Success<br/>Report]
    GENERATE_REPORT --> UPDATE_CSV_SUCCESS[Update CSV<br/>Status: Success]

    %% Failure Path
    FINAL_VALIDATION -->|Failed| COLLECT_FAILURE[Collect Failure<br/>Evidence]
    STEP_RECOVERY --> COLLECT_FAILURE
    ESCALATE_ERROR --> COLLECT_FAILURE
    COLLECT_FAILURE --> GENERATE_FAILURE[Generate Failure<br/>Report]
    GENERATE_FAILURE --> UPDATE_CSV_FAILED[Update CSV<br/>Status: Failed]

    %% Cleanup and Continue
    UPDATE_CSV_SUCCESS --> CLEANUP_BROWSER[Cleanup Browser<br/>Session]
    UPDATE_CSV_FAILED --> CLEANUP_BROWSER
    CLEANUP_BROWSER --> SKIP_ITEM
    SKIP_ITEM --> WORK_LOOP

    %% Final Completion
    WORK_LOOP -->|No More Items| FINAL_REPORT[Generate Final<br/>Execution Report]
    FINAL_REPORT --> ARCHIVE_RESULTS[Archive Results<br/>& Evidence]
    ARCHIVE_RESULTS --> END([Execution Complete])

    %% Error Exits
    CONFIG_ERROR --> END
    QUEUE_ERROR --> END
    BROWSER_ERROR --> WORK_LOOP

    %% Styling
    classDef start fill:#e0f2f1
    classDef process fill:#f1f8e9
    classDef decision fill:#fff3e0
    classDef callback fill:#e8eaf6
    classDef error fill:#ffebee
    classDef success fill:#e8f5e8
    classDef end fill:#fce4ec

    class START,END start
    class LOAD_CONFIG,LOAD_QUEUE,GET_ITEM,INIT_BROWSER,INTERPRET_ARTIFACTS,PLAN_EXECUTION,START_WORKFLOW,INTERPRET_STEP,EXECUTE_ACTION,SCREENSHOT_PRE,SCREENSHOT_POST,COLLECT_EVIDENCE,COLLECT_FAILURE,GENERATE_REPORT,GENERATE_FAILURE,CLEANUP_BROWSER,FINAL_REPORT,ARCHIVE_RESULTS process
    class VALIDATE_INPUTS,QUEUE_VALIDATE,ITEM_VALIDATE,BROWSER_READY,ACTION_RESULT,ERROR_TYPE,RETRY_LIMIT,QA_ACTION_RESULT,QA_STEP_RESULT,FINAL_VALIDATION,WORK_LOOP,STEP_ITERATOR,ACTION_ITERATOR decision
    class WF_CALLBACK_START,WF_CALLBACK_END,STEP_CALLBACK_START,STEP_CALLBACK_END,ACTION_CALLBACK_PRE,ACTION_CALLBACK_POST callback
    class CONFIG_ERROR,QUEUE_ERROR,BROWSER_ERROR,ERROR_ANALYSIS,ESCALATE_ERROR,STEP_RECOVERY error
    class UPDATE_CSV_SUCCESS,QA_ACTION_CHECK,QA_STEP_CHECK,FINAL_QA success
```

## Processing Stages Detail

### Initialization Phase
1. **Configuration Loading**: Load execution parameters, quality thresholds, retry policies
2. **Artifact Validation**: Verify workflow artifacts from SRWA-2025 are complete and valid
3. **Queue Processing**: Parse and validate CSV work items for processing

### Work Item Execution
1. **Browser Session Management**: Initialize clean browser environment for each work item
2. **Artifact Interpretation**: Parse workflow guidance and create execution plan
3. **Adaptive Execution**: Use artifacts as baseline with intelligent adaptation to UI variations

### Quality Assurance Integration
1. **Real-time Validation**: QA agent continuously validates progress and decisions
2. **Error Detection**: Immediate identification of workflow deviations or failures
3. **Recovery Mechanisms**: Intelligent retry logic and corrective action suggestions

### Evidence Collection
1. **Screenshot Documentation**: Automated capture at key workflow points
2. **Execution Logging**: Detailed action-by-action documentation
3. **Validation Records**: QA assessments and compliance verification

## Error Handling Strategies

### Error Classification
- **Element Not Found**: UI changes requiring selector adaptation
- **Page Not Ready**: Timing issues requiring wait/retry logic
- **Business Logic**: Decision points requiring artifact consultation
- **Critical Errors**: Failures requiring manual intervention

### Recovery Mechanisms
- **Adaptive Selectors**: Multiple element finding strategies
- **Intelligent Retries**: Context-aware retry with exponential backoff
- **Artifact Consultation**: Reference natural language guide for alternative approaches
- **QA-Guided Recovery**: Use QA agent suggestions for corrective actions

### Escalation Procedures
- **Retry Limits**: Prevent infinite loops with configurable retry counts
- **Manual Review**: Flag complex issues for human intervention
- **Partial Completion**: Handle scenarios where workflow partially completes
- **Error Documentation**: Comprehensive logging for troubleshooting

## Performance Considerations

### Concurrency Management
- **Browser Pooling**: Reuse browser instances when possible
- **Resource Limits**: Manage memory and CPU usage with concurrent executions
- **Queue Optimization**: Intelligent work item ordering and batching

### Monitoring and Metrics
- **Real-time Progress**: Live updates on processing status and completion rates
- **Quality Metrics**: Track QA validation success rates and error patterns
- **Performance Analytics**: Monitor execution times and resource utilization
- **Trend Analysis**: Identify patterns in successes, failures, and optimizations