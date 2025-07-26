# CLAUDE_ZH.md

此文件为 Claude Code (claude.ai/code) 提供在此代码库中工作的中文指导。

## 项目概述

这是一个基于 LangGraph 构建的**天气 Agent 生成式 UI** 项目，展示了智能自然语言处理天气查询与动态 React 组件生成。项目采用消息驱动架构，无需 LLM 依赖。

### 核心架构

- **入口点**: `src/agent/graph.py` - 主要天气 agent 逻辑和消息解析
- **UI 组件**: `src/agent/ui.tsx` - 使用 Tailwind CSS 的 React 天气卡片
- **图结构**: 单节点 StateGraph，包含 weather_node 处理
- **状态管理**: 使用包含消息和 UI 组件数据的 `State`
- **消息处理**: 从自然语言查询中提取城市信息

### 关键组件

1. **天气 Agent** (`src/agent/graph.py`):
   - `extract_city_from_message()`: 使用正则表达式进行自然语言城市提取
   - `weather_node()`: 核心处理函数，包含 UI 生成
   - `State` 类: 消息和 UI 数据流结构
   - `WEATHER_DATA`: 5个中国城市的静态天气数据集

2. **UI 组件**:
   - `src/agent/ui.tsx`: React 天气卡片组件
   - Tailwind CSS 响应式设计
   - 后端数据动态绑定

3. **配置文件**:
   - `langgraph.json`: 图和 UI 组件注册
   - `pyproject.toml`: Python 3.11+ 要求、依赖、开发工具
   - `.python-version`: uv 的 Python 版本固定

## 开发工作流

### 项目记忆规则
- **分支优先开发**: 在编写新需求代码前创建功能分支
- **代码审查**: 在合并到主分支前完成测试
- **合并提醒**: 始终提醒将完成的功能合并到主分支

### 安装和设置
```bash
# 使用 uv（推荐）
uv sync --group dev

# 或使用 pip（备用）
pip install -e . "langgraph-cli[inmem]"

# Python 版本要求
uv python pin 3.11
```

### 运行应用程序
```bash
# 启动 LangGraph 开发服务器（需要 Python 3.11+）
uv run langgraph dev

# 运行演示脚本
uv run python examples/weather_demo.py
```

### 测试（35个测试全部通过）
```bash
# 智能 uv/python 选择的 Makefile
make test                    # 运行所有单元测试
make integration_tests       # 运行集成测试
make test_watch             # 监视模式测试

# 直接命令
uv run pytest tests/unit_tests/ -v          # 使用 uv（首选）
python -m pytest tests/unit_tests/ -v       # 使用 python（备用）
```

### 代码质量
```bash
# 智能工具选择（uv 优先，python 备用）
make format                  # 代码格式化
make lint                    # 代码检查和类型检查
make help                    # 显示所有可用命令
```

## 项目特性

### 自然语言处理
- **支持的查询模式**:
  - 直接式: "北京天气", "上海的温度"
  - 询问式: "北京的天气怎么样？", "上海天气如何？"
  - 查询式: "查询北京天气", "了解上海天气"
  - 时间式: "今天北京天气", "明天上海的温度"

### 支持的城市
- 北京 - 晴天，22°C
- 上海 - 多云，18°C
- 深圳 - 小雨，26°C
- 广州 - 阴天，24°C
- 杭州 - 晴天，20°C

### 技术亮点
- **消息驱动架构**: 从用户消息提取城市，而非配置
- **无 LLM 依赖**: 使用静态数据快速响应
- **错误处理**: 对不支持城市的优雅回退
- **响应式 UI**: Tailwind CSS 移动优先设计
- **类型安全**: 完整的 TypeScript 和 Python 类型定义

## 文件结构
```
src/agent/
├── graph.py          # 主要 agent 逻辑和消息处理
├── ui.tsx           # React 天气组件
└── __init__.py      # 模块初始化

tests/
├── unit_tests/      # 35个单元测试（100%通过率）
│   ├── test_message_parsing.py     # 自然语言测试
│   ├── test_weather_node.py        # Agent 功能测试
│   ├── test_ui_data.py             # UI 组件数据测试
│   └── test_configuration.py       # 配置测试
└── integration_tests/              # 端到端测试

docs/
├── features/        # 功能文档
├── testing/         # 测试指南
└── README.md        # 文档索引

examples/
└── weather_demo.py  # 完整功能演示
```

## 开发命令参考

### Makefile 智能化
项目使用智能 Makefile 自动选择工具：
```makefile
PYTHON_CMD := $(shell command -v uv >/dev/null 2>&1 && echo "uv run" || echo "python -m")
```

### 关键配置详情

#### LangGraph 配置 (`langgraph.json`)
- 图入口点: `./src/agent/graph.py:graph`
- UI 组件: `./src/agent/ui.tsx`
- 开发服务器需要 Python 3.11+

#### Python 配置 (`pyproject.toml`)
- **基础依赖**: `langgraph>=0.2.6`, `langchain-core>=0.3.0`
- **开发依赖**: `pytest>=8.3.5`, `mypy>=1.13.0`, `ruff>=0.8.2`
- **Python 要求**: `>=3.11`（LangGraph 开发服务器需要）

## 测试策略

### 测试覆盖（35/35通过）
- **消息解析**: 10个测试，覆盖所有查询模式
- **天气节点**: 8个测试，用于异步功能和错误处理
- **UI 数据**: 12个测试，用于组件数据结构验证
- **配置**: 5个测试，用于图结构和设置

### 测试环境
- **框架**: pytest 配合 anyio 进行异步支持
- **Fixtures**: 全面的状态和配置 fixtures
- **上下文处理**: 测试的优雅 LangGraph 上下文管理

## 扩展 Agent

1. **添加新城市**: 更新 `graph.py` 中的 `WEATHER_DATA`
2. **扩展查询模式**: 向 `extract_city_from_message()` 添加正则表达式模式
3. **增强 UI**: 修改 `ui.tsx` 添加更多天气数据字段
4. **添加新节点**: 使用额外的处理节点扩展图

## 错误处理
- **不支持的城市**: 优雅回退到随机天气数据
- **缺失上下文**: UI 消息推送处理缺失的 LangGraph 上下文
- **网络问题**: 静态数据确保可靠运行
- **测试环境**: 单元测试的正确异步上下文管理

## 历史开发记录

### 主要开发阶段
1. **初始实现**: 创建基础天气 Agent 和 UI 组件
2. **架构重构**: 从配置驱动改为消息驱动架构
3. **测试完善**: 实现 100% 测试通过率（35个测试）
4. **工具优化**: 实现 uv 优先的智能构建系统
5. **文档完善**: 创建完整的文档结构

### 关键技术决策
- **消息解析**: 使用正则表达式而非 LLM 进行城市提取
- **UI 生成**: LangGraph push_ui_message 动态生成 React 组件
- **测试策略**: 简化 mock，专注核心功能测试
- **开发工具**: uv 优先，python 备用的智能选择

### 当前状态
- ✅ 完整功能实现
- ✅ 100% 测试通过
- ✅ 完整文档
- ✅ 智能构建系统
- 🔄 等待依赖下载完成启动开发服务器