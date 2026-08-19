### Updated Program ####

"""
Sequential Workflow with MAF and Microsoft Foundry

This script demonstrates a simple sequential workflow:
1. Researcher Agent gathers information on a topic.
2. Writer Agent writes an essay based on the research.

FIXED: migrated from the old `agent_framework.azure.AzureAIClient` (removed as of
Agent Framework 1.2.0) to the current `agent_framework.foundry.FoundryChatClient`.
See: https://learn.microsoft.com/en-us/agent-framework/agents/providers/microsoft-foundry

To run:
    pip install --upgrade agent-framework-foundry azure-identity python-dotenv
    python sequential_workflow.py
"""

import os
import asyncio
import logging
import random
from dotenv import load_dotenv
from agent_framework import (
    Agent,
    Executor,
    WorkflowBuilder,
    WorkflowContext,
    handler,
    WorkflowViz,
)
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential   # NOTE: sync client now, not azure.identity.aio
from agent_framework.devui import serve

# Load deployment configuration from .env instead of hard-coding environment-
# specific values in the script.
load_dotenv()
project_endpoint = (
    os.getenv("FOUNDRY_PROJECT_ENDPOINT")
    or os.getenv("AI_FOUNDRY_PROJECT_ENDPOINT")
)
model = (
    os.getenv("FOUNDRY_MODEL")
    or os.getenv("AI_FOUNDRY_DEPLOYMENT_NAME")
    or os.getenv("MODEL_DEPLOYMENT_NAME")
)
azure_tenant_id = os.getenv("AZURE_TENANT_ID")

print("Project Endpoint:", project_endpoint)
print("Model:", model)

if not project_endpoint or not model:
    missing = []
    if not project_endpoint:
        missing.append("FOUNDRY_PROJECT_ENDPOINT or AI_FOUNDRY_PROJECT_ENDPOINT")
    if not model:
        missing.append("FOUNDRY_MODEL or AI_FOUNDRY_DEPLOYMENT_NAME or MODEL_DEPLOYMENT_NAME")
    raise ValueError("Missing required .env value(s): " + ", ".join(missing))

# One shared credential + chat client is enough — FoundryChatClient manages
# per-agent sessions internally, so we no longer need to manually create an
# AIProjectClient / OpenAI client / conversation per agent (that whole dance
# was AzureAIClient-specific plumbing that FoundryChatClient does for you).
credential = AzureCliCredential(tenant_id=azure_tenant_id) if azure_tenant_id else AzureCliCredential()
chat_client = FoundryChatClient(
    project_endpoint=project_endpoint,
    model=model,
    credential=credential,
)


async def run_agent_with_retry(agent: Agent, message, *, max_tokens: int = 800):
    """Run an agent and wait/retry when Azure returns a transient rate limit."""
    max_attempts = int(os.getenv("AGENT_RETRY_ATTEMPTS", "5"))
    if max_attempts < 1:
        raise ValueError("AGENT_RETRY_ATTEMPTS must be >= 1")

    for attempt in range(max_attempts):
        try:
            return await agent.run(message, max_tokens=max_tokens)
        except Exception as exc:
            error_text = str(exc).lower()
            is_rate_limit = (
                "429" in error_text
                or "too many requests" in error_text
                or "rate_limit" in error_text
                or "rate limit" in error_text
            )
            if not is_rate_limit or attempt == max_attempts - 1:
                raise

            delay = min(30, (2 ** attempt) + random.uniform(0.25, 1.25))
            print(f"Rate limit hit. Retrying in {delay:.1f}s...")
            await asyncio.sleep(delay)


def create_agent(agent_name: str, agent_instructions: str) -> Agent:
    """Create one Foundry agent bound to the shared FoundryChatClient.

    This is now synchronous and needs no manual conversation/session setup —
    FoundryChatClient + Agent handle that internally.
    """
    agent = Agent(
        client=chat_client,
        name=agent_name,
        instructions=agent_instructions,
    )
    print(f"{agent_name} Agent created successfully!")
    return agent


# Executors are workflow nodes. Their handlers transform an incoming message
# into the message consumed by the next stage.
class ResearcherExecutor(Executor):
    def __init__(self, agent, **kwargs):
        super().__init__(**kwargs)
        self.agent = agent

    @handler
    async def handle(self, query: str, ctx: WorkflowContext[str]) -> None:
        response = await run_agent_with_retry(self.agent, query, max_tokens=700)
        # send_message passes an intermediate result to the next executor.
        await ctx.send_message(str(response))


