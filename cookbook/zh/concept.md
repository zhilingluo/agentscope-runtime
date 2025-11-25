# 概念

本章介绍了AgentScope Runtime的核心概念，它提供了两种主要的使用模式：

- **智能体部署**: 使用引擎模块进行功能完整的智能体部署，包括运行时编排、长短期记忆和生产就绪的服务
- **沙箱工具使用**: 独立使用沙箱模块，在您自己的应用程序中进行安全的工具执行和集成

## Engine模块概念

### 架构

AgentScope Runtime使用模块化架构，包含几个关键组件：

```{figure} ../_static/agent_architecture_zh.png
:alt: 智能体架构
:width: 75%
:align: center

智能体架构
```

- **Agent**：处理请求并生成响应的核心AI组件，在Runtime中，Agent的构建推荐使用AgentScope框架。
- **AgentApp**: 继承于 FastAPI App，作为应用入口，负责对外提供 API 接口、路由注册、配置加载，并将请求交由 Runner 调用执行
- **Runner**：在运行时编排智能体执行并管理部署。它处理智能体生命周期、会话管理、流式响应和服务部署。
- **Deployer**：将Runner部署为服务，提供健康检查、监控、生命周期管理、使用SSE的实时响应流式传输、错误处理、日志记录和优雅关闭。
- **Tool**: 提供即用型服务，比如RAG
- **Service**：提供智能体所需要的管理服务，比如记忆管理，沙箱管理等

### 关键组件

#### 1. Agent

`Agent` 是处理请求并生成响应的核心组件。它是一个抽象基类，定义了所有智能体类型的接口。开发者可以使用AgentScope开发需要的Agent。

#### 2. AgentApp

`AgentApp` 是 AgentScope Runtime 中的 **应用入口点**，继承自 `BaseApp`（一个扩展了 FastAPI 并可选集成 Celery 的基类），用于将 Agent 部署为可对外提供服务的 API 应用。

它的职责是：

- 初始化并绑定 **Agent** 和 **Runner**，将请求委托给运行时处理
- 提供标准化的 **HTTP API 接口**（含健康检查）
- 支持 **Server-Sent Events (SSE)** 以及标准 JSON 响应
- 允许注册中间件、任务队列（Celery）以及自定义路由
- 管理应用生命周期（支持 `before_start` / `after_finish` 钩子）

#### 3. Runner

`Runner` 类提供灵活且可扩展的运行时来编排智能体执行并提供部署功能。它管理：

- 通过 `init_handler` 和 `shutdown_handler` 管理智能体生命周期
- 通过 `query_handler` 处理请求
- 流式响应
- 通过 `deploy()` 方法进行服务部署

#### 4. Deployer

`Deployer`（实现为 `DeployManager`）提供生产级别的部署功能：

- 将Runner部署为服务
- 健康检查、监控和生命周期管理
- 使用SSE的实时响应流式传输
- 错误处理、日志记录和优雅关闭
- 支持多种部署模式（本地、容器化、Kubernetes等）

#### 5. Tool

Runtime提供三种工具接入方式
- 即用型工具，即由服务提供商提供的开箱即用的服务，比如RAG
- 工具沙箱，即运行在runtime里安全可控的工具，比如浏览器
- 自定义工具，即开发者自由定义自由部署的工具。


#### 6. Service

`Service`包含如下几种
- `state_service` 状态服务
- `memory_service` 智能体记忆服务
- `sandbox_service` 即沙箱服务
- `session_history_service` 即会话历史记录保存服务

## 沙箱模块概念

### 架构

沙箱模块为各种操作提供了一个**安全**且**隔离**的执行环境，包括MCP工具执行、浏览器自动化和文件系统操作。

系统支持多种沙箱类型，每种都针对特定用例进行了优化：

#### 1. BaseSandbox（基础沙箱）

- **用途**: 基本Python代码执行和shell命令
- **使用场景**: 基础工具执行和脚本编写的必需品
- **能力**: IPython环境、shell命令执行

#### 2. GuiSandbox （GUI沙箱）

- **用途**：具有安全访问控制的图形用户界面（GUI）交互与自动化
- **使用场景**：用户界面测试、桌面自动化、交互式工作流程
- **功能**：模拟用户输入（点击、键盘输入）、窗口管理、屏幕捕获等

#### 3. FilesystemSandbox（文件系统沙箱）

- **用途**: 具有安全访问控制的文件系统操作
- **使用场景**: 文件管理、文本处理和数据操作
- **能力**: 文件读写、目录操作、文件搜索和元数据等

#### 4. BrowserSandbox（浏览器沙箱）

- **用途**: Web浏览器自动化和控制
- **使用场景**: 网页抓取、UI测试和基于浏览器的交互
- **能力**: 页面导航、元素交互、截图捕获等

#### 5. TrainingSandbox（训练沙箱）

- **用途**:智能体训练和评估环境
- **使用场景**: 基准测试和性能评估
- **能力**: 环境分析、训练数据管理

