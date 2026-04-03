from typing import TypedDict, Annotated
from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    position: str | None
    analysis: dict | None
    theory: str | None
    recommendations: list[str] | None
