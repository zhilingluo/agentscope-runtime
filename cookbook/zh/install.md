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

# 安装

准备好开始使用 AgentScope Runtime 了吗？本指南将帮助您在几分钟内快速搭建和运行**AgentScope Runtime**。

## 安装方式

### 1. 通过 PyPI 安装

```{warning}
本项目正在快速开发和迭代中。我们建议从源码安装以获取最新功能和Bug修复。
```

要通过 PyPI 安装Agentscope Runtime的稳定版本，请使用：

```bash
pip install agentscope-runtime
```

如需完整功能，包括沙箱功能和其他智能体框架集成：

```bash
pip install "agentscope-runtime[sandbox,agentscope,langgraph,agno]"
```

### 2. （可选）从源码安装

如果您想要使用最新的开发版本或为项目做贡献，可以从源码安装：

```bash
git clone https://github.com/agentscope-ai/agentscope-runtime.git

cd agentscope-runtime

pip install .
```

对于开发用途，您需要安装包含开发依赖的版本：

```bash
pip install ".[dev]"
```

## 检查您的安装

要验证安装并查看当前版本，请在 Python 中运行以下代码：

```{code-cell}
import agentscope_runtime

print(f"AgentScope Runtime {agentscope_runtime.__version__} is ready!")
```

执行代码后，您应该会看到版本号输出。

### 检查 AgentScope Agent

```{code-cell}
try:
    from agentscope_runtime.engine.agents.agentscope_agent import AgentScopeAgent
    print(f"✅ {AgentScopeAgent.__name__} - 导入成功")
except ImportError as e:
    print(f"❌ AgentScopeAgent - 导入失败：{e}")
    print('💡 尝试通过以下命令安装：pip install "agentscope-runtime[agentscope]"')
```

### 检查 Agno Agent

```{code-cell}
try:
    from agentscope_runtime.engine.agents.agno_agent import AgnoAgent
    print(f"✅ {AgnoAgent.__name__} - 导入成功")
except ImportError as e:
    print(f"❌ AgnoAgent - 导入失败：{e}")
    print('💡尝试通过以下命令安装：pip install "agentscope-runtime[agno]"')
```

### 检查 LangGraph Agent

```{code-cell}
try:
    from agentscope_runtime.engine.agents.langgraph_agent import LangGraphAgent
    print(f"✅ {LangGraphAgent.__name__} - 导入成功")
except ImportError as e:
    print(f"❌ LangGraphAgent -导入失败：{e}")
    print('💡尝试通过以下命令安装：pip install "agentscope-runtime[langgraph]"')
```

## 安装选项说明

这个图展示了安装选项的层次结构，底层是核心运行时（agentscope-runtime）。在核心之上可以选装各种模块（比如 sandbox、AgentScope、LangGraph 等），每个模块都会增加特定的功能（比如工具执行、框架整合等），同时也需要安装对应的依赖包（比如 Docker、测试工具等）。

<img src="/_static/installation_options_zh.jpg" alt="Installation Options" style="zoom:25%;" />
