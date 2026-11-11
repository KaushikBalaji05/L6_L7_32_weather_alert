# L6_L7_32 — Weather Alert Classifier

Lab 7: Fuzz Testing for Input Validation Bugs

## About

A robust Python module that parses meteorological readings, classifies wind speed alerts, and calculates rainfall spread. This module has been hardened against edge cases, unexpected types, malformed strings, and physical domain violations using property-based fuzz testing with **Hypothesis**.

## Deliverables & Directory Structure

```
lab7/
├── processor.py                       # Hardened application code under test
├── weather_alert.py                   # Canonical repository module under test
├── test_processor.py                  # Hypothesis property-based fuzz test suite
├── test_weather_alert.py              # Canonical test suite
├── requirements.txt                   # Required Python packages
├── Lab7_FuzzTesting_Final_Report.pdf  # Comprehensive final laboratory PDF report
├── generate_report.py                 # Automated report generator (ReportLab)
├── render_evidence.py                 # Authentic evidence screenshot generator
├── evidence/                          # Genuine execution terminal screenshots
│   ├── 01_original_processor.png      # Baseline execution with valid inputs
│   ├── 02_initial_fuzz_failures.png   # 6 initial failures uncovered by Hypothesis
│   ├── 03_failure_analysis.png        # Shrunk counterexamples and stack traces
│   ├── 04_fixed_processor.png         # Hardened application execution
│   └── 05_final_passing_tests.png     # 100% passing tests (9 passed, 0 failed)
└── README.md                          # Documentation and instructions
```

## Setup & Dependencies

Install required testing and reporting packages:

```bash
pip install -r requirements.txt
# or individually:
pip install hypothesis pytest reportlab pillow
```

## Running the Application

Execute the application interactively:

```bash
python processor.py
# or
python weather_alert.py
```

## Running the Hypothesis Test Suite

Run property-based fuzz tests with verbose output:

```bash
python -m pytest -v test_processor.py
# or
python -m pytest -v test_weather_alert.py
```

All 9 tests will execute hundreds of randomized property iterations and pass with 0 failures.