Production AI Incident Response Platform

An AI-powered incident investigation system designed around observability, evidence-grounded AI, evaluation, and governance.

The project simulates a production environment where application and tool-level failures are detected automatically, investigated by an AI agent, and evaluated to determine whether the AI’s conclusions are supported by the available evidence.

Current status: Local proof of concept using Python, Ollama and Streamlit.
Next stage: Map the architecture to AWS services for production deployment.

⸻

Why I Built This

AI agents can produce convincing explanations even when the available evidence does not support them.

In a production environment, this creates a significant reliability problem: an AI system should not confidently invent a database outage, infrastructure failure, or other root cause simply because it sounds plausible.

This project explores how an AI incident-response system can be designed to:

* Detect production incidents
* Collect relevant operational evidence
* Investigate incidents using an LLM
* Ground AI responses in available evidence
* Evaluate AI outputs automatically
* Detect unsupported claims
* Apply safety and governance checks
* Keep potentially dangerous production actions behind human approval
* Replay incidents for repeatable testing

⸻

Architecture

                 Production Logs
                       │
                       ▼
                ┌──────────────┐
                │ Observability│
                │    Metrics   │
                └──────┬───────┘
                       │
                       ▼
                ┌──────────────┐
                │   Incident   │
                │   Detection  │
                └──────┬───────┘
                       │
                       ▼
                ┌──────────────┐
                │  AI Agent    │
                │ Investigation│
                └──────┬───────┘
                       │
                       ▼
                ┌──────────────┐
                │   LLM /      │
                │    Ollama    │
                └──────┬───────┘
                       │
                       ▼
                ┌──────────────┐
                │ AI Evaluation│
                │ & Regression │
                └──────┬───────┘
                       │
                       ▼
                ┌──────────────┐
                │ Governance & │
                │ Safety Checks│
                └──────┬───────┘
                       │
                       ▼
                 Human Review

⸻

Key Components

1. Observability

The observability/ package calculates operational metrics from production-style logs.

It monitors:

* Error rate
* Request latency
* Tool performance
* Recent errors
* Period-over-period changes

This provides the evidence used by the incident detection and AI investigation layers.

⸻

2. Incident Detection

The system automatically identifies incidents based on defined thresholds.

Currently simulated incidents include:

* HIGH_ERROR_RATE
* HIGH_LATENCY
* TOOL_FAILURE

Example:

Severity: HIGH
Type: HIGH_LATENCY
Message: Average latency is 2866.19ms

⸻

3. AI Incident Investigation

The AI agent receives the detected incident together with operational evidence.

The investigation process is:

Incident
   ↓
Collect metrics
   ↓
Collect tool metrics
   ↓
Collect recent errors
   ↓
Compare periods
   ↓
Build evidence-grounded prompt
   ↓
LLM investigation

The prompt instructs the model to:

* Use only available evidence
* Avoid inventing infrastructure problems
* Distinguish observed evidence from hypotheses
* State when a root cause cannot be confirmed
* Reflect uncertainty through confidence

This is designed to reduce unsupported AI conclusions.

⸻

4. AI Evaluation

The evaluation/ package evaluates generated incident reports.

Each investigation can be evaluated against:

Cause Match

Does the investigation identify the expected evidence-supported cause?

Evidence Score

Does the report contain the evidence required for the incident?

Grounding Score

Does the report avoid unsupported claims?

Overall Score

The evaluation combines these signals into an overall score.

Example:

Incident: HIGH_ERROR_RATE
Evidence score:   0.67
Grounding score:  0.00
Overall score:    0.22
Unsupported claims:
- infrastructure failure

The important behaviour is that the evaluation system can fail an AI investigation when it makes an unsupported claim, rather than assuming every generated response is correct.

⸻

5. Regression Testing

The project includes regression tests for AI behaviour.

The goal is to ensure that changes to the AI agent do not silently introduce unsafe or poorly grounded responses.

Example test scenarios include:

* Evidence-supported investigation → should pass
* Unsupported infrastructure claim → should fail
* Unsupported database/network claim → should fail

This makes the AI behaviour testable rather than relying solely on manual inspection.

⸻

6. Governance and Safety

The governance/ package provides basic controls around AI-generated recommendations.

Actions are separated into permitted and restricted categories.

Examples of restricted actions include:

delete
shutdown
modify_production
restart_service

These actions require human approval rather than allowing the AI agent to execute potentially destructive production changes autonomously.

The project also includes:

