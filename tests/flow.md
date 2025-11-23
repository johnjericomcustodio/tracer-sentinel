# Test Flow Diagram

```mermaid
flowchart TD
    Start([Test Execution]) --> LoadScenario[Load Scenario Data]
    LoadScenario --> Parser[CoordinateParser]
    
    Parser --> ParseInput[Parse Input File<br/>system_input_file.txt]
    Parser --> ParseOutput[Parse Output File<br/>system_output_file.txt]
    
    ParseInput --> ExtractRect[Extract Rectangle<br/>Work Area Coords]
    ParseInput --> ExtractExpected[Extract Expected<br/>Points Sequence]
    ParseOutput --> ExtractActual[Extract Actual<br/>Points Sequence]
    
    ExtractRect --> CheckParseFailures{Parsing<br/>Successful?}
    ExtractExpected --> CheckParseFailures
    ExtractActual --> CheckParseFailures
    
    CheckParseFailures -->|No| CollectFailures[Collect Parse Failures:<br/>- Rectangle failures<br/>- Expected points failures<br/>- Actual points failures]
    
    CheckParseFailures -->|Yes| CreateWorkArea[Create WorkArea<br/>with bounding box]
    CreateWorkArea --> CreateVerifier[Create TracerSentinel<br/>Verifier]
    
    CreateVerifier --> GeomCheck[Geometric Validity Check:<br/>Expected points within bounds?]
    GeomCheck --> SeqCheck[Sequence Sameness Check:<br/>Actual matches Expected?]
    
    SeqCheck --> CollectVerifierFailures[Collect Verifier Failures]
    
    CollectFailures --> CalcStatus{Calculate<br/>Overall Status}
    CollectVerifierFailures --> CalcStatus
    
    CalcStatus -->|Has Failures| StatusFail[Status = FAIL]
    CalcStatus -->|No Failures| StatusPass[Status = PASS]
    
    StatusFail --> CreateResults[Create ResultsBucket]
    StatusPass --> CreateResults
    
    CreateResults --> WriteResults[ResultsWriter:<br/>Write test_results.txt]
    WriteResults --> SavePlot[Save Visualization PNG:<br/>Work area + points]
    
    SavePlot --> Assert{Assert Based<br/>on Scenario Name}
    
    Assert -->|fail_* scenario| AssertHasFailures[Assert has_failures = True]
    Assert -->|pass_* scenario| AssertNoFailures[Assert has_failures = False]
    
    AssertHasFailures --> End([Test Complete])
    AssertNoFailures --> End
    
    style Start fill:#e1f5e1
    style End fill:#e1f5e1
    style StatusFail fill:#ffe1e1
    style StatusPass fill:#e1f5e1
    style CheckParseFailures fill:#fff4e1
    style CalcStatus fill:#fff4e1
    style Assert fill:#fff4e1
```

## Flow Description

### 1. Input Phase
- Load scenario data from test directory
- Initialize CoordinateParser with input/output file paths

### 2. Parsing Phase
- **Input File**: Extract rectangle coordinates and expected points sequence
- **Output File**: Extract actual points sequence
- Track parsing failures for each section

### 3. Validation Phase
- Check if parsing was successful
- If successful, create WorkArea and TracerSentinel verifier
- Run geometric validity check (points within bounds)
- Run sequence sameness check (actual matches expected)

### 4. Results Phase
- Collect all failures (parsing + verification)
- Calculate overall status (PASS/FAIL)
- Write results to `test_results.txt`
- Save visualization PNG with work area and points

### 5. Assertion Phase
- Validate that fail scenarios produce failures
- Validate that pass scenarios have no failures
