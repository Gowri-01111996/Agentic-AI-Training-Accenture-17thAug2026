# Demo-1 — Agent Architecture Patterns with Microsoft Foundry

![Microsoft Foundry](https://img.shields.io/badge/Microsoft%20Foundry-Agentic%20AI-blue)
![Python](https://img.shields.io/badge/Python-3.11+-yellow)
![Azure](https://img.shields.io/badge/Azure-AI%20Foundry-0078D4)
![Agentic AI](https://img.shields.io/badge/AI-Agentic%20AI-purple)

## 📌 Overview

This demo demonstrates **core Agentic AI architecture patterns** using **Microsoft Foundry / Azure AI Foundry**, Azure AI Projects SDK, and an OpenAI-compatible model client.

The objective is to understand how different agent architectures can be designed and implemented for enterprise AI applications, ranging from a simple single-agent tool loop to hierarchical multi-agent orchestration.

The implementation includes four major agent architecture patterns:

1. **ReAct — Reason + Act**
2. **Planner–Executor**
3. **Supervisor / Router**
4. **Hierarchical Multi-Agent Architecture**

These patterns provide a foundation for designing scalable, tool-enabled, and multi-agent enterprise AI solutions.

---

# 🎯 Learning Objectives

After completing this demo, learners will understand how to:

* Build an agent using Microsoft Foundry
* Connect an application to a deployed AI model
* Use Azure Identity / Entra ID authentication
* Implement tool/function calling
* Build a ReAct agent loop
* Separate planning and execution
* Implement supervisor-based agent routing
* Design hierarchical multi-agent systems
* Delegate tasks between specialized agents
* Combine multiple agents into an enterprise workflow
* Configure environment variables securely
* Run Agentic AI applications locally

---

# 🏗️ Architecture Patterns Covered

## 1. ReAct — Reason + Act

The **ReAct pattern** combines reasoning and action through an iterative tool-calling loop.

### Flow

```text
User Request
     ↓
Agent
     ↓
Reason
     ↓
Select Tool
     ↓
Execute Tool
     ↓
Observe Result
     ↓
Reason Again
     ↓
Final Response
```

### Example

```text
User:
What's the weather in Bengaluru?

Agent:
Identify that weather information is required
        ↓
Call get_weather()
        ↓
Receive weather result
        ↓
Return final response
```

### Key Concepts

* Tool calling
* Function calling
* Agent reasoning loop
* Tool execution
* Observation
* Iterative execution
* Maximum execution steps

---

# 2. Planner–Executor Pattern

The Planner–Executor architecture separates **planning** from **execution**.

### Flow

```text
                User Goal
                   ↓
                Planner
                   ↓
          Break into Tasks
                   ↓
        ┌──────────┼──────────┐
        ↓          ↓          ↓
      Task 1     Task 2     Task 3
        ↓          ↓          ↓
     Executor   Executor   Executor
        └──────────┼──────────┘
                   ↓
              Synthesizer
                   ↓
              Final Result
```

### Example

```text
Goal:
Create a customer onboarding process

Planner
   ↓
1. Collect customer information
2. Validate customer details
3. Create customer account
4. Send welcome notification

Executor
   ↓
Execute each task independently

Synthesizer
   ↓
Generate final result
```

### Key Concepts

* Goal decomposition
* Task planning
* Atomic tasks
* Sequential execution
* Result aggregation
* Final synthesis

---

# 3. Supervisor / Router Pattern

The Supervisor pattern uses a central agent to determine which specialist agent should handle a request.

### Architecture

```text
                  User
                   ↓
              Supervisor
                   ↓
        ┌──────────┼──────────┐
        ↓          ↓          ↓
     Billing    Technical   General
      Agent       Agent      Agent
        ↓          ↓          ↓
        └──────────┼──────────┘
                   ↓
             Final Response
```

### Specialist Agents

This demo includes:

* Billing Specialist
* Technical Support Specialist
* General Support Agent

### Example

```text
User:
My invoice was charged twice.

Supervisor
      ↓
Classifies request
      ↓
Billing Specialist
      ↓
Generates response
```

### Key Concepts

* Agent routing
* Classification
* Specialist agents
* Delegation
* Domain-specific prompts
* Central orchestration

---

# 4. Hierarchical Multi-Agent Architecture

The hierarchical pattern introduces multiple levels of management and delegation.

### Architecture

```text
                    Manager
                       ↓
              ┌────────┴────────┐
              ↓                 ↓
        Research Lead      Writing Lead
              ↓                 ↓
         Researchers          Writers
              ↓                 ↓
              └────────┬────────┘
                       ↓
                   Manager
                       ↓
                 Final Output
```

### Example

For a research and writing task:

```text
Manager
   ↓
Research Team
   ↓
Research Workers
   ↓
Research Team Lead
   ↓
Writing Team
   ↓
Writing Workers
   ↓
Writing Team Lead
   ↓
Manager
   ↓
Final Response
```

### Key Concepts

* Multi-level delegation
* Team-based agents
* Supervisor agents
* Worker agents
* Hierarchical orchestration
* Result consolidation
* Enterprise multi-agent architecture

---

# 📂 Repository Contents

```text
Demo-1/
│
├── .env
│
├── 01_langgraph_mcp_a2a_lab.ipynb
│
├── A1_agent_architecture_patterns.py
│
├── mini-Project1.ipynb
│
├── requirements.txt
│
└── README.md
```

## File Description

| File                                | Description                                                    |
| ----------------------------------- | -------------------------------------------------------------- |
| `A1_agent_architecture_patterns.py` | Python implementation of four Agentic AI architecture patterns |
| `01_langgraph_mcp_a2a_lab.ipynb`    | Hands-on notebook covering LangGraph, MCP and A2A concepts     |
| `mini-Project1.ipynb`               | Mini project / practical implementation                        |
| `requirements.txt`                  | Python dependencies required for the demo                      |
| `.env`                              | Environment configuration and credentials                      |
| `README.md`                         | Demo documentation                                             |

---

# 🛠️ Technology Stack

## Microsoft Cloud

* Microsoft Azure
* Microsoft Foundry / Azure AI Foundry
* Azure AI Projects
* Microsoft Entra ID

## AI / LLM

* Large Language Models
* OpenAI-compatible model interface
* Function Calling
* Tool Calling
* Agentic AI
* Multi-Agent Systems

## Frameworks & SDKs

* Python
* Azure AI Projects SDK
* Azure Identity
* python-dotenv
* LangGraph
* MCP
* A2A concepts

---

# ⚙️ Prerequisites

Before running the demo, ensure the following are available:

* Python **3.11 or later**
* Azure subscription
* Microsoft Foundry project
* Deployed AI model
* Appropriate Azure permissions
* Microsoft Entra ID authentication
* Git
* VS Code / Jupyter Notebook

---

# 📦 Installation

## Step 1 — Clone the Repository

```bash
git clone https://github.com/avyuktitech/Agentic-AI-Training-Accenture-17thAug2026.git
```

Navigate to the Demo-1 directory:

```bash
cd Agentic-AI-Training-Accenture-17thAug2026/Demo-1
```

---

## Step 2 — Create a Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Configuration

Create a `.env` file in the `Demo-1` directory.

Example:

```env
PROJECT_ENDPOINT=https://<account>.services.ai.azure.com/api/projects/<project>
MODEL_DEPLOYMENT=<your-model-deployment>

# Optional Azure OpenAI API-key based configuration
AZURE_OPENAI_API_KEY=<your-api-key>
AZURE_OPENAI_ENDPOINT=<your-openai-endpoint>
```

### Important Security Notice

**Never commit real API keys, passwords, tokens, or secrets to GitHub.**

Add `.env` to `.gitignore`:

```gitignore
.env
.venv/
__pycache__/
*.pyc
```

---

# 🔑 Authentication

The Python implementation supports two approaches.

## Option 1 — Microsoft Entra ID / DefaultAzureCredential

The application can authenticate through Azure identity mechanisms using:

```python
DefaultAzureCredential()
```

This is recommended for enterprise environments.

## Option 2 — Azure OpenAI API Key

An Azure OpenAI API key can be supplied through environment variables when required.

The application selects the appropriate connection based on the configured environment variables.

---

# ▶️ Running the Demo

Execute:

```bash
python A1_agent_architecture_patterns.py
```

The application demonstrates:

```text
--- ReAct ---
--- Planner-Executor ---
--- Supervisor ---
--- Hierarchical ---
```

---

# 🧪 Demo Scenarios

## Scenario 1 — ReAct

```text
What's the weather in Bengaluru?
```

Demonstrates:

* Agent reasoning
* Tool selection
* Function calling
* Tool execution
* Final response generation

---

## Scenario 2 — Planner–Executor

```text
Plan a 3-step customer onboarding checklist.
```

Demonstrates:

* Goal decomposition
* Planning
* Task execution
* Result aggregation

---

## Scenario 3 — Supervisor

```text
My invoice was charged twice this month.
```

Demonstrates:

* Request classification
* Agent routing
* Specialist selection
* Domain-specific response generation

---

## Scenario 4 — Hierarchical Agent

```text
Write a one-paragraph brief on agentic AI adoption in banking.
```

Demonstrates:

* Manager agent
* Research team
* Research workers
* Writing team
* Writing workers
* Multi-level delegation
* Final response refinement

---

# 🧠 Architecture Comparison

| Pattern          | Architecture              | Best Use Case                  |
| ---------------- | ------------------------- | ------------------------------ |
| ReAct            | Single Agent + Tools      | Tool-enabled tasks             |
| Planner–Executor | Planner + Workers         | Complex workflows              |
| Supervisor       | Router + Specialists      | Domain-based routing           |
| Hierarchical     | Manager + Teams + Workers | Enterprise multi-agent systems |

---

# 🏢 Enterprise Use Cases

These architecture patterns can be applied to real-world enterprise scenarios.

### IT Service Management

```text
User
 ↓
IT Supervisor
 ↓
Network / Database / Application / Security Agents
```

### HR Automation

```text
Employee
 ↓
HR Supervisor
 ↓
Payroll / Benefits / Leave / Recruitment Agents
```

### Banking

```text
Customer
 ↓
Banking Supervisor
 ↓
Accounts / Loans / Fraud / Payments Agents
```

### Healthcare

```text
Patient Request
 ↓
Healthcare Supervisor
 ↓
Appointments / Insurance / Billing / Clinical Information Agents
```

### Customer Support

```text
Customer
 ↓
Support Supervisor
 ↓
Billing / Technical / Product / Escalation Agents
```

---

# 🔬 Mini Project

## Enterprise Customer Support Multi-Agent System

Build a multi-agent customer support solution using the architecture patterns demonstrated in this lab.

### Requirements

The system should:

1. Receive a customer request
2. Classify the request
3. Route it to the appropriate specialist
4. Use tools where required
5. Execute the task
6. Validate the result
7. Generate a final response
8. Log the interaction

### Suggested Agents

```text
Customer Support Manager
        ↓
 ┌──────┼────────┐
 ↓      ↓        ↓
Billing Technical Product
Agent     Agent    Agent
```

---

# 🎓 Learning Outcomes

After completing Demo-1, learners should be able to:

* Explain major Agentic AI architecture patterns
* Build tool-enabled agents
* Implement function calling
* Design planner/executor workflows
* Implement supervisor-based routing
* Design hierarchical multi-agent systems
* Identify appropriate architecture patterns for enterprise use cases
* Integrate agents with Microsoft Foundry
* Secure model credentials and configuration
* Extend the architecture with MCP, A2A and LangGraph

---

# 🚀 Next Steps

Recommended progression after this demo:

```text
Agent Architecture Patterns
          ↓
LangGraph
          ↓
MCP
          ↓
A2A
          ↓
RAG
          ↓
Tool Calling
          ↓
Multi-Agent Systems
          ↓
Agent Evaluation
          ↓
Enterprise Agentic AI
          ↓
Production Deployment
```

---

# 📚 Related Topics

This repository is part of an Agentic AI training program covering:

* Generative AI
* LLMs
* Prompt Engineering
* Agentic AI
* AI Agents
* Multi-Agent Systems
* Microsoft Foundry
* Azure OpenAI
* LangGraph
* MCP
* A2A
* RAG
* Tool Calling
* Agent Evaluation
* Enterprise AI Architecture

---

# ⚠️ Security & Responsible AI

This repository is intended for **educational and demonstration purposes**.

Do not store the following information in the repository:

* API keys
* Passwords
* Access tokens
* Client secrets
* Connection strings
* Production credentials
* Personally identifiable information (PII)

Always follow your organization's security, privacy, Responsible AI, and cloud governance policies.

---

# 👨‍💻 Author

**Avyukti Tech**

GitHub: https://github.com/avyuktitech

---

# 📄 License

This repository is intended for **training, educational, demonstration, and learning purposes**.

Please review the applicable licenses and terms for Microsoft Azure, Microsoft Foundry, Azure AI SDKs, OpenAI-compatible services, and other third-party technologies used in this repository.

---

## ⭐ Training Repository

If you find this repository useful for learning **Agentic AI, Microsoft Foundry, Multi-Agent Architecture, LangGraph, MCP and A2A**, consider starring the repository and exploring the other demos.

**Think • Learn • Build • Innovate with Agentic AI 🚀**
