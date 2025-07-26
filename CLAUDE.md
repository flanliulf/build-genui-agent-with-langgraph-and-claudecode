# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a LangGraph-based generative UI agent project using Python. The project follows LangGraph's template structure for building conversational agents with visual debugging capabilities via LangGraph Studio.

### Core Architecture

- **Entry Point**: `src/agent/graph.py` - Contains the main graph definition and core agent logic
- **Graph Structure**: Single-node StateGraph with configurable parameters
- **State Management**: Uses `State` dataclass to define input/output structure
- **Configuration**: `Configuration` TypedDict for runtime parameters
- **Graph Registration**: Registered in `langgraph.json` as "agent" pointing to `graph` object

### Key Components

1. **Graph Definition** (`src/agent/graph.py`):
   - `State` class: Defines the data structure flowing through the graph
   - `Configuration` class: Runtime configurable parameters
   - `call_model()` function: Core processing node
   - `graph` object: Compiled StateGraph instance

2. **Configuration Files**:
   - `langgraph.json`: Graph registration and LangGraph Server configuration
   - `pyproject.toml`: Python project metadata, dependencies, and tool configurations
   - `.env`: Environment variables (copy from `.env.example`)

## Development Commands

### Setup and Installation
```bash
# Install dependencies and LangGraph CLI
pip install -e . "langgraph-cli[inmem]"

# Setup environment file (optional)
cp .env.example .env
```

### Running the Application
```bash
# Start LangGraph development server
langgraph dev
```

### Testing
```bash
# Run unit tests
make test

# Run specific test file
make test TEST_FILE=tests/unit_tests/test_configuration.py

# Run integration tests
make integration_tests

# Run tests in watch mode
make test_watch
```

### Code Quality
```bash
# Format code
make format

# Run linting
make lint

# Run type checking (included in lint)
python -m mypy --strict src/
```

## Key Configuration Details

### LangGraph Configuration (`langgraph.json`)
- Graph entry point: `./src/agent/graph.py:graph`
- Environment file: `.env`
- Image distribution: `wolfi`

### Python Configuration (`pyproject.toml`)
- **Dependencies**: `langgraph>=0.2.6`, `python-dotenv>=1.0.1`
- **Dev Dependencies**: `mypy>=1.11.1`, `ruff>=0.6.1`
- **Linting**: Ruff with pycodestyle, pyflakes, isort, pydocstyle
- **Type Checking**: MyPy in strict mode

## Extending the Agent

1. **Modify State Structure**: Update the `State` dataclass in `graph.py` to add new fields
2. **Add Configuration Parameters**: Extend `Configuration` TypedDict for runtime options
3. **Implement New Nodes**: Add processing functions and register them in the graph
4. **Update Graph Flow**: Use `.add_node()` and `.add_edge()` to modify the execution flow

## Testing Strategy

- **Unit Tests**: Located in `tests/unit_tests/`
- **Integration Tests**: Located in `tests/integration_tests/`
- **Test Configuration**: Uses `pytest` with `anyio` backend for async testing
- **LangSmith Integration**: Tests marked with `@pytest.mark.langsmith` for tracing