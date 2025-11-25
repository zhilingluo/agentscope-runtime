# Concepts

This chapter introduces the core concepts of AgentScope Runtime, which offers two primary usage patterns:

- **Agent Deployment**: Use the Engine Module for full-featured agent deployment with runtime orchestration, short- and long-term memory, and production-ready services
- **Sandboxed Tool Usage**: Use the Sandbox Module independently to execute tools securely and integrate them into your own applications

## Engine Module Concepts

### Architecture

AgentScope Runtime uses a modular architecture with several key components:

```{figure} ../_static/agent_architecture.png
:alt: Agent Architecture
:width: 75%
:align: center

Agent Architecture
```

- **Agent**: The core AI component that processes requests and generates responses; in the runtime we recommend building agents with the AgentScope framework.
- **AgentApp**: Inherits from FastAPI’s `App` and serves as the application entry point. It exposes APIs, registers routes, loads configurations, and delegates incoming requests to the Runner for execution.
- **Runner**: Orchestrates agent execution and manages deployment at runtime, handling agent lifecycle, session management, streaming responses, and service deployment.
- **Deployer**: Deploys the Runner as a service with health checks, monitoring, lifecycle management, SSE-based real-time streaming, error handling, logging, and graceful shutdown.
- **Tool**: Provides ready-to-use services, such as RAG.
- **Service**: Supplies management capabilities required by agents, such as memory management and sandbox management.

### Key Components

#### 1. Agent

The `Agent` is the core component that processes requests and generates responses. Many popular frameworks already provide agent abstractions, so the runtime does not introduce an additional `Agent` class—developers can build the required agents with AgentScope.

#### 2. AgentApp

`AgentApp` is the **application entry point** in AgentScope Runtime. It inherits from `BaseApp` (which extends FastAPI and can optionally integrate Celery) and is used to deploy an agent as an externally accessible API application.

Its responsibilities include:

- Initializing and binding the **Agent** and **Runner**, delegating requests to the runtime for processing
- Providing standardized **HTTP API endpoints** (including health checks)
- Supporting **Server-Sent Events (SSE)** as well as standard JSON responses
- Allowing registration of middlewares, task queues (Celery), and custom routes
- Managing the application lifecycle (supports `before_start` / `after_finish` hooks)

#### 3. Runner

The `Runner` class offers a flexible and extensible runtime that orchestrates agent execution and enables deployment. It manages:

- Agent lifecycle through `init_handler` and `shutdown_handler`
- Request processing through `query_handler`
- Streaming responses
- Service deployment via the `deploy()` method

#### 4. Deployer

The `Deployer` (implemented as `DeployManager`) provides production-grade deployment capabilities:

- Deploying the Runner as a service
- Health checks, monitoring, and lifecycle management
- SSE-based real-time response streaming
- Error handling, logging, and graceful shutdown
- Support for multiple deployment modes (local, containerized, Kubernetes, etc.)

#### 5. Tool

The runtime offers three patterns for integrating tools:

- Ready-to-use tools provided by service vendors, such as RAG
- Tool sandboxes that run securely within the runtime, such as a browser
- Custom tools that developers define and deploy themselves

#### 6. Service

`Service` includes the following components:

- `state_service` for state management
- `memory_service` for agent memory management
- `sandbox_service` for sandbox orchestration
- `session_history_service` for persisting session history

## Sandbox Module Concepts

### Architecture

The Sandbox Module provides a **secure** and **isolated** execution environment for MCP tools, browser automation, file system operations, and more.

The system supports multiple sandbox types, each optimized for specific use cases:

#### 1. BaseSandbox

- **Purpose**: Basic Python code execution and shell commands
- **Use Case**: Essential for fundamental tool execution and scripting
- **Capabilities**: IPython environment, shell command execution

#### 2. GuiSandbox

- **Purpose**: GUI interaction and automation with secure access control
- **Use Case**: User interface testing, desktop automation, and interactive workflows
- **Capabilities**: Simulated user input (clicks, keystrokes), window management, screen capture, etc.

#### 3. FilesystemSandbox

- **Purpose**: File system operations with secure access control
- **Use Case**: File management, text processing, and data manipulation
- **Capabilities**: File read/write, directory operations, file search, metadata access, etc.

#### 4. BrowserSandbox

- **Purpose**: Web browser automation and control
- **Use Case**: Web scraping, UI testing, and browser-based interactions
- **Capabilities**: Page navigation, element interaction, screenshot capture, etc.

#### 5. TrainingSandbox

- **Purpose**: Agent training and evaluation environments
- **Use Case**: Benchmarking and performance evaluation
- **Capabilities**: Environment analysis, training data management
