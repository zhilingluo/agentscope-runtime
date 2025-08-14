---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.5
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# 管理器模块（Manager Module）

该模块提供了一个统一的接口，用于注册、启动和停止多个服务（例如会话历史服务、记忆服务和沙箱服务），并具有自动生命周期管理功能。

## 概览

- **ServiceManager**：服务管理的基类，提供通用的生命周期和访问API
- **ContextManager**：专注于上下文相关服务（如 `SessionHistoryService` 与 `MemoryService`）
- **EnvironmentManager**：专注于环境/工具相关能力（通过 `SandboxService`）

### 服务接口要求

服务应支持异步上下文管理，并暴露 `health()` 方法。

```{code-cell}
from agentscope_runtime.engine.services.base import ServiceWithLifecycleManager

class MockService(ServiceWithLifecycleManager):
    def __init__(self, name: str):
        self.name = name
        self.started = False
        self.stopped = False

    async def start(self):
        self.started = True

    async def stop(self):
        self.stopped = True

    async def health(self) -> bool:
        return self.started and not self.stopped
```

### 服务生命周期管理

```{code-cell}
from agentscope_runtime.engine.services.manager import ServiceManager

class MyServiceManager(ServiceManager):
    def _register_default_services(self):
        pass

manager = MyServiceManager()
manager.register(MockService, name="service1")
manager.register(MockService, name="service2")

async def run():
    async with manager as services:
        names = services.list_services()
        health = await services.health_check()
        print(names, health)
```

### 服务访问方式

在异步上下文内可通过以下方式访问服务：

- 属性访问：`services.service1`
- 索引访问：`services["service1"]`
- 获取方法：`services.get("service1", default=None)`
- 存在性检查：`services.has_service("service1")`
- 列出名称：`services.list_services()`
- 获取所有服务：`services.all_services`

## 上下文管理器（Context Manager）

`ContextManager` 默认装配上下文服务（`memory_service`、`session_history_service`），并通过 `ContextComposer` 提供上下文组合方法。

```{code-cell}
from agentscope_runtime.engine.services.context_manager import (
    ContextManager,
    create_context_manager,
)
from agentscope_runtime.engine.services.memory_service import InMemoryMemoryService


async def use_context_manager():
    async with create_context_manager(
        memory_service=InMemoryMemoryService()
    ) as manager:
        # 默认服务可用
        _ = manager.memory_service
```

更多细节见 {doc}`context_manager`。

## 环境管理器（Environment Manager）

`EnvironmentManager` 装配 `SandboxService` 并暴露环境操作：`connect_sandbox`、`release_sandbox`。

```{code-cell}
from agentscope_runtime.engine.services.environment_manager import (
    EnvironmentManager,
    create_environment_manager,
)
from agentscope_runtime.engine.services.sandbox_service import SandboxService

async def use_environment_manager():
    env_manager = EnvironmentManager(sandbox_service=SandboxService())
    async with env_manager as manager:
        # 按会话+用户连接沙箱/工具
        boxes = manager.connect_sandbox(
            session_id="s1",
            user_id="u1",
            env_types=[],
            tools=[],
        )
        manager.release_sandbox(session_id="s1", user_id="u1")
```

更多细节见 {doc}`environment_manager`。

