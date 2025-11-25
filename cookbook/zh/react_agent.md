---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.5
kernelspec:
  display_name: Python 3.10
  language: python
  name: python3
---

# 参考: 完整部署样例

本教程演示了如何使用AgentScope Runtime与[**AgentScope框架**](https://github.com/modelscope/agentscope)创建和部署 *“推理与行动”(ReAct)* 智能体。

```{note}
ReAct（推理与行动）范式使智能体能够将推理轨迹与特定任务的行动交织在一起，使其在工具交互任务中特别有效。通过将AgentScope的`ReActAgent`与AgentScope Runtime的基础设施相结合，您可以同时获得智能决策和安全的工具执行。
```

## 前置要求

### 🔧 安装依赖

```bash
pip install agentscope-runtime
```

### 🔑 API 密钥

```{note}
确保您的浏览器沙箱环境已准备好使用，详细信息请参见{doc}`sandbox`。
```

确保浏览器沙箱镜像可用：

```bash
docker pull agentscope-registry.ap-southeast-1.cr.aliyuncs.com/agentscope/runtime-sandbox-browser:latest && docker tag agentscope-registry.ap-southeast-1.cr.aliyuncs.com/agentscope/runtime-sandbox-browser:latest agentscope/runtime-sandbox-browser:latest
```

### 🔑 API密钥配置

您需要为您选择的LLM提供商准备API密钥。此示例使用DashScope（Qwen），但您可以将其适配到其他提供商：

```bash
export DASHSCOPE_API_KEY="your_api_key_here"
```

## 分步实现

### 步骤 1：导入依赖

```{code-cell}
import os

from agentscope.agent import ReActAgent
from agentscope.model import DashScopeChatModel
from agentscope.formatter import DashScopeChatFormatter
from agentscope.tool import Toolkit, execute_python_code
from agentscope.pipeline import stream_printing_messages

from agentscope_runtime.engine import AgentApp
from agentscope_runtime.engine.schemas.agent_schemas import AgentRequest
from agentscope_runtime.adapters.agentscope.memory import AgentScopeSessionHistoryMemory
from agentscope_runtime.engine.services.agent_state import InMemoryStateService
from agentscope_runtime.engine.services.session_history import InMemorySessionHistoryService
from agentscope_runtime.engine.services.sandbox import SandboxService
from agentscope_runtime.sandbox import BrowserSandbox
```

### 步骤 2：准备浏览器沙箱工具

与 `tests/sandbox/test_sandbox.py` 相同，我们可以直接通过上下文管理器验证浏览器沙箱是否可用：

```{code-cell}
with BrowserSandbox() as box:
    print(box.list_tools())
    print(box.browser_navigate("https://www.example.com/"))
    print(box.browser_snapshot())
```

当需要在服务内长期复用沙箱时，参考 `tests/sandbox/test_sandbox_service.py` 使用 `SandboxService` 管理生命周期：

```{code-cell}
import asyncio

async def bootstrap_browser_sandbox():
    sandbox_service = SandboxService()
    await sandbox_service.start()

    session_id = "demo_session"
    user_id = "demo_user"

    sandboxes = sandbox_service.connect(
        session_id=session_id,
        user_id=user_id,
        sandbox_types=["browser"],
    )
    browser_box = sandboxes[0]
    browser_box.browser_navigate("https://www.example.com/")
    browser_box.browser_snapshot()

    await sandbox_service.stop()

asyncio.run(bootstrap_browser_sandbox())
```
这里的 `sandbox_types=["browser"]` 与 `tests/sandbox/test_sandbox_service.py` 保持一致，可确保同一 `session_id` / `user_id` 复用同一个浏览器沙箱实例。

### 步骤 3：构建 AgentApp

下面的逻辑与测试用例 `run_app()` 完全一致，包含状态服务初始化、会话记忆以及流式响应：

```{code-cell}
PORT = 8090

agent_app = AgentApp(
    app_name="Friday",
    app_description="A helpful assistant",
)


@agent_app.init
async def init_func(self):
    self.state_service = InMemoryStateService()
    self.session_service = InMemorySessionHistoryService()
    self.sandbox_service = SandboxService()

    await self.state_service.start()
    await self.session_service.start()
    await self.sandbox_service.start()


@agent_app.shutdown
async def shutdown_func(self):
    await self.state_service.stop()
    await self.session_service.stop()
    await self.sandbox_service.stop()


@agent_app.query(framework="agentscope")
async def query_func(self, msgs, request: AgentRequest = None, **kwargs):
    session_id = request.session_id
    user_id = request.user_id

    state = await self.state_service.export_state(
        session_id=session_id,
        user_id=user_id,
    )

    sandboxes = self.sandbox_service.connect(
        session_id=session_id,
        user_id=user_id,
        sandbox_types=["browser"],
    )
    browser_box = sandboxes[0]

    toolkit = Toolkit()
    for tool in (
        browser_box.browser_navigate,
        browser_box.browser_snapshot,
        browser_box.browser_take_screenshot,
        browser_box.browser_click,
        browser_box.browser_type,
    ):
        toolkit.register_tool_function(tool)
    toolkit.register_tool_function(execute_python_code)

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

    await self.state_service.save_state(
        user_id=user_id,
        session_id=session_id,
        state=agent.state_dict(),
    )
```

上述 `query_func` 会将 Agent 的输出通过 SSE 逐条返回，同时把最新 state 写回内存服务，实现多轮记忆。

借助 `SandboxService`（`sandbox_types=["browser"]`） ，浏览器沙箱会根据同一个 `session_id`、`user_id` 在多轮对话中复用，避免重复启动容器。

### 步骤 4：启动服务

```{code-cell}
if __name__ == "__main__":
    agent_app.run(host="127.0.0.1", port=PORT)
```

运行脚本后即可在 `http://127.0.0.1:8090/process` 收到流式响应。

### 步骤 5：测试 SSE 输出

```bash
curl -N \
  -X POST "http://127.0.0.1:8090/process" \
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

你将看到多条 `data: {...}` 事件以及最终的 `data: [DONE]`。如果消息体中包含 “Paris” 即表示回答正确。

### 步骤 6：多轮记忆验证

要验证 `AgentScopeSessionHistoryMemory` 是否生效，可以复用测试中「两轮对话」的交互流程：第一次提交 “My name is Alice.” 并携带固定 `session_id`，第二次询问 “What is my name?”，若返回文本包含 “Alice” 即表示记忆成功。

### 步骤 7：OpenAI 兼容模式

AgentApp 同时暴露了 `compatible-mode/v1` 路径，可使用官方 `openai` SDK 验证：

```{code-cell}
from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:8090/compatible-mode/v1")
resp = client.responses.create(
    model="any_name",
    input="Who are you?",
)

print(resp.response["output"][0]["content"][0]["text"])
```

正常情况下你会得到 “I’m Friday ...” 之类的回答。

## 总结

通过复现测试用例中的实现，你可以快速获得一个带有流式响应、会话记忆以及 OpenAI 兼容接口的 ReAct 智能体服务。若需部署到远端或扩展更多工具，只需替换 `DashScopeChatModel`、状态服务或工具注册逻辑即可。
