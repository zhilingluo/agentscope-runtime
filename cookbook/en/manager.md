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

# Manager Module

The manager module provides a unified interface for registering, starting, and stopping multiple services (e.g., session history service, memory service, and sandbox service) with automatic lifecycle management.

## Overview

- **ServiceManager**: base class for common lifecycle and access APIs, which manages services
- **ContextManager**: specializes in context services like `SessionHistoryService` and `MemoryService`
- **EnvironmentManager**: specializes in environment/tooling via `SandboxService`

### Required Service Interface

Services should be async context-manageable and expose a `health()` method.

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

### Service Lifecycle Management

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

### Service Access Methods

Within the async context:

- Attribute: `services.service1`
- Item: `services["service1"]`
- Getter: `services.get("service1", default=None)`
- Existence: `services.has_service("service1")`
- List names: `services.list_services()`
- Dict of all: `services.all_services`

## Context Manager

`ContextManager` wires default context services(`memory_service`, `session_history_service`) and exposes context composition method driven by `ContextComposer`.


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
        # default services available
        _ = manager.memory_service
```

For details, see {doc}`context_manager`.


## Environment Manager

`EnvironmentManager` wires `SandboxService` and exposes environment operations: `connect_sandbox`, `release_sandbox`

```{code-cell}
from agentscope_runtime.engine.services.environment_manager import (
    EnvironmentManager,
    create_environment_manager,
)
from agentscope_runtime.engine.services.sandbox_service import SandboxService

async def use_environment_manager():
    env_manager = EnvironmentManager(sandbox_service= SandboxService())
    async with env_manager as manager:
        # connect sandboxes/tools per session+user
        boxes = manager.connect_sandbox(
            session_id="s1",
            user_id="u1",
            env_types=[],
            tools=[],
        )
        manager.release_sandbox(session_id="s1", user_id="u1")
```

For details, see {doc}`environment_manager`.

