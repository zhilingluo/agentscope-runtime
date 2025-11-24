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

# Deep Dive into AgentApp

`AgentApp` is a complete agent service wrapper in **AgentScope Runtime**.
It can turn any agent that follows the interface into an API service, supporting:

- Streaming output (SSE)
- Health check endpoints
- Lifecycle hooks (`before_start` / `after_finish`)
- Celery asynchronous task queues
- Deployment to local or remote environments

Below is a detailed explanation of each feature with usage examples.

------

## Initialization and Basic Run

**Function**
Launch an HTTP API service containing the Agent, listening on the specified port, and providing the main processing endpoint (default `/process`).

**Example Usage**

```{code-cell}
from agentscope_runtime.engine import AgentApp
from agentscope_runtime.engine.agents.agentscope_agent import AgentScopeAgent
from agentscope.model import OpenAIChatModel
from agentscope.agent import ReActAgent

# Create Agent
agent = AgentScopeAgent(
    name="Friday",
    model=OpenAIChatModel(
        "gpt-4",
        api_key="YOUR_OPENAI_KEY",
    ),
    agent_config={"sys_prompt": "You are a helpful assistant."},
    agent_builder=ReActAgent,
)

# Create and run AgentApp
app = AgentApp(agent=agent, endpoint_path="/process", response_type="sse", stream=True)
app.run(host="0.0.0.0", port=8090)
```

------

## Streaming Output (SSE)

- **Function**
  Allows the client to receive generated results in real-time (suitable for chat, code generation, and other step-by-step output scenarios).

  **Key Parameters**

  - `response_type="sse"`
  - `stream=True`

**Client Example**

```bash
curl -N \
  -X POST "http://localhost:8090/process" \
  -H "Content-Type: application/json" \
  -d '{
    "input": [
      { "role": "user", "content": [{ "type": "text", "text": "Hello Friday" }] }
    ]
  }'
```

**Response Format**

```bash
data: {"sequence_number":0,"object":"response","status":"created", ... }
data: {"sequence_number":2,"object":"content","status":"in_progress","text":"Hello" }
data: {"sequence_number":3,"object":"content","status":"in_progress","text":" world!" }
data: {"sequence_number":4,"object":"message","status":"completed","text":"Hello world!" }
```

------

## Lifecycle Hooks

**Function**
Run custom logic before the application starts and after it stops — for example, loading models or closing connections.

### Method 1: Using Parameters

**Key Parameters**

- `before_start`: runs before the API service starts
- `after_finish`: runs when the API service is shutting down

**Example Usage**

```{code-cell}
async def init_resources(app, **kwargs):
    print("🚀 Service starting, initializing resources...")

async def cleanup_resources(app, **kwargs):
    print("🛑 Service stopping, releasing resources...")

app = AgentApp(
    agent=agent,
    before_start=init_resources,
    after_finish=cleanup_resources
)
```

### Method 2: Using Decorators (Recommended)

In addition to using parameters, you can also register lifecycle hooks using decorators, which is more flexible and intuitive:

**Example Usage**

```{code-cell}
from agentscope_runtime.engine import AgentApp
from agentscope_runtime.engine.services.agent_state import InMemoryStateService
from agentscope_runtime.engine.services.session_history import InMemorySessionHistoryService

app = AgentApp(
    app_name="Friday",
    app_description="A helpful assistant",
)

@app.init
async def init_func(self):
    """Initialize service resources"""
    self.state_service = InMemoryStateService()
    self.session_service = InMemorySessionHistoryService()
    
    await self.state_service.start()
    await self.session_service.start()
    print("✅ Service initialization complete")

@app.shutdown
async def shutdown_func(self):
    """Clean up service resources"""
    await self.state_service.stop()
    await self.session_service.stop()
    print("✅ Service resources cleaned up")
```

**Decorator Notes**

- `@app.init`: Register initialization hook, executed before service starts
- `@app.shutdown`: Register shutdown hook, executed when service stops
- Decorator functions receive `self` parameter, allowing access to the `AgentApp` instance
- Supports both sync and async functions

------

## Health Check Endpoints

**Function**
Automatically provides health probe endpoints for container or cluster deployment.

**Endpoints**

- `GET /health`: returns status and timestamp
- `GET /readiness`: checks readiness
- `GET /liveness`: checks liveness
- `GET /`: welcome message

**Example**

