#!/usr/bin/env python3
"""
天气 Agent Generative UI 演示脚本（修复版）

这个脚本展示了如何使用天气 agent 的 generative UI 功能。
用法: uv run python examples/weather_demo_fixed.py
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
    
    return f"""
┌─────────────────────────────────┐
│        🌤️  天气卡片            │
├─────────────────────────────────┤
│ 📍 城市: {city:20} │
│ 🌡️  温度: {temperature:20} │
│ ☁️  状况: {condition:20} │
│ 💧 湿度: {humidity:20} │
│ 💨 风速: {wind:20} │
├─────────────────────────────────┤
│ 📝 描述:                       │
│ {description[:25]:26} │
└─────────────────────────────────┘
"""


def safe_render_ui(result: Dict[str, Any]) -> None:
    """安全地渲染 UI 组件"""
    if result.get('ui') and len(result['ui']) > 0:
        print(render_weather_card(result['ui'][0]))
    else:
        print("📝 注意: UI 组件需要在 LangGraph 服务器上下文中才能显示")


def safe_get_city(result: Dict[str, Any]) -> str:
    """安全地获取城市信息"""
    if result.get('ui') and len(result['ui']) > 0:
        return result['ui'][0]['props']['city']
    else:
        return "未知城市"


async def demo_basic_usage():
    """演示基本用法"""
    print("🔹 基本用法演示")
    print("-" * 40)
    
    user_message = HumanMessage(content="天气怎么样？")
    state = State(messages=[user_message], ui=[])
    config = {"configurable": {}}
    
    result = await graph.ainvoke(state, config)
    
    print(f"👤 用户: {user_message.content}")
    print(f"💬 Agent 消息: {result['messages'][-1].content}")
    safe_render_ui(result)


async def demo_specified_city():
    """演示指定城市 - 从用户消息中提取城市"""
    print("🔹 指定城市演示")
    print("-" * 40)
    
    # 测试不同的城市查询方式
    test_inputs = [
        "北京的天气怎么样？",
        "查询上海天气",
        "今天深圳天气如何"
    ]
    
    for user_input in test_inputs:
        user_message = HumanMessage(content=user_input)
        state = State(messages=[user_message], ui=[])
        config = {"configurable": {}}
        
        result = await graph.ainvoke(state, config)
        
        print(f"👤 用户: {user_input}")
        print(f"💬 Agent 消息: {result['messages'][-1].content}")
        safe_render_ui(result)
        print()


async def demo_random_selection():
    """演示随机选择 - 不指定城市时的行为"""
    print("🔹 随机选择演示")
    print("-" * 40)
    print("📌 当用户没有指定特定城市时，系统会随机选择天气数据")
    
    for i in range(3):
        user_message = HumanMessage(content="天气怎么样？")
        state = State(messages=[user_message], ui=[])
        config = {"configurable": {}}
        
        result = await graph.ainvoke(state, config)
        city = safe_get_city(result)
        
        print(f"🔄 第 {i+1} 次调用 - 随机城市: {city}")
        print(f"💬 Agent 消息: {result['messages'][-1].content}")
        safe_render_ui(result)
        print()


async def demo_error_handling():
    """演示错误处理 - 不支持的城市"""
    print("🔹 错误处理演示")
    print("-" * 40)
    print("📌 当用户询问不支持的城市时，系统会提供友好的回退")
    
    user_message = HumanMessage(content="东京的天气怎么样？")
    state = State(messages=[user_message], ui=[])
    config = {"configurable": {}}
    
    result = await graph.ainvoke(state, config)
    actual_city = safe_get_city(result)
    
    print(f"👤 用户: {user_message.content}")
    print(f"💬 Agent 消息: {result['messages'][-1].content}")
    print(f"🎯 实际返回的城市: {actual_city}")
    safe_render_ui(result)


async def demo_concurrent_calls():
    """演示并发调用"""
    print("🔹 并发调用演示")
    print("-" * 40)
    print("📌 同时处理多个用户请求")
    
    async def single_call(call_id: int, user_input: str):
        user_message = HumanMessage(content=user_input)
        state = State(messages=[user_message], ui=[])
        config = {"configurable": {}}
        
        result = await graph.ainvoke(state, config)
        city = safe_get_city(result)
        return call_id, city
    
    # 创建多个并发调用
    tasks = [
        single_call(1, "北京天气"),
        single_call(2, "上海天气"),
        single_call(3, "深圳天气"),
    ]
    
    results = await asyncio.gather(*tasks)
    
    for call_id, city in results:
        print(f"✅ 调用 {call_id} 完成 - 城市: {city}")


async def demo_data_structure():
    """演示数据结构"""
    print("🔹 数据结构演示")
    print("-" * 40)
    print("📌 展示完整的响应数据结构")
    
    user_message = HumanMessage(content="杭州天气怎么样？")
    state = State(messages=[user_message], ui=[])
    config = {"configurable": {}}
    
    result = await graph.ainvoke(state, config)
    
    print("📊 完整的响应数据:")
    print(f"🔸 消息数量: {len(result['messages'])}")
    print(f"🔸 UI 组件数量: {len(result['ui'])}")
    
    # 显示消息内容
    for i, msg in enumerate(result['messages']):
        print(f"  消息 {i+1}: {type(msg).__name__}")
        print(f"    内容: {msg.content}")
        print(f"    ID: {msg.id}")
    
    # 显示 UI 数据
    if result['ui']:
        ui_data = result['ui'][0]
        print(f"🔸 UI 组件类型: {ui_data.get('name', 'N/A')}")
        print(f"🔸 组件属性: {json.dumps(ui_data.get('props', {}), ensure_ascii=False, indent=2)}")
    else:
        print("🔸 UI 组件: 无（需要 LangGraph 服务器上下文）")


async def main():
    """主函数"""
    print("🌤️  天气 Agent Generative UI 演示")
    print("=" * 50)
    print(f"📊 可用城市: {', '.join([w['city'] for w in WEATHER_DATA])}")
    print("=" * 50)
    print()
    
    # 运行所有演示
    await demo_basic_usage()
    print()
    
    await demo_specified_city()
    print()
    
    await demo_random_selection()
    print()
    
    await demo_error_handling() 
    print()
    
    await demo_concurrent_calls()
    print()
    
    await demo_data_structure()
    print()
    
    print("✅ 所有演示完成！")
    print("💡 提示: 要在完整的 LangGraph 环境中看到 UI 组件效果，请运行:")
    print("   uv run langgraph dev")


if __name__ == "__main__":
    asyncio.run(main())