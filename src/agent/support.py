from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent

from src.prompt import SUPPORT_AGENT_PROMPT
from src.tools import TOOLS


def build_support_agent(model: str | BaseChatModel, checkpointer: BaseCheckpointSaver | None = None):
    """Cria uma instância do agente."""
    return create_agent(
        model=model,
        name="emporio_da_musica_support",
        system_prompt=SUPPORT_AGENT_PROMPT,
        tools=TOOLS,
        checkpointer=checkpointer if checkpointer is not None else InMemorySaver(),
    )