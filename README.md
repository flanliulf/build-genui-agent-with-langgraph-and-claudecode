# Weather Agent with Generative UI

基于 LangGraph 构建的智能天气 Agent，具备 Generative UI 功能，支持自然语言交互和动态 React 组件生成。

## 🌟 核心特性

- ✅ **智能自然语言处理** - 优化的两层城市提取算法，支持复杂自然语言表达
- ✅ **动态 UI 生成** - 后端动态生成带动画效果的 React 天气卡片组件
- ✅ **多种表达支持** - 支持直接查询、询问模式、查询模式、时间模式等
- ✅ **无 LLM 依赖** - 使用静态数据和正则表达式，响应速度快
- ✅ **响应式设计** - 现代化UI设计，支持移动端适配
- ✅ **完整测试覆盖** - 34个单元测试，100%通过率

## 🚀 快速开始

### 安装依赖
```bash
# 使用 uv（推荐）
uv sync --group dev

# 或使用 pip
pip install -e . "langgraph-cli[inmem]"

# Python 版本要求
uv python pin 3.11
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
from agent.graph import graph, AgentState

# 创建用户查询
state = AgentState(
    messages=[HumanMessage(content="北京天气怎么样？")],
    ui=[]
)

# 调用 agent
result = await graph.ainvoke(state, {"configurable": {}})

# 获取结果
ai_message = result["messages"][-1].content  # AI 回复 "☀️ 今天北京天气晴朗..."
ui_data = result["ui"][-1]["props"]          # UI 组件数据 {"city": "北京", ...}
```

## 🏗️ 项目结构

```
.
├── src/agent/                    # 核心 Agent 代码
│   ├── graph.py                  # 主要 graph 定义和天气节点
│   ├── ui.tsx                    # React UI 组件（带动画效果）
│   └── __init__.py               # 模块初始化
├── tests/                        # 测试套件
│   ├── unit_tests/               # 34个单元测试 (100% 通过)
│   │   ├── test_message_parsing.py    # 自然语言解析测试
│   │   ├── test_weather_node.py       # 天气节点功能测试
│   │   ├── test_ui_data.py            # UI组件数据测试
│   │   └── test_configuration.py      # 配置结构测试
│   └── integration_tests/        # 集成测试
├── examples/                     # 示例和演示
│   └── weather_demo.py           # 完整功能演示脚本
├── docs/                         # 项目文档
│   ├── development/              # 开发文档
│   │   ├── ARCHITECTURE.md       # 技术架构文档
│   │   └── README.md             # 开发文档导航
│   ├── features/                 # 功能文档
│   │   ├── generative-ui-guide.md
│   │   └── message-parsing.md
│   └── testing/                  # 测试文档
│       └── test-structure.md
├── CLAUDE.md                     # 项目指导文件
├── langgraph.json                # LangGraph 配置
├── pyproject.toml                # Python 项目配置
├── Makefile                      # 智能工具选择
└── .python-version               # Python 版本锁定 (3.11)
```

## 💬 支持的查询方式

### 🎯 优化的两层城市提取算法

**第一层：直接匹配（性能最优）**
- "北京天气" → 直接识别 "北京"
- "上海的温度" → 直接识别 "上海"  
- "深圳" → 直接识别 "深圳"

**第二层：正则表达式模式匹配（支持复杂自然语言）**

### 查询模式
- "查询北京的天气"
- "查看上海天气"
- "了解深圳的温度"
- "知道广州天气"

### 询问模式  
- "北京的天气怎么样？"
- "上海天气如何？"
- "深圳的温度怎样？"
- "广州天气怎么样？"

### 时间表达模式
- "今天北京天气"
- "明天上海的温度" 
- "现在深圳天气"

### 复杂自然语言表达
- "我想知道北京今天的天气情况"
- "请告诉我上海的天气预报"
- "能帮我查一下深圳的天气吗"

## 🧪 测试

### 📊 测试覆盖 (34/34 通过, 100%)
- **消息解析**: 10个测试 - 自然语言模式识别
- **天气节点**: 8个测试 - 异步功能和错误处理  
- **UI数据**: 12个测试 - 组件数据结构验证
- **配置**: 4个测试 - 图结构和设置

### 🔧 运行测试
```bash
# 使用 make 命令（推荐，自动优先使用 uv）
make test                    # 运行所有单元测试
make integration_tests       # 运行集成测试
make test_watch             # 监视模式运行测试

# 代码质量检查
make format                  # 代码格式化
make lint                    # 代码检查

# 直接使用 uv 或 python
uv run pytest tests/unit_tests/ -v          # 使用 uv（推荐）
python -m pytest tests/unit_tests/ -v       # 使用 python
```

## 🎨 UI 组件

