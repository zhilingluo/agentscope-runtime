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

# 快速开始

本教程演示如何在 **AgentScope Runtime** 框架中构建一个简单的智能体并将其部署为服务。

## 前置条件

### 🔧 安装要求

安装带有基础依赖的 AgentScope Runtime：

```bash
pip install agentscope-runtime
```

### 🔑 API密钥配置

您需要为所选的大语言模型提供商提供API密钥。本示例使用DashScope（Qwen）：

```bash
export DASHSCOPE_API_KEY="your_api_key_here"
```

## 分步实现

### 步骤1：导入依赖

首先导入所有必要的模块：

```{code-cell}
import os

from agentscope_runtime.engine import AgentApp
from agentscope_runtime.engine.agents.agentscope_agent import AgentScopeAgent
from agentscope_runtime.engine.deployers import LocalDeployManager
from agentscope.model import OpenAIChatModel
from agentscope.agent import ReActAgent


print("✅ 依赖导入成功")
```

### 步骤2：创建智能体

我们这里使用agentscope作为示例：

```{code-cell}
from agentscope.agent import ReActAgent
from agentscope.model import DashScopeChatModel
from agentscope_runtime.engine.agents.agentscope_agent import AgentScopeAgent

agent = AgentScopeAgent(
    name="Friday",
    model=DashScopeChatModel(
        "qwen-turbo",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
    ),
    agent_config={
        "sys_prompt": "You're a helpful assistant named Friday.",
    },
    agent_builder=ReActAgent,
)

print("✅ AgentScope agent created successfully")
```

### 步骤3：创建并启动Agent App

用agent和 `AgentApp` 创建一个 Agent API 服务器：

```{code-cell}
app = AgentApp(agent=agent, endpoint_path="/process")

app.run(host="0.0.0.0", port=8090)
```

运行后，服务器会启动并监听：`http://localhost:8090/process`

### 步骤4：发送一个请求

你可以使用 `curl` 向 API 发送 JSON 输入：

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

你将会看到以 **Server-Sent Events (SSE)** 格式流式输出的响应：

```bash
data: {"sequence_number":0,"object":"response","status":"created", ... }
data: {"sequence_number":1,"object":"response","status":"in_progress", ... }
data: {"sequence_number":2,"object":"content","status":"in_progress","text":"The" }
data: {"sequence_number":3,"object":"content","status":"in_progress","text":" capital of France is Paris." }
data: {"sequence_number":4,"object":"message","status":"completed","text":"The capital of France is Paris." }
```

### 步骤5: 使用 Deployer 部署代理

AgentScope Runtime 提供了一个功能强大的部署系统，可以将你的智能体部署到远程或本地容器中。这里我们以 `LocalDeployManager` 为例：

```{code-cell}
async def main():
    await app.deploy(LocalDeployManager(host="0.0.0.0", port=8091))
```

这段代码会在指定的端口运行你的智能体API Server，使其能够响应外部请求。除了基本的 HTTP API 访问外，你还可以使用不同的协议与智能体进行交互，例如：A2A、Response API、Agent API等。详情请参考 {doc}`protocol`。

例如用户可以通过OpenAI SDK 来请求这个部署。

```python
from openai import OpenAI

client = OpenAI(base_url="http://0.0.0.0:8091/compatible-mode/v1")

response = client.responses.create(
  model="any_name",
  input="杭州天气如何？"
)

print(response)
```