# Tools

In AgentScope Runtime, tools are how agents deliver business capabilities. Whether you call model services directly, run browser automation, or integrate corporate APIs, the tool stack must be safe, controllable, and extensible. This chapter outlines the overall approach and links to the follow-up sections (Ready-to-use Tools, Sandbox Basics/Advanced, Training Sandbox, Sandbox Troubleshooting) so you can select the right path for your scenario.

## Tool Integration Modes

Runtime supports three common ways to connect tools:

1. **Ready-to-use tools**: Vendor- or Runtime-provided capabilities (such as RAG retrieval) that require zero deployment.
2. **Sandboxed tools**: Tools executed inside Browser/FileSystem or other sandboxes for controlled side effects.
3. **Custom/MCP tools**: Fully extensible plugins, including in-house APIs, MCP providers, or external microservices.

You can mix and match while managing dependencies with `ToolRegistry`, `SandboxService`, and related modules.

## Section Guide

### Ready-to-use Tools

Showcases the built-in tools you can call directly within Runtime—retrieval, file understanding, and more. It is ideal when you want to reuse the Alibaba Cloud ecosystem quickly. Configuration patterns and best practices are included in {doc}`dashscope_tools`.

### Sandbox Basics

Introduces sandbox concepts, lifecycle, and common types (browser, filesystem, Python execution, etc.). You will learn how to:

- Provision, connect, and release sandboxes via `SandboxService`.
- Infer sandbox types automatically based on tool dependencies.
- Reuse or isolate resources across multi-session scenarios.

See {doc}`sandbox` for hands-on details.

### Sandbox Advanced

Dives into multi-tenancy, security compliance, and remote sandbox proxies. Targeted at teams that need to run at scale or meet enterprise security requirements, covering:

- Access control via tokens and ACLs.
- Integrations with Kubernetes or remote container fleets.
- Extension hooks for new sandbox types.

Read {doc}`sandbox_advanced` for the complete guidance.

### Training Sandbox

Focuses on sandboxes for evaluation, training, or self-play workloads. Examples include:

- Offline matches or task replays.
- Batch validation of tool invocations via policy scripts.
- Reproducing complex task flows within a controlled environment.

See {doc}`training_sandbox` for more.

### Sandbox Troubleshooting

Provides checklists and fixes for common issues such as failed sandbox start, tool timeouts, or missing permissions. It explains what to inspect (logs, health probes, resource usage) plus frequent error codes.

Follow {doc}`sandbox_troubleshooting` for the diagnostic steps.

## Recommended Flow

1. Start from ready-to-use tools or your in-house tools to determine the invocation pattern.
2. Decide whether you need sandboxes—and at which level—based on side effects and security posture.
3. Use the training and advanced sandbox chapters to perform batch validation and production hardening.
4. Consult the troubleshooting section whenever stability issues arise.

This approach yields a secure, reliable, and extensible tool stack so your agents can keep evolving.

