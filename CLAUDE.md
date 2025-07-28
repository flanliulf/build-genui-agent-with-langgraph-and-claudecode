# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Weather Agent with Generative UI** project built on LangGraph, demonstrating intelligent natural language processing for weather queries with dynamic React component generation. The project showcases message-driven architecture without LLM dependencies.

### Core Architecture

- **Entry Point**: `src/agent/graph.py` - Main weather agent logic with message parsing
- **UI Component**: `src/agent/ui.tsx` - React weather card with Tailwind CSS
- **Graph Structure**: Single-node StateGraph with weather_node processing
- **State Management**: Uses `AgentState` with messages and UI component data
- **Message Processing**: Extracts city information from natural language queries

### Key Components

1. **Weather Agent** (`src/agent/graph.py`):
   - `extract_city_from_message()`: Natural language city extraction with regex patterns
   - `weather_node()`: Core processing function with UI generation
   - `AgentState` class: Messages and UI data flow structure
   - `WEATHER_DATA`: Static weather dataset for 5 Chinese cities

2. **UI Components**:
   - `src/agent/ui.tsx`: React weather card component
   - Tailwind CSS responsive design
   - Dynamic data binding from backend

3. **Configuration Files**:
   - `langgraph.json`: Graph and UI component registration
   - `pyproject.toml`: Python 3.11+ requirements, dependencies, dev tools
   - `.python-version`: Python version pinning for uv

## Development Workflow

### Project Memory Rules
- **Branch-First Development**: Create feature branches before coding new requirements
- **Code Review**: Complete testing before merging to main
- **Merge Reminders**: Always remind to merge completed features to main branch

### Setup and Installation
```bash
# Using uv (recommended)
uv sync --group dev

# Or using pip (fallback)
pip install -e . "langgraph-cli[inmem]"

# Python version requirement
uv python pin 3.11
```

### Running the Application
```bash
# Start LangGraph development server (requires Python 3.11+)
uv run langgraph dev

# Run demo script
uv run python examples/weather_demo.py
```

### Testing (All 34 tests pass)
```bash
# Makefile with intelligent uv/python selection
make test                    # Run all unit tests
make integration_tests       # Run integration tests
make test_watch             # Watch mode testing

# Direct commands
uv run pytest tests/unit_tests/ -v          # Using uv (preferred)
python -m pytest tests/unit_tests/ -v       # Using python (fallback)
```

### Code Quality
```bash
# Intelligent tool selection (uv preferred, python fallback)
make format                  # Code formatting
make lint                    # Linting and type checking
make help                    # Show all available commands
```

## Project Features

### Natural Language Processing
- **Supported Query Patterns**:
  - Direct: "北京天气", "上海的温度"
  - Inquiry: "北京的天气怎么样？", "上海天气如何？"
  - Query: "查询北京天气", "了解上海天气"
  - Temporal: "今天北京天气", "明天上海的温度"

### Supported Cities
- 北京 (Beijing) - Sunny, 22°C
- 上海 (Shanghai) - Cloudy, 18°C
- 深圳 (Shenzhen) - Light rain, 26°C
- 广州 (Guangzhou) - Overcast, 24°C
- 杭州 (Hangzhou) - Sunny, 20°C

### Technical Highlights
- **Message-Driven Architecture**: Extracts city from user messages, not config
- **No LLM Dependencies**: Uses static data for fast response
- **Error Handling**: Graceful fallback for unsupported cities
- **Responsive UI**: Tailwind CSS mobile-first design
- **Type Safety**: Full TypeScript and Python type definitions

## File Structure
```
src/agent/
├── graph.py          # Main agent logic and message processing
├── ui.tsx           # React weather component
└── __init__.py      # Module initialization

tests/
├── unit_tests/      # 34 unit tests (100% pass rate)
│   ├── test_message_parsing.py     # Natural language tests (10 tests)
│   ├── test_weather_node.py        # Agent functionality tests (8 tests)
│   ├── test_ui_data.py             # UI component data tests (12 tests)
│   └── test_configuration.py       # Configuration tests (4 tests)
└── integration_tests/              # End-to-end tests

docs/
├── development/     # Development documentation
│   ├── ARCHITECTURE.md  # Technical architecture
│   └── README.md        # Development guide
├── features/        # Feature documentation
├── testing/         # Testing guides
└── README.md        # Documentation index

examples/
└── weather_demo.py  # Complete functionality demo
```

## Development Commands Reference

### Makefile Intelligence
The project uses an intelligent Makefile that automatically selects tools:
```makefile
PYTHON_CMD := $(shell command -v uv >/dev/null 2>&1 && echo "uv run" || echo "python -m")
```

### Key Configuration Details

#### LangGraph Configuration (`langgraph.json`)
- Graph entry point: `./src/agent/graph.py:graph`
- UI component: `./src/agent/ui.tsx`
- Python 3.11+ requirement for dev server

#### Python Configuration (`pyproject.toml`)
- **Base Dependencies**: `langgraph>=0.2.6`, `langchain-core>=0.3.0`
- **Dev Dependencies**: `pytest>=8.3.5`, `mypy>=1.13.0`, `ruff>=0.8.2`
- **Python Requirement**: `>=3.11` (for LangGraph dev server)

## Testing Strategy

### Test Coverage (34/34 passing)
- **Message Parsing**: 10 tests covering all query patterns and natural language expressions
- **Weather Node**: 8 tests for async functionality, city extraction, and error handling
- **UI Data**: 12 tests for component data structure validation and windSpeed field consistency
- **Configuration**: 4 tests for AgentState structure and graph compilation

### Test Environment
- **Framework**: pytest with anyio for async support
- **Fixtures**: Comprehensive state and configuration fixtures
- **Context Handling**: Graceful LangGraph context management for testing

## Extending the Agent

1. **Add New Cities**: Update `WEATHER_DATA` in `graph.py`
2. **Extend Query Patterns**: Add regex patterns to `extract_city_from_message()`
3. **Enhance UI**: Modify `ui.tsx` with additional weather data fields
4. **Add New Nodes**: Extend graph with additional processing nodes

## Error Handling
- **Unsupported Cities**: Graceful fallback to default weather data (Beijing)
- **Missing Context**: UI message push handles missing LangGraph context with try-catch
- **Network Issues**: Static data ensures reliable operation without external APIs
- **Test Environment**: Proper async context management for unit tests with RuntimeError handling
- **Field Consistency**: Unified windSpeed field name across frontend and backend