"""Weather Agent with Generative UI support.

Demonstrates how to create UI components from LangGraph nodes.
"""

import uuid
from typing import Annotated, Sequence, TypedDict

from langchain_core.messages import AIMessage, BaseMessage
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
try:
    from langgraph.graph.ui import AnyUIMessage, push_ui_message, ui_message_reducer
except ImportError:
    # Fallback for older versions
    AnyUIMessage = Any
    def push_ui_message(component_name: str, props: dict, message=None):
        """Fallback implementation for push_ui_message"""
        return {"id": str(uuid.uuid4()), "name": component_name, "props": props}
    def ui_message_reducer(messages, new_message):
        """Fallback implementation for ui_message_reducer"""
        return messages + [new_message] if new_message else messages


class WeatherOutput(TypedDict):
    """Weather output with city information."""

    city: str


class AgentState(TypedDict):
    """Agent state with messages and UI components."""

    messages: Annotated[Sequence[BaseMessage], add_messages]
    ui: Annotated[Sequence[AnyUIMessage], ui_message_reducer]




async def weather_node(state: AgentState) -> dict[str, list[AIMessage]]:
    """Weather node that generates UI components."""
    # For this demo, we'll extract city from the last user message
    # In a real implementation, you'd use structured output with ChatOpenAI
    last_message = state["messages"][-1] if state["messages"] else None
    user_input = last_message.content if last_message else ""

    # Ensure user_input is a string for processing
    if isinstance(user_input, list):
        user_input = " ".join(str(item) for item in user_input)
    user_input = str(user_input)

    # Simple city extraction (in real implementation, use structured output)
    city = "北京"  # Default city
    if "上海" in user_input:
        city = "上海"
    elif "深圳" in user_input:
        city = "深圳"
    elif "广州" in user_input:
        city = "广州"
    elif "杭州" in user_input:
        city = "杭州"

    weather_data: WeatherOutput = {"city": city}

    message = AIMessage(
        id=str(uuid.uuid4()), content=f"这是{weather_data['city']}的天气信息"
    )

    # Emit UI elements associated with the message
    push_ui_message("weather", dict(weather_data), message=message)

    return {"messages": [message]}


# Define the graph
graph = (
    StateGraph(AgentState)
    .add_node("weather", weather_node)
    .add_edge("__start__", "weather")
    .compile()
)
