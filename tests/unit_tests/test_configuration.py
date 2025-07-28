import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from langgraph.pregel import Pregel
from agent.graph import graph, AgentState, WEATHER_DATA


def test_graph_is_pregel_instance() -> None:
    """测试 graph 是 Pregel 实例"""
    assert isinstance(graph, Pregel)


def test_agent_state_structure() -> None:
    """测试AgentState结构"""
    # 测试 AgentState TypedDict
    state = AgentState(messages=[], ui=[])
    assert "messages" in state
    assert "ui" in state
    assert isinstance(state["messages"], list)
    assert isinstance(state["ui"], list)


def test_weather_data_constants() -> None:
    """测试天气数据常量"""
    assert isinstance(WEATHER_DATA, list)
    assert len(WEATHER_DATA) > 0
    
    # 验证每个天气数据的结构
    for weather in WEATHER_DATA:
        assert isinstance(weather, dict)
        required_keys = ["city", "temperature", "condition", "humidity", "windSpeed", "description"]
        for key in required_keys:
            assert key in weather


def test_graph_compilation() -> None:
    """测试 graph 编译"""
    assert graph is not None
    # 图已经编译，可以进行基本调用
