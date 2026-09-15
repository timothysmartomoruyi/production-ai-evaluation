Production AI Incident Response Platform

An experimental AI incident investigation platform exploring observability, evidence-grounded AI, evaluation, and governance.

The project simulates a production environment where application and tool-level failures are detected, investigated by an LLM, and evaluated to determine whether the resulting investigation is supported by available evidence.

Project status: Learning-focused proof of concept.
Current implementation: Python, Ollama and Streamlit.
Future direction: Explore how the architecture could be implemented using AWS services.

⸻

Why I Built This

I wanted to learn more about the engineering challenges involved in taking AI systems beyond simple demonstrations and towards more reliable production systems.

The project explores how an AI incident-response system could:

* Detect production incidents
* Collect operational evidence
* Investigate incidents using an LLM
* Ground investigations in available evidence
* Evaluate AI-generated responses
* Detect unsupported claims
* Apply basic safety and governance controls
* Keep potentially destructive production actions behind human approval
* Replay incidents for repeatable testing

⸻

Architecture

Production Logs
      │
      ▼
 Observability
      │
      ▼
Incident Detection
      │
      ▼
 AI Investigation
      │
      ▼
    LLM
      │
      ▼
AI Evaluation
      │
      ▼
Governance / Safety
      │
      ▼
 Human Review

⸻

Key Components

Observability

The observability/ package calculates operational metrics from simulated production logs.

It currently covers:

* Error rate
* Request latency
* Tool performance
* Recent errors
* Period comparisons

These metrics provide evidence for the incident detection and investigation layers.

Incident Detection

The system detects simulated incidents including:

* HIGH_ERROR_RATE
* HIGH_LATENCY
* TOOL_FAILURE

AI Investigation

The AI agent gathers available operational evidence and provides it to an LLM for investigation.

The prompt is designed to encourage the model to:

* Use available evidence
* Avoid inventing unsupported causes
* Distinguish evidence from hypotheses
* Acknowledge uncertainty
* Avoid claiming a root cause when the evidence is insufficient

AI Evaluation

The evaluation/ package evaluates generated investigations using:

* Cause matching
* Required evidence
* Grounding checks
* Overall scoring

The evaluator can identify unsupported claims.

For example, during testing, an investigation was detected making the unsupported claim:

infrastructure failure

The evaluation system therefore marked the investigation as failing its grounding check.

Governance

The project includes basic:

* Action policy checks
* Safety checks
* PII detection

Potentially destructive actions are intended to require human approval rather than being automatically executed by the AI.

⸻

Running the Project

Create and activate a virtual environment:

python3 -m venv .venv
source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Run the incident replay:

python3 -m simulator.replay_incident

Run the evaluation:

python3 evaluation/evaluator.py

Run regression tests:

python3 evaluation/regression_tests.py

Run the dashboard:

streamlit run dashboard/app.py

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

AI Assistance & Learning

This project was developed as a learning exercise with substantial AI assistance.

I was new to several of the technologies and concepts used in the project, particularly AWS, production AI architecture, and some of the Python implementation.

During the initial development, I used AI assistants extensively to:

* Generate implementation ideas
* Explain architecture
* Generate and modify Python code
* Debug errors
* Create project files
* Suggest evaluation and governance approaches
* Structure the project

A significant portion of the initial code was generated through AI-assisted prompts and then copied into the project, rather than written independently from scratch.

As a result, this repository should not be interpreted as evidence that I independently wrote every component of the implementation.

The purpose of publishing it is instead to document my learning process and demonstrate the concepts I am currently exploring.

Current Learning Goal

The next stage of the project is to move from:

“I can use AI to help me build this.”

towards:

“I understand why each component exists and can reproduce the core functionality myself.”

I am therefore using the existing implementation as a learning reference and working through the Python, LLM, evaluation, governance and cloud concepts behind it.

⸻

AWS Direction

The current project runs locally and uses Ollama for LLM inference.

A potential future AWS architecture could replace local components with managed cloud services such as:

Local Prototype             Potential AWS Direction
---------------------------------------------------------
Production logs          →   Amazon S3
Event triggers           →   EventBridge
Application processing  →   Lambda / ECS
Observability           →   CloudWatch
LLM inference           →   Amazon Bedrock
Access control          →   IAM
Human approval          →   Approval workflow

These AWS components have not yet been implemented in this repository.

The AWS architecture is currently a learning and design direction rather than a completed deployment.

⸻

What I Am Learning

This project is helping me develop an understanding of:

* Python application structure
* Observability
* Incident detection
* LLM-based investigation
* Evidence-grounded prompting
* AI evaluation
* Regression testing
* AI governance
* Human-in-the-loop systems
* Cloud architecture
* Production AI reliability

The main lesson so far is that building an AI application is not only about getting an LLM to produce an answer.

A production system also needs to answer:

Can I trust the answer?

What evidence supports it?

What happens when the model is wrong?

Can I detect regressions?

What actions should the AI be allowed to take?

Those questions are the main focus of this project.