* Safety checks
* PII detection
* Action policy checks

⸻

7. Incident Replay

Incidents can be replayed using:

python3 -m simulator.replay_incident

The simulator:

1. Loads production-style logs
2. Detects incidents
3. Sends incidents to the AI investigator
4. Generates an investigation
5. Runs governance checks
6. Saves the investigation report

Reports are stored under:

incidents/reports/

This makes the system reproducible and provides data for evaluation and regression testing.

⸻

Project Structure

production-ai-evaluation/
│
├── ai_agent/
│   ├── agent.py
│   ├── prompts.py
│   └── tools.py
│
├── dashboard/
│   └── app.py
│
├── evaluation/
│   ├── dataset.json
│   ├── evaluator.py
│   └── regression_tests.py
│
├── governance/
│   ├── pii_detection.py
│   ├── policy.py
│   └── saftey_checks.py
│
├── incidents/
│   └── production_logs.json
│
├── observability/
│   ├── __init__.py
│   ├── alerts.py
│   ├── logger.py
│   └── metrics.py
│
├── simulator/
│   ├── generate_logs.py
│   └── replay_incident.py
│
├── Dockerfile
├── README.md
└── requirements.txt

⸻

Running the Project

1. Create the virtual environment

python3 -m venv .venv

Activate it:

source .venv/bin/activate

2. Install dependencies

pip install -r requirements.txt

3. Start Ollama

Make sure Ollama is running locally and that the required model is available.

The current agent uses:

llama3.2

4. Replay an incident

From the project root:

python3 -m simulator.replay_incident

5. Run evaluation

python3 evaluation/evaluator.py

6. Run regression tests

python3 evaluation/regression_tests.py

7. Run the dashboard

streamlit run dashboard/app.py

⸻

Example Incident Flow

A simulated production environment detects:

Error rate: 19.6%

The incident detector creates:

HIGH_ERROR_RATE

The AI agent then receives operational evidence including:

* Overall metrics
* Tool-level metrics
* Recent errors
* Historical comparison

The LLM investigates the incident.

The resulting investigation is then evaluated for:

Evidence
Grounding
Root-cause reasoning
Unsupported claims

The report is saved for later inspection and regression testing.

⸻

Production AWS Direction

The current implementation is deliberately local so that the underlying production-AI concepts can be tested before introducing cloud infrastructure.

A potential AWS implementation would map the architecture approximately as follows:

Local Component             AWS Direction
------------------------------------------------
Production logs          →  Amazon S3
Event/incident triggers  →  EventBridge
Processing               →  AWS Lambda / ECS
Observability            →  CloudWatch
AI model                 →  Amazon Bedrock
Agent orchestration      →  Bedrock Agents / application layer
Evaluation               →  Automated evaluation pipeline
Governance               →  IAM + application guardrails
Human approval           →  Approval workflow
Dashboard                →  Streamlit / AWS-hosted application

The exact production architecture would depend on requirements such as:

* Expected incident volume
* Latency requirements
* Model selection
* Security requirements
* Data sensitivity
* Cost constraints
* Required availability
* Human approval requirements

⸻

Engineering Principles

The project is built around several principles:

Evidence before explanation

The AI should investigate the evidence rather than inventing a plausible story.

Uncertainty is acceptable

If the available data does not establish the root cause, the system should explicitly say so.

AI output should be evaluated

A successful LLM call does not mean a successful investigation.

Production actions require controls

The AI should not automatically perform destructive production actions.

Incidents should be reproducible

Incident replay allows AI behaviour to be tested repeatedly.

Observability should extend to the AI system

The system should monitor not only the application but also the quality and safety of the AI’s decisions.

⸻

Future Improvements

Potential next steps include:

* Deploying the architecture to AWS
* Replacing local Ollama inference with a managed model endpoint
* Adding CloudWatch-based monitoring
* Event-driven incident detection
* Persistent evaluation history
* Automated model regression testing
* Improved PII redaction
* Human approval workflows
* Authentication and role-based access control
* Model latency and cost monitoring
* Production-scale agent observability

⸻

What I Learned

This project was built to explore the engineering challenges involved in moving AI systems beyond simple demonstrations.

The main areas explored were:

* Python application architecture
* Production observability
* Incident detection
* LLM-based investigation
* Evidence-grounded prompting
* AI evaluation
* Regression testing
* AI safety and governance
* Human-in-the-loop design
* Cloud architecture

The next stage is applying these concepts to AWS and developing the system towards a production deployment.