```bash
curl http://localhost:8090/health
curl http://localhost:8090/readiness
curl http://localhost:8090/liveness
curl http://localhost:8090/
```

------

## Middleware Extensions

**Function**
Run additional logic when requests enter or complete (e.g., logging, authentication, rate limiting).

**Example**

```{code-cell}
@app.middleware("http")
async def custom_logger(request, call_next):
    print(f"Received request: {request.method} {request.url}")
    response = await call_next(request)
    return response
```

- Built-in in AgentApp:
  - Request logging middleware
  - CORS (Cross-Origin Resource Sharing) support

------

## Celery Asynchronous Task Queue (Optional)

**Function**
Supports long-running background tasks without blocking the main HTTP thread.

**Key Parameters**

- `broker_url="redis://localhost:6379/0"`
- `backend_url="redis://localhost:6379/0"`

**Example Usage**

```{code-cell}
app = AgentApp(
    agent=agent,
    broker_url="redis://localhost:6379/0",
    backend_url="redis://localhost:6379/0"
)

@app.task("/longjob", queue="celery")
def heavy_computation(data):
    return {"result": data["x"] ** 2}
```

Request:

```bash
curl -X POST http://localhost:8090/longjob -H "Content-Type: application/json" -d '{"x": 5}'
```

Returns Task ID:

```bash
{"task_id": "abc123"}
```

Fetch result:

```bash
curl http://localhost:8090/longjob/abc123
```

------

## Custom Query Processing

**Function**
Use the `@app.query()` decorator to fully customize query processing logic, enabling more flexible control including state management, session history management, etc.

### Basic Usage

```{code-cell}
from agentscope_runtime.engine import AgentApp
from agentscope_runtime.engine.schemas.agent_schemas import AgentRequest
from agentscope.agent import ReActAgent
from agentscope.model import DashScopeChatModel
from agentscope.pipeline import stream_printing_messages
from agentscope_runtime.adapters.agentscope.memory import AgentScopeSessionHistoryMemory

app = AgentApp(
    app_name="Friday",
    app_description="A helpful assistant",
)

@app.query(framework="agentscope")
async def query_func(
    self,
    msgs,
    request: AgentRequest = None,
    **kwargs,
):
    """Custom query processing function"""
    session_id = request.session_id
    user_id = request.user_id
    
    # Load session state
    state = await self.state_service.export_state(
        session_id=session_id,
        user_id=user_id,
    )
    
    # Create Agent instance
    agent = ReActAgent(
        name="Friday",
        model=DashScopeChatModel(
            "qwen-turbo",
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            stream=True,
        ),
        sys_prompt="You're a helpful assistant named Friday.",
        memory=AgentScopeSessionHistoryMemory(
            service=self.session_service,
            session_id=session_id,
            user_id=user_id,
        ),
    )
    
    # Restore state (if exists)
    if state:
        agent.load_state_dict(state)
    
    # Stream process messages
    async for msg, last in stream_printing_messages(
        agents=[agent],
        coroutine_task=agent(msgs),
    ):
        yield msg, last
    
    # Save state
    state = agent.state_dict()
    await self.state_service.save_state(
        user_id=user_id,
        session_id=session_id,
        state=state,
    )
```

### Key Features

1. **Framework Support**: The `framework` parameter supports `"agentscope"`, `"autogen"`, `"agno"`, `"langgraph"`, etc.
2. **Function Signature**:
   - `self`: AgentApp instance, can access registered services
   - `msgs`: Input message list
   - `request`: AgentRequest object, containing `session_id`, `user_id`, etc.
   - `**kwargs`: Other extension parameters
3. **Streaming Output**: Functions can be generators, supporting streaming result returns
4. **State Management**: Can access `self.state_service` for state save and restore
5. **Session History**: Can access `self.session_service` for session history management

### State Service (StateService) Details

`StateService` is used to manage agent states, supporting state save, restore, and management. In custom query processing, you can access the state service through `self.state_service`.

**Main Methods**:

- `save_state(user_id, state, session_id=None, round_id=None)`: Save agent state
- `export_state(user_id, session_id=None, round_id=None)`: Export/load agent state
- `list_states(user_id, session_id=None)`: List all states
- `delete_state(user_id, session_id=None, round_id=None)`: Delete state

**Implementations**:

- `InMemoryStateService`: In-memory implementation, suitable for development and testing
- `RedisStateService`: Redis implementation, suitable for production environments with persistence support

**Usage Example**:

