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

# Quick Start

This guide demonstrates how to build a simple agent application in the **AgentScope Runtime** framework and deploy it as a service.

## Prerequisites

### 🔧 Installation Requirements

Install AgentScope Runtime with basic dependencies:

```bash
pip install agentscope-runtime
```

### 🔑 API Key Configuration

You'll need an API key for your chosen LLM provider. This example uses DashScope (Qwen):

```bash
export DASHSCOPE_API_KEY="your_api_key_here"
```

## Step-by-Step Implementation

### Step 1: Import Dependencies

Start by importing all necessary modules:

```{code-cell}
import os

from agentscope.agent import ReActAgent
from agentscope.model import DashScopeChatModel
from agentscope.formatter import DashScopeChatFormatter
from agentscope.tool import Toolkit, execute_python_code
from agentscope.pipeline import stream_printing_messages

from agentscope_runtime.engine import AgentApp
from agentscope_runtime.engine.schemas.agent_schemas import AgentRequest
from agentscope_runtime.adapters.agentscope.memory import (
    AgentScopeSessionHistoryMemory,
)
from agentscope_runtime.engine.services.agent_state import (
    InMemoryStateService,
)
from agentscope_runtime.engine.services.session_history import (
    InMemorySessionHistoryService,
)

print("✅ Dependencies imported successfully")
```

### Step 2: Create an Agent App

`AgentApp` is the core of an agent application's lifecycle and request handling. All initialization, query processing, and resource cleanup will be registered on it.

```{code-cell}
agent_app = AgentApp(
    app_name="Friday",
    app_description="A helpful assistant",
)

print("✅ Agent App created successfully")
```

### Step 3: Register Lifecycle Methods (Initialization & Shutdown)

Here we define what the app does at startup (initialize state management, session history services) and how it releases resources when shutting down.

```{code-cell}
@agent_app.init
async def init_func(self):
    self.state_service = InMemoryStateService()
    self.session_service = InMemorySessionHistoryService()

    await self.state_service.start()
    await self.session_service.start()

@agent_app.shutdown
async def shutdown_func(self):
    await self.state_service.stop()
    await self.session_service.stop()
```

### Step 4: Define AgentScope Agent Query Logic

- This section defines the business logic when the Agent API is called:
  - **Get session information**: Ensure context is isolated between different users/sessions.
  - **Build the agent**: Includes model, tools (e.g. execute Python code), memory, formatter.
  - **Support streaming output**: Must use `stream_printing_messages` to return `(msg, last)` to support generation while responding to the client.
  - **Persist state**: Save the agent’s current state.

```{code-cell}
@agent_app.query(framework="agentscope")
async def query_func(
    self,
    msgs,
    request: AgentRequest = None,
    **kwargs,
):
    session_id = request.session_id
    user_id = request.user_id

    state = await self.state_service.export_state(
        session_id=session_id,
        user_id=user_id,
    )

    toolkit = Toolkit()
    toolkit.register_tool_function(execute_python_code)

    agent = ReActAgent(
        name="Friday",
        model=DashScopeChatModel(
            "qwen-turbo",
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            stream=True,
        ),
        sys_prompt="You're a helpful assistant named Friday.",
        toolkit=toolkit,
        memory=AgentScopeSessionHistoryMemory(
            service=self.session_service,
            session_id=session_id,
            user_id=user_id,
        ),
        formatter=DashScopeChatFormatter(),
    )
    agent.set_console_output_enabled(enabled=False)

    if state:
        agent.load_state_dict(state)

    async for msg, last in stream_printing_messages(
        agents=[agent],
        coroutine_task=agent(msgs),
    ):
        yield msg, last

    state = agent.state_dict()

    await self.state_service.save_state(
        user_id=user_id,
        session_id=session_id,
        state=state,
    )
```

### Step 5: Start the Agent App

Start the Agent API server. Once running, the server will be listening at:
`http://localhost:8090/process`

```{code-cell}
app.run(host="0.0.0.0", port=8090)
```

### Step 6: Send Request to Agent

You can use `curl` to send a JSON payload to the API:

```bash
curl -N \
  -X POST "http://localhost:8090/process" \
  -H "Content-Type: application/json" \
  -d '{
    "input": [
      {
        "role": "user",
        "content": [
          { "type": "text", "text": "What is the capital of France?" }
        ]
      }
    ]
  }'
```

You’ll see output streamed in **Server-Sent Events (SSE)** format:

```bash
data: {"sequence_number":0,"object":"response","status":"created", ... }
data: {"sequence_number":1,"object":"response","status":"in_progress", ... }
data: {"sequence_number":2,"object":"content","status":"in_progress","text":"The" }
data: {"sequence_number":3,"object":"content","status":"in_progress","text":" capital of France is Paris." }
data: {"sequence_number":4,"object":"message","status":"completed","text":"The capital of France is Paris." }
```

### Step 7: Deploy the Agent App Using DeployManager

The AgentScope Runtime provides a powerful deployment system that allows you to deploy your agent to remote or local container. And we use `LocalDeployManager` as example:

```{code-cell}
async def main():
    await app.deploy(LocalDeployManager(host="0.0.0.0", port=8091))
```


This will run your agent API Server on the specified port, making it accessible for external requests. In addition to basic HTTP API access, you can interact with the agent through different protocols, such as A2A, Response API, Agent API, and others. Please refer {doc}`protocol` for details.

For example, user could query the deployment by OpenAI SDK with response api.

```python
from openai import OpenAI

client = OpenAI(base_url="http://0.0.0.0:8091/compatible-mode/v1")

response = client.responses.create(
  model="any_name",
  input="What is the weather in Beijing?"
)

print(response)
```