class WriterExecutor(Executor):
    def __init__(self, agent, **kwargs):
        super().__init__(**kwargs)
        self.agent = agent

    @handler
    async def handle(self, research_data: str, ctx: WorkflowContext[str]) -> None:
        response = await run_agent_with_retry(self.agent, research_data, max_tokens=900)
        # yield_output publishes the final workflow result to DevUI.
        await ctx.yield_output(str(response))


def build_workflow():
    """Create the agents and connect them in a researcher-to-writer pipeline.

    NOTE: this no longer needs to be async — agent creation is now a plain
    synchronous call — but it's kept callable the same way so main() below
    doesn't need to change shape.
    """
    # Each instruction prompt gives an agent one clear responsibility.
    researcher_agent = create_agent(
        agent_name="Researcher-Agent",
        agent_instructions=(
            "You are a knowledgeable researcher. Gather useful facts and insights on the topic. "
            "Keep the research summary concise, practical, and under 300 words."
        )
    )
    writer_agent = create_agent(
        agent_name="Writer-Agent",
        agent_instructions=(
            "You are a clear writer. Turn the research into a coherent short essay. "
            "Keep the final essay focused and under 500 words."
        )
    )

    # Executor IDs make workflow traces and diagrams easier to read.
    researcher_executor = ResearcherExecutor(researcher_agent, id="ResearcherExecutor")
    writer_executor = WriterExecutor(writer_agent, id="WriterExecutor")

    # A single directed edge creates strict sequential execution:
    # the writer starts only after the researcher sends its result.
    # NOTE: as of the current agent_framework, start_executor is a required
    # constructor argument — the old .set_start_executor(...) fluent method
    # has been removed in favor of this.
    workflow = (
        WorkflowBuilder(
            name="Sequential Research & Writing Workflow",
            description="A two-step workflow: research a topic, then write an essay.",
            start_executor=researcher_executor,
        )
        .add_edge(researcher_executor, writer_executor)
        .build()
    )

    # Mermaid text is a portable representation of the workflow graph.
    viz = WorkflowViz(workflow)
    mermaid_content = viz.to_mermaid()
    print("Mermaid Diagram:\n", mermaid_content)

    return workflow


def _call_serve_compatibly(**desired_kwargs):
    """Call agent_framework.devui.serve() with only the kwargs it currently
    supports, dropping any it doesn't recognize (instead of crashing).

    agent_framework_devui is still preview-grade and its serve() signature
    has been changing release to release — this keeps the script working
    across those changes without needing a patch every time one kwarg shifts.
    """
    import inspect

    supported = set(inspect.signature(serve).parameters)
    accepted = {k: v for k, v in desired_kwargs.items() if k in supported}
    dropped = set(desired_kwargs) - set(accepted)
    if dropped:
        print(f"Note: serve() in your installed agent_framework_devui doesn't "
              f"support these kwargs — skipping them: {sorted(dropped)}")
    return serve(**accepted)


def main():
    """Launch the sequential workflow in DevUI."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logger = logging.getLogger(__name__)
    devui_port = int(os.getenv("DEVUI_SEQUENTIAL_PORT") or os.getenv("DEVUI_PORT", "8090"))
    logger.info("Starting Sequential Research & Writing Workflow")
    logger.info("Available at: http://localhost:%s", devui_port)
    logger.info("Entity ID: workflow_sequential_research_writer")

    # No asyncio.run() needed here anymore for setup — build_workflow() is
    # synchronous now (see NOTE above) — which also sidesteps the old
    # event-loop-mismatch risk between an asyncio.run() setup phase and
    # DevUI's own internal loop.
    workflow = build_workflow()
    # DevUI exposes the workflow in a browser; tracing makes each stage
    # observable for debugging and learning (when supported — see above).
    _call_serve_compatibly(entities=[workflow], port=devui_port, auto_open=True, tracing_enabled=True)


if __name__ == "__main__":
    # Prevent server startup when this module is imported elsewhere.
    main()


#######User Prompts - Sample Examples:
# (1) Write a short essay on how artificial intelligence is changing education.
# (2) Write an essay about how cloud computing helps modern companies scale faster.
# (3) Research the impact of electric vehicles on urban transportation and write a clear essay.
# (4) Explain the importance of cybersecurity for small businesses in a short essay.
