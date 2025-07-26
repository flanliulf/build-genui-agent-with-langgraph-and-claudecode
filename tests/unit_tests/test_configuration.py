import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from langgraph.pregel import Pregel
from agent.graph import graph, Configuration, State, WEATHER_DATA


def test_graph_is_pregel_instance() -> None:
    """测试 graph 是 Pregel 实例"""
    assert isinstance(graph, Pregel)


def test_configuration_structure() -> None:
    """测试配置结构"""
    # 测试 Configuration TypedDict
    config = Configuration()
    assert isinstance(config, dict)
    # Configuration 目前为空，保留结构以便未来扩展


def test_state_structure() -> None:
    """测试状态结构"""
    # 测试 State TypedDict
    state = State(messages=[], ui=[])
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
        required_keys = ["city", "temperature", "condition", "humidity", "wind", "description"]
        for key in required_keys:
            assert key in weather


def test_graph_name() -> None:
    """测试 graph 名称"""
    assert graph.name == "Weather Agent"
