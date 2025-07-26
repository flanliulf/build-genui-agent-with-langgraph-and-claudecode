# 天气 Agent Generative UI 示例

这个项目展示了如何使用 LangGraph 创建具有 Generative UI 功能的天气 agent。

## 🏗️ 架构概览

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   后端 Agent    │    │  LangGraph      │    │   前端 React    │
│   (graph.py)    │────│   Platform      │────│   (ui.tsx)      │
│                 │    │                 │    │                 │
│ weather_node()  │    │ push_ui_message │    │ WeatherComponent│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📋 功能特性

- ✅ **无 LLM 依赖**：使用静态天气数据，无需调用 LLM API
- ✅ **动态 UI 组件**：后端动态生成 React 组件数据
- ✅ **响应式设计**：使用 Tailwind CSS 创建美观的天气卡片
- ✅ **配置灵活**：支持指定默认城市或随机选择
- ✅ **类型安全**：完整的 Python 和 TypeScript 类型定义

## 🗂️ 文件结构

```
src/agent/
├── graph.py          # 后端 agent 逻辑和天气节点
├── ui.tsx           # React UI 组件（天气卡片）
└── __init__.py      # 模块初始化

配置文件:
├── langgraph.json   # LangGraph 平台配置
├── pyproject.toml   # Python 项目配置
└── example_client.py # 使用示例

测试文件:
├── test_weather.py        # 基本功能测试
├── test_random_weather.py # 随机功能测试
└── example_client.py      # 完整示例
```

## 🚀 快速开始

### 1. 安装依赖

```bash
# 使用 uv（推荐）
uv sync

# 或使用 pip
pip install -e .
```

### 2. 运行测试

```bash
# 基本功能测试
python test_weather.py

# 随机功能测试  
python test_random_weather.py

# 完整示例
python example_client.py
```

### 3. 启动开发服务器

```bash
# 启动 LangGraph 开发服务器
uv run langgraph dev
```

## 💻 代码说明

### 后端 Agent (graph.py)

```python
class State(TypedDict):
    """支持消息和 UI 的状态"""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    ui: Annotated[Sequence[AnyUIMessage], ui_message_reducer]

async def weather_node(state: State, config: RunnableConfig):
    """天气节点：返回静态天气数据并创建 UI 组件"""
    weather_data = random.choice(WEATHER_DATA)
    message = AIMessage(content=f"🌤️ {weather_data['description']}")
    
    # 推送 UI 组件数据到前端
    push_ui_message("weather", weather_data, message=message)
    
    return {"messages": [message]}
```

### 前端组件 (ui.tsx)

```typescript
const WeatherComponent: React.FC<WeatherProps> = ({
  city, temperature, condition, humidity, wind, description
}) => {
  const weatherIcon = getWeatherIcon(condition);
  const gradientClass = getBackgroundGradient(condition);

  return (
    <div className={`bg-gradient-to-br ${gradientClass} rounded-xl shadow-lg`}>
      {/* 天气卡片内容 */}
    </div>
  );
};
```

### 配置文件 (langgraph.json)

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

## 🎯 使用场景

### 1. 基本使用

```python
from src.agent.graph import graph, State

# 创建状态
state = State(messages=[], ui=[])

# 调用 agent
result = await graph.ainvoke(state, {"configurable": {}})

# 获取 UI 数据
ui_data = result['ui'][-1]['props']  # 天气数据
message = result['messages'][-1].content  # 消息内容
```

### 2. 指定城市

```python
config = {
    "configurable": {
        "default_city": "上海"
    }
}

result = await graph.ainvoke(state, config)
```

### 3. 前端集成

```tsx
import { useStream } from "@langchain/langgraph-sdk/react";
import { LoadExternalComponent } from "@langchain/langgraph-sdk/react-ui";

export default function Page() {
  const { thread, values } = useStream({
    apiUrl: "http://localhost:2024",
    assistantId: "agent",
  });

  return (
    <div>
      {thread.messages.map((message) => (
        <div key={message.id}>
          {message.content}
          {values.ui
            ?.filter((ui) => ui.metadata?.message_id === message.id)
            .map((ui) => (
              <LoadExternalComponent key={ui.id} stream={thread} message={ui} />
            ))}
        </div>
      ))}
    </div>
  );
}
```

## 🌟 核心概念

### 1. Generative UI
- 后端根据数据动态生成 UI 组件
- 前端通过 `LoadExternalComponent` 渲染组件
- 实现了 AI 与 UI 的深度结合

### 2. 状态管理
- `messages`: 存储对话消息
- `ui`: 存储 UI 组件数据
- 使用 LangGraph 的 reducer 自动管理状态

### 3. 组件通信
- `push_ui_message()` 从后端发送组件数据
- 前端通过 stream 接收实时更新
- 支持组件属性和消息关联

## 🔧 自定义扩展

### 1. 添加新的天气数据

```python
WEATHER_DATA.append({
    "city": "成都",
    "temperature": "19°C",
    "condition": "多云",
    "humidity": "65%",
    "wind": "4km/h",
    "description": "成都今天多云，温度舒适。"
})
```

### 2. 扩展 UI 组件

```typescript
// 添加新属性
interface WeatherProps {
  // ... 现有属性
  airQuality?: string;
  uvIndex?: string;
}

// 在组件中显示
<div className="grid grid-cols-3 gap-2">
  <div>湿度: {humidity}</div>
  <div>风速: {wind}</div>
  <div>空气质量: {airQuality}</div>
</div>
```

### 3. 添加交互功能

```typescript
import { useStreamContext } from "@langchain/langgraph-sdk/react-ui";

const WeatherComponent = (props) => {
  const { thread, submit } = useStreamContext();
  
  return (
    <div>
      {/* 天气显示 */}
      <button
        onClick={() => {
          submit({ messages: [{ type: "human", content: "刷新天气" }] });
        }}
      >
        🔄 刷新天气
      </button>
    </div>
  );
};
```

## ✅ 测试结果

所有测试都已通过：
- ✅ 基本功能测试
- ✅ 随机城市选择
- ✅ 指定城市功能
- ✅ 配置参数处理
- ✅ UI 组件数据生成
- ✅ 消息和 UI 状态管理

## 📚 参考资料

- [LangGraph Generative UI 文档](https://langchain-ai.github.io/langgraph/how-tos/generative-ui-react/)
- [LangGraph Platform 文档](https://langchain-ai.github.io/langgraph/concepts/langgraph_platform/)
- [React UI SDK 参考](https://langchain-ai.github.io/langgraph/reference/sdk/js_ts_sdk_ref/)