```{code-cell}
from agentscope_runtime.engine.services.agent_state import (
    InMemoryStateService,
    RedisStateService,
)

# Use in-memory state service (development)
@app.init
async def init_func(self):
    self.state_service = InMemoryStateService()
    await self.state_service.start()

# Use Redis state service (production)
@app.init
async def init_func(self):
    self.state_service = RedisStateService(
        host="localhost",
        port=6379,
        db=0,
    )
    await self.state_service.start()

# Use state service in query processing
@app.query(framework="agentscope")
async def query_func(self, msgs, request: AgentRequest = None, **kwargs):
    session_id = request.session_id
    user_id = request.user_id
    
    # Load historical state
    state = await self.state_service.export_state(
        user_id=user_id,
        session_id=session_id,
    )
    
    # Create Agent and restore state
    agent = ReActAgent(...)
    if state:
        agent.load_state_dict(state)
    
    # Process messages...
    
    # Save state
    new_state = agent.state_dict()
    await self.state_service.save_state(
        user_id=user_id,
        session_id=session_id,
        state=new_state,
    )
```

### Complete Example: AgentApp with State Management

```{code-cell}
import os
from agentscope_runtime.engine import AgentApp
from agentscope_runtime.engine.schemas.agent_schemas import AgentRequest
from agentscope.agent import ReActAgent
from agentscope.model import DashScopeChatModel
from agentscope.tool import Toolkit, execute_python_code
from agentscope.pipeline import stream_printing_messages
from agentscope_runtime.adapters.agentscope.memory import AgentScopeSessionHistoryMemory
from agentscope_runtime.engine.services.agent_state import InMemoryStateService
from agentscope_runtime.engine.services.session_history import InMemorySessionHistoryService

app = AgentApp(
    app_name="Friday",
    app_description="A helpful assistant with state management",
)

@app.init
async def init_func(self):
    """Initialize state and session services"""
    self.state_service = InMemoryStateService()
    self.session_service = InMemorySessionHistoryService()
    await self.state_service.start()
    await self.session_service.start()

@app.shutdown
async def shutdown_func(self):
    """Clean up services"""
    await self.state_service.stop()
    await self.session_service.stop()

@app.query(framework="agentscope")
async def query_func(
    self,
    msgs,
    request: AgentRequest = None,
    **kwargs,
):
    """Query processing with state management"""
    session_id = request.session_id
    user_id = request.user_id
    
    # Load historical state
    state = await self.state_service.export_state(
        session_id=session_id,
        user_id=user_id,
    )
    
    # Create toolkit
    toolkit = Toolkit()
    toolkit.register_tool_function(execute_python_code)
    
    # Create Agent
    agent = ReActAgent(
        name="Friday",
        model=DashScopeChatModel(
            "qwen-turbo",
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            enable_thinking=True,
            stream=True,
        ),
        sys_prompt="You're a helpful assistant named Friday.",
        toolkit=toolkit,
        memory=AgentScopeSessionHistoryMemory(
            service=self.session_service,
            session_id=session_id,
            user_id=user_id,
        ),
    )
    agent.set_console_output_enabled(enabled=False)
    
    # Restore state
    if state:
        agent.load_state_dict(state)
    
    # Stream process
    async for msg, last in stream_printing_messages(
        agents=[agent],
        coroutine_task=agent(msgs),
    ):
        yield msg, last
    
    # Save state
    state = agent.state_dict()
    await self.state_service.save_state(
        user_id=user_id,
        session_id=session_id,
        state=state,
    )

# Run service
app.run(host="0.0.0.0", port=8090)
```

### Comparison with Standard Agent Parameter Method

| Feature | Standard Method (agent parameter) | Custom Query (@app.query) |
|---------|-----------------------------------|---------------------------|
| Flexibility | Lower, uses predefined Agent | High, fully customizable processing logic |
| State Management | Automatic handling | Manual management, more flexible |
| Use Cases | Simple scenarios | Complex scenarios requiring fine-grained control |
| Multi-framework Support | Limited | Supports multiple frameworks |

------
## Local or Remote Deployment

**Function**
Deploy to different runtime environments via the unified `deploy()` method.

**Example Usage**

```{code-cell}
from agentscope_runtime.engine.deployers import LocalDeployManager

await app.deploy(LocalDeployManager(host="0.0.0.0", port=8091))
```

For more deployment options and detailed instructions, please refer to the {doc}`advanced_deployment` documentation.
