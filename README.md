# Weather Agent with Generative UI

基于 LangGraph 构建的智能天气 Agent，具备 Generative UI 功能，支持自然语言交互和动态 React 组件生成。

## 🌟 核心特性

- ✅ **智能消息解析** - 从用户自然语言中提取城市信息
- ✅ **动态 UI 生成** - 后端动态生成 React 天气卡片组件
- ✅ **多种表达支持** - 支持各种中文天气查询表达方式
- ✅ **无 LLM 依赖** - 使用静态数据，快速响应
- ✅ **响应式设计** - Tailwind CSS 美观界面
- ✅ **完整测试** - 全面的单元测试和集成测试

## 🚀 快速开始

### 安装依赖
```bash
# 使用 uv（推荐）
uv sync

# 或使用 pip
pip install -e . "langgraph-cli[inmem]"
```

### 运行演示
```bash
# 查看功能演示
uv run python examples/weather_demo.py

# 启动开发服务器
uv run langgraph dev
```

### 基本使用
```python
from langchain_core.messages import HumanMessage
from agent.graph import graph, State

# 创建用户查询
state = State(
    messages=[HumanMessage(content="北京天气怎么样？")],
    ui=[]
)

# 调用 agent
result = await graph.ainvoke(state, {"configurable": {}})

# 获取结果
ai_message = result["messages"][-1].content  # AI 回复
ui_data = result["ui"][-1]["props"]          # UI 组件数据
```

## 🏗️ 项目结构

```
.
├── src/agent/           # 核心 Agent 代码
│   ├── graph.py         # 主要 graph 定义和天气节点
│   └── ui.tsx          # React UI 组件
├── tests/              # 测试套件
│   ├── unit_tests/     # 单元测试
│   └── integration_tests/ # 集成测试
├── examples/           # 示例和演示
│   └── weather_demo.py # 功能演示脚本
└── docs/              # 项目文档
    ├── features/      # 功能文档
    └── testing/       # 测试文档
```

## 💬 支持的查询方式

### 直接城市查询
- "北京天气"
- "上海的温度"
- "深圳气候"

### 询问模式
- "北京的天气怎么样？"
- "上海天气如何？"
- "深圳的气候怎样？"

### 查询模式
- "查询北京的天气"
- "了解上海天气"
- "知道深圳的气候"

### 时间模式
- "今天北京天气"
- "明天上海的温度"
- "现在深圳天气"

## 🧪 测试

```bash
# 使用 make 命令（推荐，自动优先使用 uv）
make test                    # 运行所有单元测试
make integration_tests       # 运行集成测试
make test_watch             # 监视模式运行测试

# 运行特定测试文件
make test TEST_FILE=tests/unit_tests/test_message_parsing.py

# 直接使用 uv 或 python
uv run pytest tests/unit_tests/ -v          # 使用 uv（推荐）
python -m pytest tests/unit_tests/ -v       # 使用 python
```

## 🎨 UI 组件

天气 agent 生成的 UI 组件包含：
- 📍 城市名称
- 🌡️ 温度信息
- ☁️ 天气状况
- 💧 湿度数据
- 💨 风速信息
- 📝 天气描述

前端可以使用 `LoadExternalComponent` 渲染：
```tsx
import { LoadExternalComponent } from "@langchain/langgraph-sdk/react-ui";

<LoadExternalComponent 
  stream={thread} 
  message={ui} 
  fallback={<div>Loading...</div>} 
/>
```

## 📊 支持的城市

当前支持以下城市的天气查询：
- 北京 - 晴天，22°C
- 上海 - 多云，18°C  
- 深圳 - 小雨，26°C
- 广州 - 阴天，24°C
- 杭州 - 晴天，20°C

## 🔧 配置

### LangGraph 配置 (langgraph.json)
```json
{
  "graphs": {
    "agent": "./src/agent/graph.py:graph"
  },
  "ui": {
    "agent": "./src/agent/ui.tsx"
  }
}
```

### 环境配置
复制 `.env.example` 到 `.env` 并配置相关参数（可选）。

## 📚 详细文档

- [Generative UI 功能指南](docs/features/generative-ui-guide.md) - 详细的 UI 组件开发指南
- [消息解析功能](docs/features/message-parsing.md) - 自然语言处理实现详解
- [测试结构文档](docs/testing/test-structure.md) - 测试套件结构和使用说明

## 🛠️ 开发指南

### 添加新城市
1. 在 `src/agent/graph.py` 的 `WEATHER_DATA` 中添加城市数据
2. 更新测试用例
3. 运行测试验证

### 扩展解析模式
1. 在 `extract_city_from_message()` 函数中添加新的正则表达式模式
2. 添加对应的单元测试
3. 验证功能正确性

### 自定义 UI 组件
1. 修改 `src/agent/ui.tsx` 中的 `WeatherComponent`
2. 使用 Tailwind CSS 进行样式设计
3. 确保与后端数据结构匹配

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 运行测试确保通过
5. 提交 Pull Request

## 📄 许可证

MIT License - 详见 LICENSE 文件

## 🙋‍♂️ 支持

如有问题或建议，请：
1. 查看文档目录中的详细指南
2. 运行示例脚本了解用法
3. 查看测试用例作为参考
4. 提交 Issue 反馈问题

---

**开始使用**: `uv run python examples/weather_demo.py` 🚀
