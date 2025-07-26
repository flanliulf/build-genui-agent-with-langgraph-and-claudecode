import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

import pytest

from langchain_core.messages import HumanMessage
from agent import graph
from agent.graph import State

pytestmark = pytest.mark.anyio


@pytest.mark.langsmith
async def test_weather_agent_basic_functionality() -> None:
    """测试天气 agent 基本功能"""
    # 创建包含用户消息的输入状态
    inputs = State(
        messages=[HumanMessage(content="天气怎么样？")],
        ui=[]
    )
    config = {"configurable": {}}
    
    # 调用 graph
    result = await graph.ainvoke(inputs, config)
    
    # 基本验证
    assert result is not None
    assert "messages" in result
    assert "ui" in result
    assert len(result["messages"]) > 0
    assert len(result["ui"]) > 0


@pytest.mark.langsmith
async def test_weather_agent_with_city_message() -> None:
    """测试包含城市消息的天气 agent"""
    inputs = State(
        messages=[HumanMessage(content="北京天气怎么样？")],
        ui=[]
    )
    config = {"configurable": {}}
    
    result = await graph.ainvoke(inputs, config)
    
    assert result is not None
    assert len(result["messages"]) >= 2  # 原始用户消息 + AI 回复
    assert len(result["ui"]) == 1
    
    # 验证返回了北京的数据
    ui_data = result["ui"][0]
    assert ui_data["props"]["city"] == "北京"
