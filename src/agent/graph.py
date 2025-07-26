"""Weather Agent with Generative UI support.

Demonstrates how to create UI components from LangGraph nodes.
"""

from __future__ import annotations

import random
import re
import uuid
from typing import Annotated, Any, Dict, Sequence, TypedDict

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
try:
    from langgraph.graph.ui import AnyUIMessage, push_ui_message, ui_message_reducer
except ImportError:
    # Fallback for older versions
    from langgraph.graph import MessagesState
    AnyUIMessage = Any
    def push_ui_message(component_name: str, props: dict, message=None):
        """Fallback implementation for push_ui_message"""
        return {"id": str(uuid.uuid4()), "name": component_name, "props": props}
    def ui_message_reducer(messages, new_message):
        """Fallback implementation for ui_message_reducer"""
        return messages + [new_message] if new_message else messages


class Configuration(TypedDict):
    """Configurable parameters for the weather agent."""
    
    # 目前不需要额外的配置参数，保留空结构以便未来扩展
    pass


class WeatherData(TypedDict):
    """Weather information structure."""

    city: str
    temperature: str
    condition: str
    humidity: str
    wind: str
    description: str


class State(TypedDict):
    """State for the weather agent with message and UI support."""

    messages: Annotated[Sequence[BaseMessage], add_messages]
    ui: Annotated[Sequence[AnyUIMessage], ui_message_reducer]


# Predefined weather data for different cities
WEATHER_DATA = [
    {
        "city": "北京",
        "temperature": "22°C",
        "condition": "晴天",
        "humidity": "45%",
        "wind": "3km/h",
        "description": "今天北京天气晴朗，温度适宜，适合外出活动。"
    },
    {
        "city": "上海",
        "temperature": "18°C",
        "condition": "多云",
        "humidity": "68%",
        "wind": "5km/h",
        "description": "上海今天多云转阴，温度稍凉，建议增添衣物。"
    },
    {
        "city": "深圳",
        "temperature": "26°C",
        "condition": "小雨",
        "humidity": "78%",
        "wind": "7km/h",
        "description": "深圳今天有小雨，湿度较高，出门记得带伞。"
    },
    {
        "city": "广州",
        "temperature": "24°C",
        "condition": "阴天",
        "humidity": "72%",
        "wind": "4km/h",
        "description": "广州今天阴天，温度舒适，适合室内活动。"
    },
    {
        "city": "杭州",
        "temperature": "20°C",
        "condition": "晴天",
        "humidity": "55%",
        "wind": "6km/h",
        "description": "杭州今天晴空万里，温度宜人，是游览的好天气。"
    }
]


def extract_city_from_message(message_content: str) -> str:
    """从用户消息中提取城市名称"""
    # 支持的城市列表
    available_cities = {w["city"] for w in WEATHER_DATA}
    
    # 直接匹配城市名称 - 按在消息中出现的位置排序
    city_positions = []
    for city in available_cities:
        pos = message_content.find(city)
        if pos != -1:
            city_positions.append((pos, city))
    
    if city_positions:
        # 返回最先出现的城市
        city_positions.sort(key=lambda x: x[0])
        return city_positions[0][1]
    
    # 使用正则表达式匹配天气查询模式
    weather_patterns = [
        r"(?:查询|查看|了解|知道)(.+?)(?:的)?(?:天气|气候|温度)",  # 查询北京的天气
        r"(.+?)(?:的)?(?:天气|气候|温度)(?:如何|怎么样|怎样)",    # 北京的天气如何
        r"(?:今天|明天|现在)(.+?)(?:的)?(?:天气|气候|温度)",      # 今天北京天气
        r"(.+?)(?:天气|气候|温度)"                              # 北京天气
    ]
    
    for pattern in weather_patterns:
        match = re.search(pattern, message_content)
        if match:
            potential_city = match.group(1).strip()
            # 检查提取的城市是否在支持列表中
            for city in available_cities:
                if city in potential_city:
                    return city
    
    return None


async def weather_node(state: State, config: RunnableConfig) -> Dict[str, Any]:
    """Weather node that returns static weather data and creates UI components."""
    # 获取最后一条用户消息
    user_message = None
    if state["messages"]:
        # 从后往前找最新的用户消息
        for msg in reversed(state["messages"]):
            if isinstance(msg, HumanMessage):
                user_message = msg
                break
    
    # 从用户消息中提取城市名称
    requested_city = None
    if user_message:
        requested_city = extract_city_from_message(user_message.content)
    
    # 选择天气数据
    if requested_city:
        # 用户指定了城市
        weather_data = next((w for w in WEATHER_DATA if w["city"] == requested_city), None)
        if not weather_data:
            # 如果指定的城市不在数据中，随机选择
            weather_data = random.choice(WEATHER_DATA)
    else:
        # 用户没有指定城市，或者没有用户消息，随机选择
        weather_data = random.choice(WEATHER_DATA)
    
    # 创建响应消息
    if requested_city and requested_city == weather_data["city"]:
        # 用户请求了特定城市且找到了数据
        message_content = f"🌤️ {weather_data['description']}"
    elif requested_city and requested_city != weather_data["city"]:
        # 用户请求了特定城市但没有数据，显示随机城市
        message_content = f"🌤️ 抱歉，没有找到{requested_city}的天气数据，为您显示{weather_data['city']}的天气：{weather_data['description']}"
    else:
        # 用户没有指定城市，显示随机天气
        message_content = f"🌤️ {weather_data['description']}"
    
    # 创建 AI 消息
    message = AIMessage(
        id=str(uuid.uuid4()),
        content=message_content
    )
    
    # 推送 UI 组件数据到前端（仅在 LangGraph 上下文中）
    try:
        push_ui_message("weather", weather_data, message=message)
    except RuntimeError as e:
        # 在测试或非 LangGraph 上下文中运行时，跳过 UI 消息推送
        if "runnable context" not in str(e):
            raise
    
    return {"messages": [message]}


# Define the graph
graph = (
    StateGraph(State, config_schema=Configuration)
    .add_node("weather", weather_node)
    .add_edge("__start__", "weather")
    .compile(name="Weather Agent")
)
