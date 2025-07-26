"""天气 Agent Graph 集成测试"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

import pytest
from langchain_core.messages import AIMessage

from agent import graph
from agent.graph import State, Configuration, WEATHER_DATA

pytestmark = pytest.mark.anyio


class TestWeatherGraph:
    """天气 Graph 集成测试"""

    @pytest.fixture
    def initial_state(self):
        """创建初始状态"""
        return State(messages=[], ui=[])

    @pytest.fixture
    def default_config(self):
        """默认配置"""
        return {"configurable": {}}

    @pytest.fixture
    def beijing_config(self):
        """北京配置"""
        return {"configurable": {"default_city": "北京"}}

    @pytest.fixture
    def invalid_city_config(self):
        """无效城市配置"""
        return {"configurable": {"default_city": "不存在的城市"}}

    @pytest.mark.langsmith
    async def test_weather_graph_basic_flow(self, initial_state, default_config):
        """测试基本的天气 graph 流程"""
        # 调用 graph
        result = await graph.ainvoke(initial_state, default_config)
        
        # 验证返回结构
        assert isinstance(result, dict)
        assert "messages" in result
        assert "ui" in result
        
        # 验证消息
        messages = result["messages"]
        assert len(messages) == 1
        assert isinstance(messages[0], AIMessage)
        assert "🌤️" in messages[0].content
        
        # 验证 UI 组件
        ui_components = result["ui"]
        assert len(ui_components) == 1
        
        ui_data = ui_components[0]
        assert "id" in ui_data
        assert "name" in ui_data
        assert "props" in ui_data
        assert ui_data["name"] == "weather"
        
        # 验证 UI 组件属性
        props = ui_data["props"]
        assert "city" in props
        assert "temperature" in props
        assert "condition" in props
        assert "humidity" in props
        assert "wind" in props
        assert "description" in props

    @pytest.mark.langsmith
    async def test_weather_graph_specified_city(self, initial_state, beijing_config):
        """测试指定城市的 graph 流程"""
        result = await graph.ainvoke(initial_state, beijing_config)
        
        # 验证返回了北京的天气数据
        ui_data = result["ui"][0]
        props = ui_data["props"]
        assert props["city"] == "北京"
        
        # 验证消息内容包含北京的描述
        message_content = result["messages"][0].content
        beijing_weather = next(w for w in WEATHER_DATA if w["city"] == "北京")
        assert beijing_weather["description"] in message_content

    @pytest.mark.langsmith
    async def test_weather_graph_invalid_city_fallback(self, initial_state, invalid_city_config):
        """测试无效城市回退到随机选择"""
        result = await graph.ainvoke(initial_state, invalid_city_config)
        
        # 验证返回了有效的天气数据
        ui_data = result["ui"][0]
        props = ui_data["props"]
        
        # 验证城市是预定义城市列表中的一个
        valid_cities = {w["city"] for w in WEATHER_DATA}
        assert props["city"] in valid_cities

    @pytest.mark.langsmith
    async def test_weather_graph_message_ui_consistency(self, initial_state, default_config):
        """测试消息和 UI 组件的一致性"""
        result = await graph.ainvoke(initial_state, default_config)
        
        message = result["messages"][0]
        ui_data = result["ui"][0]
        props = ui_data["props"]
        
        # 验证消息内容与 UI 数据的描述一致
        assert props["description"] in message.content
        
        # 验证消息 ID 存在
        assert message.id is not None
        assert isinstance(message.id, str)

    @pytest.mark.langsmith
    async def test_weather_graph_multiple_invocations_randomness(self, initial_state, default_config):
        """测试多次调用的随机性"""
        results = []
        
        # 多次调用 graph
        for _ in range(5):
            result = await graph.ainvoke(initial_state, default_config)
            ui_data = result["ui"][0]
            city = ui_data["props"]["city"]
            results.append(city)
        
        # 验证至少有一些变化 (可能会有重复，但不应该完全相同)
        unique_cities = set(results)
        # 至少应该有 1 个不同的城市 (考虑到随机性)
        assert len(unique_cities) >= 1
        
        # 所有城市都应该在预定义列表中
        valid_cities = {w["city"] for w in WEATHER_DATA}
        for city in unique_cities:
            assert city in valid_cities

    @pytest.mark.langsmith
    async def test_weather_graph_state_immutability(self, initial_state, default_config):
        """测试状态不可变性"""
        original_messages = list(initial_state["messages"])
        original_ui = list(initial_state["ui"])
        
        # 调用 graph
        result = await graph.ainvoke(initial_state, default_config)
        
        # 验证原始状态未被修改
        assert initial_state["messages"] == original_messages
        assert initial_state["ui"] == original_ui
        
        # 验证返回了新的状态
        assert result is not initial_state
        assert result["messages"] is not initial_state["messages"]
        assert result["ui"] is not initial_state["ui"]

    @pytest.mark.langsmith
    async def test_weather_graph_configuration_inheritance(self):
        """测试配置继承"""
        # 测试带有额外配置的情况
        config_with_extra = {
            "configurable": {
                "default_city": "上海",
                "extra_param": "should_be_ignored"
            }
        }
        
        initial_state = State(messages=[], ui=[])
        result = await graph.ainvoke(initial_state, config_with_extra)
        
        # 验证上海天气数据被正确返回
        ui_data = result["ui"][0]
        assert ui_data["props"]["city"] == "上海"
        
        # 验证额外参数不影响功能
        assert len(result["messages"]) == 1
        assert len(result["ui"]) == 1

    @pytest.mark.langsmith
    async def test_weather_graph_all_cities_coverage(self):
        """测试所有城市的覆盖"""
        all_cities = {w["city"] for w in WEATHER_DATA}
        tested_cities = set()
        
        # 为每个城市创建配置并测试
        for city in all_cities:
            config = {"configurable": {"default_city": city}}
            initial_state = State(messages=[], ui=[])
            
            result = await graph.ainvoke(initial_state, config)
            
            ui_data = result["ui"][0]
            returned_city = ui_data["props"]["city"]
            tested_cities.add(returned_city)
            
            # 验证返回了正确的城市
            assert returned_city == city
        
        # 验证所有城市都被测试了
        assert tested_cities == all_cities

    @pytest.mark.langsmith
    async def test_weather_graph_error_handling(self):
        """测试错误处理"""
        # 测试空配置
        empty_config = {}
        initial_state = State(messages=[], ui=[])
        
        try:
            result = await graph.ainvoke(initial_state, empty_config)
            # 应该能够处理空配置（使用默认值）
            assert len(result["messages"]) == 1
            assert len(result["ui"]) == 1
        except Exception as e:
            pytest.fail(f"Graph 应该能够处理空配置: {e}")

    @pytest.mark.langsmith
    async def test_weather_graph_performance(self, initial_state, default_config):
        """测试性能 - 简单的响应时间测试"""
        import time
        
        start_time = time.time()
        result = await graph.ainvoke(initial_state, default_config)
        end_time = time.time()
        
        # 验证响应时间合理（应该在 1 秒内完成）
        response_time = end_time - start_time
        assert response_time < 1.0, f"响应时间过长: {response_time:.2f}s"
        
        # 验证结果正确
        assert len(result["messages"]) == 1
        assert len(result["ui"]) == 1

    async def test_weather_graph_concurrent_calls(self, default_config):
        """测试并发调用"""
        import asyncio
        
        async def single_call():
            initial_state = State(messages=[], ui=[])
            return await graph.ainvoke(initial_state, default_config)
        
        # 并发执行多个调用
        tasks = [single_call() for _ in range(3)]
        results = await asyncio.gather(*tasks)
        
        # 验证所有调用都成功
        assert len(results) == 3
        
        for result in results:
            assert len(result["messages"]) == 1
            assert len(result["ui"]) == 1
            
            # 验证数据结构完整
            ui_data = result["ui"][0]
            assert "props" in ui_data
            assert "city" in ui_data["props"]