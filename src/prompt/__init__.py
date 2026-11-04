from pathlib import Path

SUPPORT_AGENT_PROMPT = (Path(__file__).with_name("support_agent.md")).read_text(encoding="utf-8").strip()

__all__ = ["SUPPORT_AGENT_PROMPT"]