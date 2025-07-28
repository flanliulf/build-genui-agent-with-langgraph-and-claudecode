#!/usr/bin/env python3
"""
测试修复后的UI组件功能
"""

import asyncio
import sys
import os

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from langchain_core.messages import HumanMessage
from agent.graph import graph, AgentState

async def test_ui_components():
    """测试UI组件是否正常工作"""
    print("🧪 测试修复后的UI组件功能")
    print("=" * 50)
    
    # 测试不同城市
    test_cases = [
        "北京天气怎么样？",
        "上海的天气如何？", 
        "深圳天气",
        "广州今天天气",
        "杭州天气预报"
    ]
    
    for i, user_input in enumerate(test_cases, 1):
        print(f"\n🔹 测试用例 {i}: {user_input}")
        print("-" * 30)
        
        # 创建状态
        state = AgentState(
            messages=[HumanMessage(content=user_input)],
            ui=[]
        )
        
        # 调用图
        result = await graph.ainvoke(state)
        
        # 分析结果
        messages = result.get("messages", [])
        ui_components = result.get("ui", [])
        
        print(f"📝 AI响应: {messages[-1].content if messages else '无响应'}")
        
        if ui_components:
            ui_data = ui_components[-1]
            print(f"🎨 UI组件: {ui_data.get('name', 'unknown')}")
            print(f"🏙️ 城市数据: {ui_data.get('props', {})}")
            print(f"✅ UI组件成功推送!")
        else:
            print("❌ 没有UI组件数据")
            
        print()

if __name__ == "__main__":
    asyncio.run(test_ui_components())