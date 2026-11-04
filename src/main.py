import os
import sys
from uuid import uuid4

from dotenv import load_dotenv
from langchain_core.messages import AIMessageChunk
from langchain_openai import ChatOpenAI

from src.agent import build_support_agent

load_dotenv(override=True)


def _text_from_chunk(chunk: AIMessageChunk) -> str:
    """Retorna apenas texto visível, ignorando chamadas de tools e outros blocos."""

    if isinstance(chunk.content, str):
        return chunk.content
    return "".join(
        block["text"]
        for block in chunk.content
        if isinstance(block, dict)
        and block.get("type") == "text"
        and isinstance(block.get("text"), str)
    )

def _send_message(agent, message: str, thread_id: str) -> None:
    print("Agente: ", end="", flush=True)
    human_msg = {"messages": [{"role": "user", "content": message}]}
    config = {"configurable": {"thread_id": thread_id}}
    for chunk, metadata in agent.stream(human_msg, config, stream_mode="messages"):
        if not isinstance(chunk, AIMessageChunk) or metadata.get("langgraph_node") != "model":
            continue
        text = _text_from_chunk(chunk)
        if text:
            print(text, end="", flush=True)
    print()


def main() -> int:
    model = ChatOpenAI(model=os.getenv("MODEL", "gpt-6-luna"))
    agent = build_support_agent(model)
    thread_id = uuid4().hex

    if sys.argv[1:]:
        _send_message(agent, " ".join(sys.argv[1:]), thread_id)
        return 0

    print("Assistente do Empório da Música — digite 'exit' para sair.")
    while True:
        try:
            message = input("Você: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0

        if message.casefold() == "exit":
            return 0
        if message:
            _send_message(agent, message, thread_id)


if __name__ == "__main__":
    raise SystemExit(main())