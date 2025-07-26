"""测试消息解析功能的单元测试"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

import pytest
from agent.graph import extract_city_from_message, WEATHER_DATA


class TestMessageParsing:
    """消息解析功能单元测试"""

    def test_extract_city_direct_match(self):
        """测试直接城市匹配"""
        test_cases = [
            ("北京天气", "北京"),
            ("上海的温度", "上海"),
            ("深圳气候", "深圳"),
            ("广州天气如何", "广州"),
            ("杭州的天气怎么样", "杭州"),
        ]
        
        for message, expected_city in test_cases:
            result = extract_city_from_message(message)
            assert result == expected_city, f"消息 '{message}' 应该提取出城市 '{expected_city}', 但得到 '{result}'"

    def test_extract_city_pattern_matching(self):
        """测试模式匹配"""
        test_cases = [
            ("查询北京的天气", "北京"),
            ("了解上海天气", "上海"),
            ("今天深圳的温度", "深圳"),
            ("现在广州天气如何", "广州"),
            ("明天杭州的气候", "杭州"),
        ]
        
        for message, expected_city in test_cases:
            result = extract_city_from_message(message)
            assert result == expected_city, f"消息 '{message}' 应该提取出城市 '{expected_city}', 但得到 '{result}'"

    def test_extract_city_no_city(self):
        """测试没有城市的消息"""
        test_cases = [
            "天气怎么样？",
            "今天气温如何？",
            "你好",
            "帮我查询天气",
            "气候情况",
            ""
        ]
        
        for message in test_cases:
            result = extract_city_from_message(message)
            assert result is None, f"消息 '{message}' 不应该提取出城市，但得到 '{result}'"

    def test_extract_city_unsupported_city(self):
        """测试不支持的城市"""
        test_cases = [
            "火星的天气",
            "月球气候",
            "纽约天气",
            "东京的温度",
            "伦敦天气如何"
        ]
        
        for message in test_cases:
            result = extract_city_from_message(message)
            assert result is None, f"消息 '{message}' 包含不支持的城市，不应该提取出城市，但得到 '{result}'"

    def test_extract_city_mixed_content(self):
        """测试包含多种内容的消息"""
        test_cases = [
            ("我想知道北京和上海的天气", "北京"),  # 应该返回第一个匹配的
            ("从深圳到广州的天气如何", "深圳"),    # 应该返回第一个匹配的
        ]
        
        for message, expected_city in test_cases:
            result = extract_city_from_message(message)
            assert result == expected_city, f"消息 '{message}' 应该提取出城市 '{expected_city}', 但得到 '{result}'"

    def test_extract_city_case_sensitivity(self):
        """测试大小写敏感性（虽然中文没有大小写，但测试字符处理）"""
        # 这些测试确保函数能正确处理各种字符
        test_cases = [
            ("查询 北京 的天气", "北京"),
            ("  上海天气  ", "上海"),
            ("深圳！天气", "深圳"),
        ]
        
        for message, expected_city in test_cases:
            result = extract_city_from_message(message)
            assert result == expected_city, f"消息 '{message}' 应该提取出城市 '{expected_city}', 但得到 '{result}'"

    def test_extract_city_with_all_supported_cities(self):
        """测试所有支持的城市都能被正确提取"""
        supported_cities = {w["city"] for w in WEATHER_DATA}
        
        for city in supported_cities:
            # 测试不同的表达方式
            test_messages = [
                f"{city}天气",
                f"{city}的天气",
                f"查询{city}天气",
                f"今天{city}的温度",
                f"{city}天气如何"
            ]
            
            for message in test_messages:
                result = extract_city_from_message(message)
                assert result == city, f"消息 '{message}' 应该提取出城市 '{city}', 但得到 '{result}'"

    def test_extract_city_function_return_type(self):
        """测试函数返回类型"""
        # 测试有效返回
        result = extract_city_from_message("北京天气")
        assert isinstance(result, str), "提取到城市时应该返回字符串"
        
        # 测试无效返回
        result = extract_city_from_message("天气")
        assert result is None, "没有提取到城市时应该返回 None"

    def test_extract_city_edge_cases(self):
        """测试边界情况"""
        edge_cases = [
            ("", None),           # 空字符串
            ("   ", None),        # 只有空格
            ("天", None),          # 单个字符
            ("天气", None),        # 只有天气关键词
            ("北", None),          # 城市名称不完整
        ]
        
        for message, expected in edge_cases:
            result = extract_city_from_message(message)
            assert result == expected, f"边界情况 '{message}' 的处理结果不正确"

    def test_weather_patterns_coverage(self):
        """测试天气模式覆盖"""
        patterns_to_test = [
            ("查询北京的天气", "北京"),      # 查询模式
            ("北京的天气如何", "北京"),      # 询问模式  
            ("今天北京天气", "北京"),        # 时间模式
            ("北京天气", "北京"),            # 简单模式
        ]
        
        for message, expected_city in patterns_to_test:
            result = extract_city_from_message(message)
            assert result == expected_city, f"天气模式测试失败: '{message}' -> '{result}' (期望: '{expected_city}')"