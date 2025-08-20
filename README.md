<div align="center">

# AgentScope Runtime

[![PyPI](https://img.shields.io/pypi/v/agentscope-runtime?label=PyPI&color=brightgreen&logo=python)](https://pypi.org/project/agentscope-runtime/)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg?logo=python&label=Python)](https://python.org)
[![License](https://img.shields.io/badge/license-Apache%202.0-red.svg?logo=apache&label=Liscnese)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-black.svg?logo=python&label=CodeStyle)](https://github.com/psf/black)
[![GitHub Stars](https://img.shields.io/github/stars/agentscope-ai/agentscope-runtime?style=flat&logo=github&color=yellow&label=Stars)](https://github.com/agentscope-ai/agentscope-runtime/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/agentscope-ai/agentscope-runtime?style=flat&logo=github&color=purple&label=Forks)](https://github.com/agentscope-ai/agentscope-runtime/network)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg?logo=githubactions&label=Build)](https://github.com/agentscope-ai/agentscope-runtime/actions)
[![Cookbook](https://img.shields.io/badge/📚_Cookbook-English|中文-teal.svg)](https://runtime.agentscope.io)
[![DeepWiki](https://img.shields.io/badge/DeepWiki-agentscope--runtime-navy.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACwAAAAyCAYAAAAnWDnqAAAAAXNSR0IArs4c6QAAA05JREFUaEPtmUtyEzEQhtWTQyQLHNak2AB7ZnyXZMEjXMGeK/AIi+QuHrMnbChYY7MIh8g01fJoopFb0uhhEqqcbWTp06/uv1saEDv4O3n3dV60RfP947Mm9/SQc0ICFQgzfc4CYZoTPAswgSJCCUJUnAAoRHOAUOcATwbmVLWdGoH//PB8mnKqScAhsD0kYP3j/Yt5LPQe2KvcXmGvRHcDnpxfL2zOYJ1mFwrryWTz0advv1Ut4CJgf5uhDuDj5eUcAUoahrdY/56ebRWeraTjMt/00Sh3UDtjgHtQNHwcRGOC98BJEAEymycmYcWwOprTgcB6VZ5JK5TAJ+fXGLBm3FDAmn6oPPjR4rKCAoJCal2eAiQp2x0vxTPB3ALO2CRkwmDy5WohzBDwSEFKRwPbknEggCPB/imwrycgxX2NzoMCHhPkDwqYMr9tRcP5qNrMZHkVnOjRMWwLCcr8ohBVb1OMjxLwGCvjTikrsBOiA6fNyCrm8V1rP93iVPpwaE+gO0SsWmPiXB+jikdf6SizrT5qKasx5j8ABbHpFTx+vFXp9EnYQmLx02h1QTTrl6eDqxLnGjporxl3NL3agEvXdT0WmEost648sQOYAeJS9Q7bfUVoMGnjo4AZdUMQku50McDcMWcBPvr0SzbTAFDfvJqwLzgxwATnCgnp4wDl6Aa+Ax283gghmj+vj7feE2KBBRMW3FzOpLOADl0Isb5587h/U4gGvkt5v60Z1VLG8BhYjbzRwyQZemwAd6cCR5/XFWLYZRIMpX39AR0tjaGGiGzLVyhse5C9RKC6ai42ppWPKiBagOvaYk8lO7DajerabOZP46Lby5wKjw1HCRx7p9sVMOWGzb/vA1hwiWc6jm3MvQDTogQkiqIhJV0nBQBTU+3okKCFDy9WwferkHjtxib7t3xIUQtHxnIwtx4mpg26/HfwVNVDb4oI9RHmx5WGelRVlrtiw43zboCLaxv46AZeB3IlTkwouebTr1y2NjSpHz68WNFjHvupy3q8TFn3Hos2IAk4Ju5dCo8B3wP7VPr/FGaKiG+T+v+TQqIrOqMTL1VdWV1DdmcbO8KXBz6esmYWYKPwDL5b5FA1a0hwapHiom0r/cKaoqr+27/XcrS5UwSMbQAAAABJRU5ErkJggg==)](https://deepwiki.com/agentscope-ai/agentscope-runtime)
[![A2A](https://img.shields.io/badge/A2A-Agent_to_Agent-blue.svg?label=A2A)](https://a2a-protocol.org/)
[![MCP](https://img.shields.io/badge/MCP-Model_Context_Protocol-purple.svg?logo=plug&label=MCP)](https://modelcontextprotocol.io/)
[![Discord](https://img.shields.io/badge/Discord-Join_Us-blueviolet.svg?logo=discord)](https://discord.gg/eYMpfnkG8h)
[![DingTalk](https://img.shields.io/badge/DingTalk-Join_Us-orange.svg)](https://qr.dingtalk.com/action/joingroup?code=v1,k1,OmDlBXpjW+I2vWjKDsjvI9dhcXjGZi3bQiojOq3dlDw=&_dt_no_comment=1&origin=11)

[[中文README]](README_zh.md)

**A Production-Ready Runtime Framework for Intelligent Agent Applications**

*AgentScope Runtime tackles two critical challenges in agent development: secure sandboxed tool execution and scalable agent deployment. Built with a dual-core architecture, it provides framework-agnostic infrastructure for deploying agents with full observability and safe tool interactions.*

</div>

---

## ✨ Key Features

- **🏗️ Deployment Infrastructure**: Built-in services for session management, memory, and sandbox environment control
- **🔒 Sandboxed Tool Execution**: Isolated sandboxes ensure safe tool execution without system compromise

- **🔧 Framework Agnostic**: Not tied to any specific framework. Works seamlessly with popular open-source agent frameworks and custom implementations

- ⚡ **Developer Friendly**: Simple deployment with powerful customization options

- **📊 Observability**: Comprehensive tracing and monitoring for runtime operations

---

## 💬 Contact

Welcome to join our community on

| [Discord](https://discord.gg/eYMpfnkG8h)                     | DingTalk                                                     |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| <img src="https://gw.alicdn.com/imgextra/i1/O1CN01hhD1mu1Dd3BWVUvxN_!!6000000000238-2-tps-400-400.png" width="100" height="100"> | <img src="https://img.alicdn.com/imgextra/i1/O1CN01LxzZha1thpIN2cc2E_!!6000000005934-2-tps-497-477.png" width="100" height="100"> |

---

## 📋 Table of Contents

- [🚀 Quick Start](#-quick-start)
- [📚 Cookbook](#-cookbook)
- [🔌 Agent Framework Integration](#-agent-framework-integration)
- [🏗️ Deployment](#️-deployment)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip or uv package manager

### Installation

From PyPI:

```bash
# Install core dependencies
pip install agentscope-runtime

# Install sandbox dependencies
pip install "agentscope-runtime[sandbox]"
```

(Optional) From source:

```bash
# Pull the source code from GitHub
git clone -b main https://github.com/agentscope-ai/agentscope-runtime.git
cd agentscope-runtime

# Install core dependencies
pip install -e .

# Install sandbox dependencies
pip install -e ".[sandbox]"
```

### Basic Agent Usage Example

This example demonstrates how to create a simple LLM agent using AgentScope Runtime and stream responses from the Qwen model.

```python
import asyncio
import os
from agentscope_runtime.engine import Runner
from agentscope_runtime.engine.agents.llm_agent import LLMAgent
from agentscope_runtime.engine.llms import QwenLLM
from agentscope_runtime.engine.schemas.agent_schemas import AgentRequest
from agentscope_runtime.engine.services.context_manager import ContextManager


async def main():
    # Set up the language model and agent
    model = QwenLLM(
        model_name="qwen-turbo",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
    )
    llm_agent = LLMAgent(model=model, name="llm_agent")

    async with ContextManager() as context_manager:
        runner = Runner(agent=llm_agent, context_manager=context_manager)

        # Create a request and stream the response
        request = AgentRequest(
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "What is the capital of France?",
                        },
                    ],
                },
            ],
        )

        async for message in runner.stream_query(request=request):
            if hasattr(message, "text"):
                print(f"Streamed Answer: {message.text}")


asyncio.run(main())
```

### Basic Sandbox Usage Example

This example demonstrates how to create sandboxed and execute tool within the sandbox.

```python
from agentscope_runtime.sandbox import BaseSandbox

with BaseSandbox() as box:
    print(box.run_ipython_cell(code="print('hi')"))
    print(box.run_shell_command(command="echo hello"))
```

> [!NOTE]
>
> Current version requires Docker to be installed and running on your system. In the future, we will provide Kubernetes deployment and public cloud deployment options. Please refer to [this tutorial](https://runtime.agentscope.io/en/sandbox.html) for more details.

---

## 📚 Cookbook

- **[📖 Cookbook](https://runtime.agentscope.io/en/intro.html)**: Comprehensive tutorials
- **[💡 Concept](https://runtime.agentscope.io/en/concept.html)**: Core concepts and architecture overview
- **[🚀 Quick Start](https://runtime.agentscope.io/en/quickstart.html)**: Quick start tutorial
- **[🏠 Demo House](https://runtime.agentscope.io/en/demohouse.html)**: Rich example projects

---

## 🔌 Agent Framework Integration

### AgentScope Integration

```python
import os

from agentscope.agent import ReActAgent
from agentscope.model import OpenAIChatModel
from agentscope_runtime.engine.agents.agentscope_agent import AgentScopeAgent

agent = AgentScopeAgent(
    name="Friday",
    model=OpenAIChatModel(
        "gpt-4",
        api_key=os.getenv("OPENAI_API_KEY"),
    ),
    agent_config={
        "sys_prompt": "You're a helpful assistant named {name}.",
    },
    agent_builder=ReActAgent,
)
```

### Agno Integration

```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agentscope_runtime.engine.agents.agno_agent import AgnoAgent

agent = AgnoAgent(
    name="Friday",
    model=OpenAIChat(
        id="gpt-4",
    ),
    agent_config={
        "instructions": "You're a helpful assistant.",
    },
    agent_builder=Agent,
)
```

### LangGraph Integration

```python
from typing import TypedDict
from langgraph import graph, types
from agentscope_runtime.engine.agents.langgraph_agent import LangGraphAgent


# define the state
class State(TypedDict, total=False):
    id: str


# define the node functions
async def set_id(state: State):
    new_id = state.get("id")
    assert new_id is not None, "must set ID"
    return types.Command(update=State(id=new_id), goto="REVERSE_ID")


async def reverse_id(state: State):
    new_id = state.get("id")
    assert new_id is not None, "ID must be set before reversing"
    return types.Command(update=State(id=new_id[::-1]))


state_graph = graph.StateGraph(state_schema=State)
state_graph.add_node("SET_ID", set_id)
state_graph.add_node("REVERSE_ID", reverse_id)
state_graph.set_entry_point("SET_ID")
compiled_graph = state_graph.compile(name="ID Reversal")
agent = LangGraphAgent(graph=compiled_graph)
```

> [!NOTE]
>
> More agent framework interations are comming soon!

---

## 🏗️ Deployment

The agent runner exposes a `deploy` method that takes a `DeployManager` instance and deploys the agent. The service port is set as the parameter `port` when creating the `LocalDeployManager`. The service endpoint path is set as the parameter `endpoint_path` when deploying the agent. In this example, we set the endpoint path to `/process`. After deployment, you can access the service at `http://localhost:8090/process`.

```python
from agentscope_runtime.engine.deployers import LocalDeployManager

# Create deployment manager
deploy_manager = LocalDeployManager(
    host="localhost",
    port=8090,
)

# Deploy the agent as a streaming service
deploy_result = await runner.deploy(
    deploy_manager=deploy_manager,
    endpoint_path="/process",
    stream=True,  # Enable streaming responses
)
```

---

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### 🐛 Bug Reports
- Use GitHub Issues to report bugs
- Include detailed reproduction steps
- Provide system information and logs

### 💡 Feature Requests
- Discuss new ideas in GitHub Discussions
- Follow the feature request template
- Consider implementation feasibility

### 🔧 Code Contributions
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

For detailed contributing guidelines, please see  [CONTRIBUTE](cookbook/en/contribute.md).

---

## 📄 License

AgentScope Runtime is released under the [Apache License 2.0](LICENSE).

```
Copyright 2025 Tongyi Lab

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
