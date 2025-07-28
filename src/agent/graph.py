"""Weather Agent with Generative UI support.

Demonstrates how to create UI components from LangGraph nodes.
"""

import random
import re
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
    """Weather output with complete weather information."""

    city: str
    temperature: str
    condition: str
    humidity: str
    windSpeed: str  # 统一使用windSpeed（与前端对齐）
    description: str


class AgentState(TypedDict):
    """Agent state with messages and UI components."""

    messages: Annotated[Sequence[BaseMessage], add_messages]
    ui: Annotated[Sequence[AnyUIMessage], ui_message_reducer]


# Predefined weather data for different cities
WEATHER_DATA = [
    {
        "city": "北京",
        "temperature": "22°C",
        "condition": "晴天",
        "humidity": "45%",
        "windSpeed": "3km/h",  # 统一使用windSpeed
        "description": "今天北京天气晴朗，温度适宜，适合外出活动。"
    },
    {
        "city": "上海",
        "temperature": "18°C",
        "condition": "多云",
        "humidity": "68%",
        "windSpeed": "5km/h",
        "description": "上海今天多云转阴，温度稍凉，建议增添衣物。"
    },
    {
        "city": "深圳",
        "temperature": "26°C",
        "condition": "小雨",
        "humidity": "78%",
        "windSpeed": "7km/h",
        "description": "深圳今天有小雨，湿度较高，出门记得带伞。"
    },
    {
        "city": "广州",
        "temperature": "24°C",
        "condition": "阴天",
        "humidity": "72%",
        "windSpeed": "4km/h",
        "description": "广州今天阴天，温度舒适，适合室内活动。"
    },
    {
        "city": "杭州",
        "temperature": "20°C",
        "condition": "晴天",
        "humidity": "55%",
        "windSpeed": "6km/h",
        "description": "杭州今天晴空万里，温度宜人，是游览的好天气。"
    }
]


def extract_city_from_message(message_content: str) -> str:
    """从用户消息中提取城市名称 - 优化版本"""
    # 动态获取支持的城市列表
    available_cities = {w["city"] for w in WEATHER_DATA}
    
    # 第一层: 直接匹配城市名称 - 按位置排序 (最快)
    city_positions = []
    for city in available_cities:
        pos = message_content.find(city)
        if pos != -1:
            city_positions.append((pos, city))
    
    if city_positions:
        # 返回最先出现的城市
        city_positions.sort(key=lambda x: x[0])
        return city_positions[0][1]
    
    # 第二层: 基本正则模式匹配 (核心场景覆盖)
    basic_patterns = [
        r"(?:查询|查看|了解)(.+?)(?:的)?(?:天气|温度)",     # "查询北京的天气"
        r"(.+?)(?:的)?(?:天气|温度)(?:如何|怎么样)",        # "北京的天气如何"
        r"(.+?)(?:天气|温度)"                             # "北京天气"
    ]
    
    for pattern in basic_patterns:
        match = re.search(pattern, message_content)
        if match:
            potential_city = match.group(1).strip()
            # 检查提取的城市是否在支持列表中
            for city in available_cities:
                if city in potential_city:
                    return city
    
    return None


async def weather_node(state: AgentState) -> dict[str, list[AIMessage]]:
    """Weather node that generates UI components with complete weather data."""
    # Extract city from the last user message
    last_message = state["messages"][-1] if state["messages"] else None
    user_input = last_message.content if last_message else ""

    # Ensure user_input is a string for processing
    if isinstance(user_input, list):
        user_input = " ".join(str(item) for item in user_input)
    user_input = str(user_input)

    # Enhanced city extraction using the optimized function
    requested_city = extract_city_from_message(user_input)

    # Select weather data
    if requested_city:
        # User specified a city, find matching data
        weather_data = next((w for w in WEATHER_DATA if w["city"] == requested_city), None)
        if not weather_data:
            # City not found, use random data
            weather_data = random.choice(WEATHER_DATA)
    else:
        # No city specified, use default (Beijing)
        weather_data = next((w for w in WEATHER_DATA if w["city"] == "北京"), random.choice(WEATHER_DATA))

    # Create complete weather output
    weather_output: WeatherOutput = {
        "city": weather_data["city"],
        "temperature": weather_data["temperature"],
        "condition": weather_data["condition"],
        "humidity": weather_data["humidity"],
        "windSpeed": weather_data["windSpeed"],
        "description": weather_data["description"]
    }

    # Create meaningful AI message with actual weather information
    weather_icon = {"晴天": "☀️", "多云": "⛅", "阴天": "☁️", "小雨": "🌧️"}.get(weather_data["condition"], "🌤️")
    message_content = f"{weather_icon} {weather_data['description']}"

    message = AIMessage(
        id=str(uuid.uuid4()), 
        content=message_content
    )

    # Emit complete weather data to UI component (仅在 LangGraph 上下文中)
    try:
        push_ui_message("weather", dict(weather_output), message=message)
    except RuntimeError as e:
        # 在测试或非 LangGraph 上下文中运行时，跳过 UI 消息推送
        if "runnable context" not in str(e):
            raise

    return {"messages": [message]}


# Define the graph
graph = (
    StateGraph(AgentState)
    .add_node("weather", weather_node)
    .add_edge("__start__", "weather")
    .compile()
)
