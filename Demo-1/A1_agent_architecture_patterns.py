"""
A1 — Agent Architecture Patterns on Microsoft Foundry (Azure AI Foundry)
=========================================================================
Demonstrates four core agent patterns using the `azure-ai-projects` (2.x)
SDK against a Foundry project + deployed model.

    pip install "azure-ai-projects>=2.3.0" azure-identity python-dotenv

Env vars required:
    PROJECT_ENDPOINT   = https://<account>.services.ai.azure.com/api/projects/<project>
    MODEL_DEPLOYMENT   = e.g. gpt-4o

Run:  python A1_agent_architecture_patterns.py
"""

import os
import json
import sys
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
sys.stdout.reconfigure(encoding="utf-8")

MODEL = os.environ.get("MODEL_DEPLOYMENT", "gpt-4o")

# Use an Azure OpenAI API key when supplied; otherwise retain the Entra ID-based
# Foundry project connection used in the original workshop.
api_key = os.environ.get("AZURE_OPENAI_API_KEY")
if api_key:
    azure_openai_endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    oai = OpenAI(api_key=api_key, base_url=azure_openai_endpoint)
else:
    project_endpoint = os.environ["PROJECT_ENDPOINT"]
    client = AIProjectClient(
        endpoint=project_endpoint, credential=DefaultAzureCredential()
    )
    oai = client.get_openai_client()  # OpenAI-compatible Foundry model client


# ---------------------------------------------------------------------------
# Pattern 1: ReAct (Reason + Act) — single agent, tool-loop
# ---------------------------------------------------------------------------
def get_weather(city: str) -> str:
    return f"{city}: 29°C, clear skies"


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string"}},
                "required": ["city"],
            },
        },
    }
]
TOOL_IMPL = {"get_weather": get_weather}


def run_react_agent(user_prompt: str, max_steps: int = 5) -> str:
    """Classic ReAct loop: model reasons, calls a tool, observes, repeats."""
    messages = [
        {"role": "system", "content": "Think step by step. Use tools when needed."},
        {"role": "user", "content": user_prompt},
    ]
    for step in range(max_steps):
        resp = oai.chat.completions.create(model=MODEL, messages=messages, tools=TOOLS)
        msg = resp.choices[0].message
        if not msg.tool_calls:
            return msg.content  # final answer reached
        messages.append(msg)
        for call in msg.tool_calls:
            args = json.loads(call.function.arguments)
            result = TOOL_IMPL[call.function.name](**args)
            messages.append(
                {"role": "tool", "tool_call_id": call.id, "content": str(result)}
            )
    return "Max ReAct steps exceeded."


# ---------------------------------------------------------------------------
# Pattern 2: Planner–Executor — separate planning and execution model calls
# ---------------------------------------------------------------------------
def run_planner_executor(goal: str) -> str:
    plan_resp = oai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Break the goal into a numbered list of atomic steps. Output JSON list of strings."},
            {"role": "user", "content": goal},
        ],
        response_format={"type": "json_object"},
    )
    plan = json.loads(plan_resp.choices[0].message.content).get("steps", [])

    results = []
    for step in plan:
        exec_resp = oai.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "Execute this single step and report the outcome concisely."},
                {"role": "user", "content": step},
            ],
        )
        results.append({"step": step, "result": exec_resp.choices[0].message.content})

    synth = oai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Summarize the completed plan and results for the user."},
            {"role": "user", "content": json.dumps(results)},
        ],
    )
    return synth.choices[0].message.content


# ---------------------------------------------------------------------------
# Pattern 3: Supervisor — a router agent delegates to specialist agents
# ---------------------------------------------------------------------------
SPECIALISTS = {
    "billing": "You are a billing support specialist. Answer only billing questions.",
    "technical": "You are a technical support specialist. Answer only technical issues.",
    "general": "You are a general customer support agent.",
}


def run_supervisor(user_prompt: str) -> str:
    route_resp = oai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": f"Classify the request into one of {list(SPECIALISTS)}. Reply with just the label."},
            {"role": "user", "content": user_prompt},
        ],
    )
    label = route_resp.choices[0].message.content.strip().lower()
    system_prompt = SPECIALISTS.get(label, SPECIALISTS["general"])

    final = oai.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
    )
    return f"[routed -> {label}] {final.choices[0].message.content}"


# ---------------------------------------------------------------------------
# Pattern 4: Hierarchical — supervisor over sub-supervisors over workers
#   Manager -> {Research team lead -> workers, Writing team lead -> workers}
# ---------------------------------------------------------------------------
def call(system: str, user: str) -> str:
    r = oai.chat.completions.create(
        model=MODEL, messages=[{"role": "system", "content": system}, {"role": "user", "content": user}]
    )
    return r.choices[0].message.content


def research_team(task: str) -> str:
    facts = call("You are a research worker. Return 3 concise bullet facts.", task)
    return call("You are the research team lead. Consolidate the bullets into one paragraph.", facts)


def writing_team(task: str) -> str:
    draft = call("You are a writing worker. Draft a short paragraph.", task)
    return call("You are the writing team lead. Edit for clarity and tone.", draft)


def run_hierarchical(goal: str) -> str:
    research = research_team(goal)
    draft = writing_team(f"Goal: {goal}\nResearch: {research}")
    return call("You are the top-level manager. Approve or refine the final output.", draft)


if __name__ == "__main__":
    print("--- ReAct ---")
    print(run_react_agent("What's the weather in Bengaluru? Reply in one sentence."))

    print("\n--- Planner-Executor ---")
    print(run_planner_executor("Plan a 3-step customer onboarding checklist."))

    print("\n--- Supervisor ---")
    print(run_supervisor("My invoice was charged twice this month."))

    print("\n--- Hierarchical ---")
    print(run_hierarchical("Write a one-paragraph brief on agentic AI adoption in banking."))
