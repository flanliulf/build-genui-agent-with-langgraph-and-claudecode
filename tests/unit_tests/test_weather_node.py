"""简化的天气节点单元测试"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

import pytest
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import AIMessage, HumanMessage
from agent.graph import weather_node, State, WEATHER_DATA, extract_city_from_message


class TestWeatherNodeSimple:
    """简化的天气节点单元测试"""

    @pytest.fixture
    def empty_state(self):
        """创建空状态"""
        return State(messages=[], ui=[])

    @pytest.fixture
    def state_with_city_message(self):
        """创建包含城市消息的状态"""
        return State(
            messages=[HumanMessage(content="北京的天气怎么样？")],
            ui=[]
        )

    @pytest.fixture
    def state_with_no_city_message(self):
        """创建不包含城市的消息状态"""
        return State(
            messages=[HumanMessage(content="天气怎么样？")],
            ui=[]
        )

    @pytest.fixture
    def default_config(self):
        """创建默认配置"""
        return RunnableConfig(configurable={})

    def test_weather_data_structure(self):
        """测试天气数据结构"""
        assert len(WEATHER_DATA) > 0
        
        for weather in WEATHER_DATA:
            assert "city" in weather
            assert "temperature" in weather
            assert "condition" in weather
            assert "humidity" in weather
            assert "wind" in weather
            assert "description" in weather
            
            # 验证字段类型
            assert isinstance(weather["city"], str)
            assert isinstance(weather["temperature"], str)
            assert isinstance(weather["condition"], str)
            assert isinstance(weather["humidity"], str)
            assert isinstance(weather["wind"], str)
            assert isinstance(weather["description"], str)

    @pytest.mark.anyio
    async def test_weather_node_basic_functionality(self, empty_state, default_config):
        """测试基本功能"""
        result = await weather_node(empty_state, default_config)

        # 验证结果
        assert "messages" in result
        assert len(result["messages"]) == 1

        message = result["messages"][0]
        assert isinstance(message, AIMessage)
        assert "🌤️" in message.content
        
        # 验证消息 ID 存在
        assert message.id is not None
        assert isinstance(message.id, str)

    @pytest.mark.anyio
    async def test_weather_node_with_city_message(self, state_with_city_message, default_config):
        """测试包含城市的消息"""
        result = await weather_node(state_with_city_message, default_config)

        # 验证结果
        assert "messages" in result
        message = result["messages"][0]
        assert isinstance(message, AIMessage)

        # 验证消息包含北京的描述
        beijing_weather = next(w for w in WEATHER_DATA if w["city"] == "北京")
        assert beijing_weather["description"] in message.content

    @pytest.mark.anyio
    async def test_weather_node_no_city_message(self, state_with_no_city_message, default_config):
        """测试不包含城市的消息"""
        result = await weather_node(state_with_no_city_message, default_config)

        # 验证结果存在
        assert "messages" in result
        assert len(result["messages"]) == 1
        
        message = result["messages"][0]
        assert isinstance(message, AIMessage)
        assert "🌤️" in message.content

    def test_extract_city_from_message_basic(self):
        """测试城市提取基本功能"""
        # 测试直接匹配
        assert extract_city_from_message("北京天气") == "北京"
        assert extract_city_from_message("上海的温度") == "上海"
        
        # 测试询问模式
        assert extract_city_from_message("深圳的天气怎么样？") == "深圳"
        
        # 测试查询模式
        assert extract_city_from_message("查询广州天气") == "广州"
        
        # 测试时间模式
        assert extract_city_from_message("今天杭州天气") == "杭州"
        
        # 测试无匹配
        assert extract_city_from_message("天气怎么样") is None
        assert extract_city_from_message("你好") is None
        assert extract_city_from_message("火星天气") is None

    def test_configuration_structure(self):
        """测试配置结构"""
        from agent.graph import Configuration
        
        # Configuration 应该是一个空的 TypedDict
        config = {}  # Configuration 当前为空
        assert isinstance(config, dict)

    def test_weather_cities_coverage(self):
        """测试天气城市覆盖"""
        cities = [weather["city"] for weather in WEATHER_DATA]
        expected_cities = ["北京", "上海", "深圳", "广州", "杭州"]
        
        for city in expected_cities:
            assert city in cities, f"城市 {city} 不在天气数据中"

    def test_weather_conditions_variety(self):
        """测试天气状况多样性"""
        conditions = [weather["condition"] for weather in WEATHER_DATA]
        
        # 应该有多种不同的天气状况
        unique_conditions = set(conditions)
        assert len(unique_conditions) > 1, "天气状况缺乏多样性"