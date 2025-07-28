"""测试 UI 组件数据生成的单元测试"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

import pytest
from unittest.mock import patch, MagicMock

from agent.graph import WEATHER_DATA, WeatherOutput


class TestUIDataGeneration:
    """UI 数据生成单元测试"""

    def test_weather_output_type_definition(self):
        """测试 WeatherOutput TypedDict 结构"""
        # 创建测试数据
        weather_data = WeatherOutput(
            city="测试城市",
            temperature="25°C",
            condition="晴天",
            humidity="50%",
            windSpeed="5km/h",
            description="测试描述"
        )
        
        assert weather_data["city"] == "测试城市"
        assert weather_data["temperature"] == "25°C"
        assert weather_data["condition"] == "晴天"
        assert weather_data["humidity"] == "50%"
        assert weather_data["windSpeed"] == "5km/h"
        assert weather_data["description"] == "测试描述"

    def test_all_weather_data_completeness(self):
        """测试所有天气数据的完整性"""
        for i, weather in enumerate(WEATHER_DATA):
            # 验证所有必需字段都存在且不为空
            required_fields = ["city", "temperature", "condition", "humidity", "windSpeed", "description"]
            
            for field in required_fields:
                assert field in weather, f"天气数据 {i} 缺少字段 '{field}'"
                assert weather[field], f"天气数据 {i} 的字段 '{field}' 为空"
                assert isinstance(weather[field], str), f"天气数据 {i} 的字段 '{field}' 不是字符串类型"

    def test_weather_data_format_validation(self):
        """测试天气数据格式验证"""
        for weather in WEATHER_DATA:
            # 验证温度格式 (应该以°C结尾)
            assert weather["temperature"].endswith("°C"), f"温度格式错误: {weather['temperature']}"
            
            # 验证湿度格式 (应该以%结尾)
            assert weather["humidity"].endswith("%"), f"湿度格式错误: {weather['humidity']}"
            
            # 验证风速格式 (应该以km/h结尾)
            assert weather["windSpeed"].endswith("km/h"), f"风速格式错误: {weather['windSpeed']}"
            
            # 验证城市名称不为空且长度合理
            assert len(weather["city"]) >= 2, f"城市名称过短: {weather['city']}"
            assert len(weather["city"]) <= 10, f"城市名称过长: {weather['city']}"
            
            # 验证描述不为空且长度合理
            assert len(weather["description"]) >= 10, f"描述过短: {weather['description']}"
            assert len(weather["description"]) <= 50, f"描述过长: {weather['description']}"

    def test_weather_conditions_mapping(self):
        """测试天气状况映射"""
        # 定义有效的天气状况
        valid_conditions = {"晴天", "多云", "阴天", "小雨", "大雨", "雪", "雾"}
        
        for weather in WEATHER_DATA:
            condition = weather["condition"]
            assert condition in valid_conditions, f"无效的天气状况: {condition}"

    def test_city_uniqueness(self):
        """测试城市名称唯一性"""
        cities = [weather["city"] for weather in WEATHER_DATA]
        unique_cities = set(cities)
        
        assert len(cities) == len(unique_cities), "存在重复的城市名称"

    def test_temperature_range_validation(self):
        """测试温度范围合理性"""
        for weather in WEATHER_DATA:
            temp_str = weather["temperature"].replace("°C", "")
            
            try:
                temp_value = int(temp_str)
                # 验证温度在合理范围内 (-50°C 到 50°C)
                assert -50 <= temp_value <= 50, f"温度超出合理范围: {temp_value}°C"
            except ValueError:
                pytest.fail(f"无法解析温度值: {weather['temperature']}")

    def test_humidity_range_validation(self):
        """测试湿度范围合理性"""
        for weather in WEATHER_DATA:
            humidity_str = weather["humidity"].replace("%", "")
            
            try:
                humidity_value = int(humidity_str)
                # 验证湿度在 0-100% 范围内
                assert 0 <= humidity_value <= 100, f"湿度超出范围: {humidity_value}%"
            except ValueError:
                pytest.fail(f"无法解析湿度值: {weather['humidity']}")

    def test_wind_speed_validation(self):
        """测试风速合理性"""
        for weather in WEATHER_DATA:
            wind_str = weather["windSpeed"].replace("km/h", "")
            
            try:
                wind_value = int(wind_str)
                # 验证风速在合理范围内 (0-100 km/h)
                assert 0 <= wind_value <= 100, f"风速超出合理范围: {wind_value}km/h"
            except ValueError:
                pytest.fail(f"无法解析风速值: {weather['windSpeed']}")

    def test_description_content_validation(self):
        """测试描述内容合理性"""
        for weather in WEATHER_DATA:
            description = weather["description"]
            city = weather["city"]
            
            # 验证描述包含城市名称
            assert city in description, f"描述中缺少城市名称: {description}"
            
            # 验证描述包含天气相关词汇
            weather_keywords = ["天气", "温度", "适合", "建议", "出门", "活动", "记得", "增添", "衣物", "带伞"]
            has_weather_keyword = any(keyword in description for keyword in weather_keywords)
            assert has_weather_keyword, f"描述中缺少天气相关词汇: {description}"

    def test_ui_message_structure(self):
        """测试 UI 消息结构"""
        # 这个测试验证 UI 消息应该具有的基本结构
        expected_ui_message = {
            "id": "test-ui-id",
            "name": "weather",
            "props": WEATHER_DATA[0]
        }
        
        # 验证结构
        assert "id" in expected_ui_message
        assert "name" in expected_ui_message
        assert "props" in expected_ui_message
        
        assert expected_ui_message["name"] == "weather"
        assert expected_ui_message["props"] == WEATHER_DATA[0]
        
        # 验证 props 包含所有必需的天气字段
        props = expected_ui_message["props"]
        required_fields = ["city", "temperature", "condition", "humidity", "windSpeed", "description"]
        for field in required_fields:
            assert field in props

    def test_weather_data_json_serializable(self):
        """测试天气数据可以序列化为 JSON"""
        import json
        
        for weather in WEATHER_DATA:
            try:
                json_str = json.dumps(weather, ensure_ascii=False)
                deserialized = json.loads(json_str)
                assert deserialized == weather
            except (TypeError, ValueError) as e:
                pytest.fail(f"天气数据无法序列化为 JSON: {e}")

    def test_ui_component_props_compatibility(self):
        """测试 UI 组件属性兼容性"""
        # 验证天气数据包含 UI 组件所需的所有属性
        required_ui_props = ["city", "temperature", "condition", "humidity", "windSpeed", "description"]
        
        for weather in WEATHER_DATA:
            for prop in required_ui_props:
                assert prop in weather, f"天气数据缺少 UI 组件所需属性: {prop}"
                
        # 验证数据类型符合 TypeScript 接口要求
        for weather in WEATHER_DATA:
            for prop in required_ui_props:
                assert isinstance(weather[prop], str), f"属性 {prop} 应该是字符串类型"