### 🎭 动态天气卡片组件
天气 agent 生成的 UI 组件包含：
- 📍 **城市名称** - 支持的5个中国城市
- 🌡️ **温度信息** - 精准的温度显示 (如：22°C)
- ☁️ **天气状况** - 动态图标映射 (☀️晴天 ⛅多云 🌧️小雨)
- 💧 **湿度数据** - 百分比显示 (如：45%)
- 💨 **风速信息** - 统一windSpeed字段 (如：3km/h)
- 📝 **天气描述** - 贴心的生活建议

### ✨ UI 特性
- **动画效果**: 卡片入场动画、图标弹跳、闪烁特效
- **响应式设计**: 移动端适配，自动缩放
- **背景渐变**: 根据天气状况动态调整背景色
- **类型安全**: 完整的TypeScript接口定义

### 📱 前端集成
```tsx
import { LoadExternalComponent } from "@langchain/langgraph-sdk/react-ui";

<LoadExternalComponent 
  stream={thread} 
  message={ui} 
  fallback={<div>Loading weather...</div>} 
/>
```

### 🔧 数据结构
```typescript
interface WeatherProps {
  city: string;           // 城市名称
  temperature: string;    // 温度 "22°C"
  condition: string;      // 天气状况 "晴天"
  humidity: string;       // 湿度 "45%"
  windSpeed: string;      // 风速 "3km/h" 
  description: string;    // 详细描述
}
```

## 📊 支持的城市

当前支持以下**5个中国城市**的天气查询：

| 城市 | 天气状况 | 温度 | 湿度 | 风速 | 特色描述 |
|------|----------|------|------|------|----------|
| 北京 | 晴天 ☀️ | 22°C | 45% | 3km/h | 天气晴朗，温度适宜，适合外出活动 |
| 上海 | 多云 ⛅ | 18°C | 68% | 5km/h | 多云转阴，温度稍凉，建议增添衣物 |
| 深圳 | 小雨 🌧️ | 26°C | 78% | 7km/h | 有小雨，湿度较高，出门记得带伞 |
| 广州 | 阴天 ☁️ | 24°C | 72% | 4km/h | 阴天，温度舒适，适合室内活动 |
| 杭州 | 晴天 ☀️ | 20°C | 55% | 6km/h | 晴空万里，温度宜人，是游览的好天气 |

### 🔄 容错处理
- **不支持的城市**: 自动回退到默认城市（北京）
- **无城市指定**: 默认显示北京天气
- **多城市同时出现**: 返回消息中最先出现的城市

## 🔧 技术配置

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

### Python 配置 (pyproject.toml)
```toml
[project]
requires-python = ">=3.11"
dependencies = [
    "langgraph>=0.2.6", 
    "langchain-core>=0.3.0"
]

[tool.uv.dev-dependencies]
pytest = ">=8.3.5"
mypy = ">=1.13.0"
ruff = ">=0.8.2"
```

### 智能 Makefile
```makefile
PYTHON_CMD := $(shell command -v uv >/dev/null 2>&1 && echo "uv run" || echo "python -m")
```
自动选择 `uv` 或 `python` 命令，优先使用性能更好的 `uv`。

## 📚 详细文档

### 🏗️ 开发文档
- [技术架构文档](docs/development/ARCHITECTURE.md) - 完整的系统架构和技术实现详解

### ✨ 功能文档  
- [Generative UI 功能指南](docs/features/generative-ui-guide.md) - 详细的 UI 组件开发指南
- [消息解析功能](docs/features/message-parsing.md) - 自然语言处理实现详解

### 🧪 测试文档
- [测试结构文档](docs/testing/test-structure.md) - 测试套件结构和使用说明

## 🛠️ 开发指南

### 🏙️ 添加新城市
1. 在 `src/agent/graph.py` 的 `WEATHER_DATA` 数组中添加城市数据
2. 确保包含所有必需字段：`city`, `temperature`, `condition`, `humidity`, `windSpeed`, `description`
3. 更新相关测试用例（`test_ui_data.py`, `test_weather_node.py`）
4. 运行 `make test` 验证所有测试通过

### 🧠 扩展自然语言模式
1. 在 `extract_city_from_message()` 函数的 `basic_patterns` 数组中添加新的正则表达式
2. 在 `test_message_parsing.py` 中添加对应的测试用例
3. 使用 `uv run python examples/weather_demo.py` 验证功能
4. 确保向后兼容性，不破坏现有模式

### 🎨 自定义 UI 组件
1. 修改 `src/agent/ui.tsx` 中的 `WeatherComponent`
2. 更新 `WeatherProps` 接口定义（如需要）
3. 使用内联样式或扩展现有动画效果
4. 保持与后端 `WeatherOutput` 数据结构的一致性
5. 在移动端测试响应式布局

### 📊 数据一致性检查
```bash
# 检查前后端数据结构一致性
make test  # UI数据测试会验证字段匹配
```

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
