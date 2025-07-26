#!/usr/bin/env python3
"""
天气 Agent Generative UI 演示脚本

这个脚本展示了如何使用天气 agent 的 generative UI 功能。
用法: uv run python examples/weather_demo.py
"""

import asyncio
import json
import sys
import os
from typing import Dict, Any

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from langchain_core.messages import HumanMessage
from agent.graph import graph, State, WEATHER_DATA


def render_weather_card(ui_data: Dict[str, Any]) -> str:
    """渲染天气卡片的文本版本"""
    if not ui_data or "props" not in ui_data:
        return "❌ 没有 UI 数据"
    
    props = ui_data["props"]
    city = props.get("city", "N/A")
    temperature = props.get("temperature", "N/A")
    condition = props.get("condition", "N/A")
    humidity = props.get("humidity", "N/A")
    wind = props.get("wind", "N/A")
    description = props.get("description", "N/A")
    
    # 天气图标映射
    weather_icons = {
        '晴天': '☀️',
        '多云': '⛅',
        '阴天': '☁️',
        '小雨': '🌧️',
        '大雨': '🌧️',
        '雪': '❄️',
        '雾': '🌫️'
    }
    icon = weather_icons.get(condition, '🌤️')
    
    # 创建天气卡片
    card = f"""
╭─────────────────────────────────────╮
│  {icon} {city} 天气                    │
├─────────────────────────────────────┤
│  🌡️  温度: {temperature:<20} │
│  ☁️  状况: {condition:<20} │
│  💧  湿度: {humidity:<20} │
│  💨  风速: {wind:<20} │
├─────────────────────────────────────┤
│  📝 {description:<25} │
╰─────────────────────────────────────╯
"""
    return card


async def demo_basic_usage():
    """演示基本用法 - 用户询问天气但不指定城市"""
    print("🔹 基本用法演示")
    print("-" * 40)
    
    # 用户询问天气但不指定城市
    user_message = HumanMessage(content="天气怎么样？")
    state = State(messages=[user_message], ui=[])
    config = {"configurable": {}}
    
    result = await graph.ainvoke(state, config)
    
    print(f"👤 用户: {user_message.content}")
    print(f"💬 Agent 消息: {result['messages'][-1].content}")
    
    # 处理 UI 组件（在直接运行时可能为空）
    if result['ui']:
        print(f"🖼️  UI 组件: {result['ui'][0]['name']}")
        print(render_weather_card(result['ui'][0]))
    else:
        print("📝 注意: UI 组件需要在 LangGraph 服务器上下文中才能显示")


async def demo_specified_city():
    """演示指定城市 - 从用户消息中提取城市"""
    print("🔹 指定城市演示")
    print("-" * 40)
    
    # 测试不同的用户表达方式
    test_messages = [
        "北京的天气怎么样？",
        "查询上海天气",
        "今天深圳的温度如何",
        "广州天气",
        "杭州的气候"
    ]
    
    for user_input in test_messages:
        user_message = HumanMessage(content=user_input)
        state = State(messages=[user_message], ui=[])
        config = {"configurable": {}}
        
        result = await graph.ainvoke(state, config)
        
        print(f"👤 用户: {user_input}")
        print(f"💬 Agent 消息: {result['messages'][-1].content}")
        
        # 处理 UI 组件
        if result['ui']:
            print(render_weather_card(result['ui'][0]))
        else:
            print("📝 注意: UI 组件需要在 LangGraph 服务器上下文中才能显示")
        print()


async def demo_random_selection():
    """演示随机选择 - 不指定城市时的行为"""
    print("🔹 随机选择演示")
    print("-" * 40)
    
    results = []
    for i in range(5):
        # 用户询问天气但不指定城市
        user_message = HumanMessage(content="天气怎么样？")
        state = State(messages=[user_message], ui=[])
        config = {"configurable": {}}
        
        result = await graph.ainvoke(state, config)
        city = result['ui'][0]['props']['city']
        results.append(city)
        
        print(f"第{i+1}次: {city}")
    
    unique_cities = set(results)
    print(f"\n📊 统计: 5次调用获得了 {len(unique_cities)} 个不同城市: {', '.join(unique_cities)}")
    print()


async def demo_error_handling():
    """演示错误处理 - 不支持的城市"""
    print("🔹 错误处理演示")
    print("-" * 40)
    
    # 测试不支持的城市
    test_cases = [
        "火星的天气如何？",
        "纽约天气怎么样？",
        "东京的温度"
    ]
    
    for user_input in test_cases:
        user_message = HumanMessage(content=user_input)
        state = State(messages=[user_message], ui=[])
        config = {"configurable": {}}
        
        result = await graph.ainvoke(state, config)
        actual_city = result['ui'][0]['props']['city']
        
        print(f"👤 用户: {user_input}")
        print(f"💬 Agent 消息: {result['messages'][-1].content}")
        print(f"🔄 实际显示城市: {actual_city} (自动回退到随机城市)")
        print(render_weather_card(result['ui'][0]))
        print()


async def demo_concurrent_calls():
    """演示并发调用"""
    print("🔹 并发调用演示")
    print("-" * 40)
    
    async def single_call(call_id: int):
        state = State(messages=[], ui=[])
        config = {"configurable": {}}
        result = await graph.ainvoke(state, config)
        return call_id, result['ui'][0]['props']['city']
    
    # 并发执行3个调用
    tasks = [single_call(i) for i in range(1, 4)]
    results = await asyncio.gather(*tasks)
    
    print("并发执行3个调用:")
    for call_id, city in results:
        print(f"  调用 {call_id}: {city}")
    
    print()


async def demo_data_structure():
    """演示数据结构"""
    print("🔹 数据结构演示")
    print("-" * 40)
    
    state = State(messages=[], ui=[])
    config = {"configurable": {"default_city": "杭州"}}
    
    result = await graph.ainvoke(state, config)
    
    print("📋 完整的返回数据结构:")
    print(f"Messages: {len(result['messages'])} 条")
    print(f"UI Components: {len(result['ui'])} 个")
    
    print("\n📝 消息详情:")
    message = result['messages'][0]
    print(f"  - ID: {message.id}")
    print(f"  - 类型: {type(message).__name__}")
    print(f"  - 内容: {message.content}")
    
    print("\n🖼️  UI 组件详情:")
    ui_data = result['ui'][0]
    print(f"  - ID: {ui_data.get('id', 'N/A')}")
    print(f"  - 名称: {ui_data.get('name', 'N/A')}")
    print(f"  - 属性: {json.dumps(ui_data.get('props', {}), ensure_ascii=False, indent=4)}")
    
    print()


async def main():
    """主程序"""
    print("🌤️  天气 Agent Generative UI 演示")
    print("=" * 50)
    print(f"📊 可用城市: {', '.join(w['city'] for w in WEATHER_DATA)}")
    print("=" * 50)
    print()
    
    # 运行所有演示
    await demo_basic_usage()
    print()
    
    await demo_specified_city()
    
    await demo_random_selection()
    
    await demo_error_handling()
    print()
    
    await demo_concurrent_calls()
    
    await demo_data_structure()
    
    print("✅ 所有演示完成!")
    print()
    print("📖 集成说明:")
    print("1. 后端: 使用 LangGraph 创建天气节点")
    print("2. 前端: 使用 React + Tailwind CSS 渲染 UI 组件")
    print("3. 通信: 通过 push_ui_message 发送组件数据")
    print("4. 配置: 在 langgraph.json 中注册 UI 组件")
    print()
    print("🚀 要启动开发服务器，请运行: langgraph dev")


if __name__ == "__main__":
    asyncio.run(main())