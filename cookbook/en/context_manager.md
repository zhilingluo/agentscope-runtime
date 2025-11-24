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

# Services

## Overview

Services in AgentScope Runtime provide essential functionality for agent execution, including session history management, memory storage, sandbox management, and state management. All services implement the `ServiceWithLifecycleManager` interface, which provides standard lifecycle management methods: `start()`, `stop()`, and `health()`.

## Service Interface

All services must implement the `ServiceWithLifecycleManager` interface:

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

### Service Lifecycle

Services follow a standard lifecycle pattern:

```{code-cell}
import asyncio
from agentscope_runtime.engine.services.memory import InMemoryMemoryService

async def main():
    # Create service
    memory_service = InMemoryMemoryService()

    # Start service
    await memory_service.start()

    # Check service health
    is_healthy = await memory_service.health()
    print(f"Service health status: {is_healthy}")

    # Stop service
    await memory_service.stop()

await main()
```

## Available Services

### SessionHistoryService

`SessionHistoryService` manages conversation sessions for users, providing a structured way to handle conversation history and message storage. Each session contains the history of a conversation and is uniquely identified by its ID.

#### Service Overview

The Session Service provides an abstract interface for session management with concrete implementations like `InMemorySessionHistoryService`.

```{code-cell}
from agentscope_runtime.engine.services.session_history import InMemorySessionHistoryService
from agentscope_runtime.engine.schemas.session import Session

# Create a session service instance
session_history_service = InMemorySessionHistoryService()
```

#### Core Functionality

- `create_session`: Create a new session
- `get_session`: Get a session
- `delete_session`: Delete a session
- `list_sessions`: List all sessions
- `append_message`: Append a message to the history

For details, see {ref}`here <session-history-service>`

### MemoryService

The `MemoryService` manages long-term memory storage. In Agent, memory stores previous conversation of an end-user. For example, an end-user may mention their name in a previous conversation. The memory service will store it so that the agent can use it in the next conversation.

#### Service Overview

The Memory Service provides an abstract interface for memory management with concrete implementations like `InMemoryMemoryService`.

```{code-cell}
from agentscope_runtime.engine.services.memory import InMemoryMemoryService

# Create and start the memory service
memory_service = InMemoryMemoryService()
```

#### Core Functionality

- `add_memory`: Add a memory to the memory service
- `search_memory`: Search a memory from the memory service
- `delete_memory`: Delete a memory from the memory service
- `list_memory`: List all memories

For details, see {ref}`here <memory-service>`

### SandboxService

The **Sandbox Service** manages and provides access to sandboxed tool execution environments for different users and sessions. Sandboxes are organized by a composite key of session ID and user ID, allowing isolated execution contexts for each user session.

#### Service Overview

The Sandbox Service provides a unified interface for sandbox management with support for different sandbox types like code execution, file operations, and other specialized sandboxes.

```{code-cell}
from agentscope_runtime.engine.services.sandbox_service import SandboxService

# Create and start the sandbox service
sandbox_service = SandboxService()

# Or with remote sandbox service
# sandbox_service = SandboxService(
#     base_url="http://sandbox-server:8000",
#     bearer_token="your-auth-token"
# )
```

#### Core Functionality

- `connect`: Connect to sandboxes for a specific user session
- `release`: Release sandboxes when no longer needed

For details, see {doc}`sandbox` and {doc}`environment_manager`.

### StateService

The `StateService` manages agent state storage. It stores and manages agent states organized by user_id, session_id, and round_id. Supports saving, retrieving, listing, and deleting states.

#### Service Overview

The State Service provides an abstract interface for state management with concrete implementations like `InMemoryStateService`.

```{code-cell}
from agentscope_runtime.engine.services.agent_state.state_service import InMemoryStateService

# Create and start the state service
state_service = InMemoryStateService()
```

#### Core Functionality

- `save_state`: Save serialized state data for a specific user/session
- `export_state`: Retrieve serialized state data for a user/session

## Available Memory Services

|         MemoryType         | Import                                                                                             |                       Note                       |
|:--------------------------:|----------------------------------------------------------------------------------------------------|:------------------------------------------------:|
|   InMemoryMemoryService    | `from agentscope_runtime.engine.services.memory import InMemoryMemoryService`              |                                                  |
|     RedisMemoryService     | `from agentscope_runtime.engine.services.redis_memory_service import RedisMemoryService`           |                                                  |
| ReMe.PersonalMemoryService | `from reme_ai.service.personal_memory_service import PersonalMemoryService`                        | [User Guide](https://github.com/modelscope/ReMe) |
|   ReMe.TaskMemoryService   | `from reme_ai.service.task_memory_service import TaskMemoryService`                                | [User Guide](https://github.com/modelscope/ReMe) |
| Mem0MemoryService | `from agentscope_runtime.engine.services.memory import Mem0MemoryService`             |                   |
| TablestoreMemoryService | `from agentscope_runtime.engine.services.memory import TablestoreMemoryService` |        develop by [tablestore-for-agent-memory](https://github.com/aliyun/alibabacloud-tablestore-for-agent-memory/blob/main/python/docs/knowledge_store_tutorial.ipynb)                          |

### Description
- **InMemoryMemoryService**: An in-memory memory service without persistent storage.
- **RedisMemoryService**: A memory service leveraging Redis for persistent storage.
- **ReMe.PersonalMemoryService**: ReMe's personalized memory service (formerly MemoryScope) empowers you to generate, retrieve, and share customized memories. Leveraging advanced LLM, embedding, and vector store technologies, it builds a comprehensive memory system with intelligent, context- and time-aware memory management—seamlessly enabling you to configure and deploy powerful AI agents.
- **ReMe.TaskMemoryService**: ReMe's task-oriented memory service helps you efficiently manage and schedule task-related memories, enhancing both the accuracy and efficiency of task execution. Powered by LLM capabilities, it supports flexible creation, retrieval, update, and deletion of memories across diverse task scenarios—enabling you to effortlessly build and scale robust agent-based task systems.
- **Mem0MemoryService**: An intelligent memory service powered by the mem0 platform, providing long-term memory storage and management capabilities. Supports asynchronous operations and automatically extracts, stores, and retrieves key information from conversations, enabling context-aware memory for AI agents. Ideal for complex conversational scenarios and agent applications requiring persistent memory. (For more details, see [mem0 platform documentation](https://docs.mem0.ai/platform/quickstart))
- **TablestoreMemoryService**: A memory service based on aliyun tablestore (Tablestore provides Serverless table storage services for massive structured data, and provides a one-stop IoTstore solution for deep optimization of IoT scenarios. It is suitable for structured data storage in scenarios such as massive bills, IM messages, IoT, Internet of Vehicles, risk control, and recommendations, and provides low-cost storage of massive data, millisecond-level online data query and retrieval, and flexible data analysis capabilities), develop by [tablestore-for-agent-memory](https://github.com/aliyun/alibabacloud-tablestore-for-agent-memory/blob/main/python/docs/knowledge_store_tutorial.ipynb). Example:
```python
from agentscope_runtime.engine.services.memory import TablestoreMemoryService
from agentscope_runtime.engine.services.utils.tablestore_service_utils import create_tablestore_client
from agentscope_runtime.engine.services.tablestore_memory_service import SearchStrategy

# create tablestore memory service, default search strategy is full text
tablestore_memory_service = TablestoreMemoryService(
    tablestore_client=create_tablestore_client(
        end_point="your_endpoint",
        instance_name="your_instance_name",
        access_key_id="your_access_key_id",
        access_key_secret="your_access_key_secret",
    ),
)

# Create a tablestore memory service based on vector retrieval, with DashScopeEmbeddings() as the default embedding model
tablestore_memory_service = TablestoreMemoryService(
    tablestore_client=create_tablestore_client(
        end_point="your_endpoint",
        instance_name="your_instance_name",
        access_key_id="your_access_key_id",
        access_key_secret="your_access_key_secret",
    ),
    search_strategy=SearchStrategy.VECTOR,
)
```

(session-history-service)=

## Details about Session History Service

The Session History Service manages conversation sessions for users, providing a structured way to handle conversation history and message storage. Each session contains the history of a conversation and is uniquely identified by its ID.

### Session Object Structure

Each session is represented by a `Session` object with the following structure:

```{code-cell}
from agentscope_runtime.engine.schemas.session import Session
from agentscope_runtime.engine.schemas.agent_schemas import Message, TextContent, Role

# Session object structure
session_obj = Session(
    id="session_123",
    user_id="user_456",
    messages=[
        Message(role=Role.USER, content=[TextContent(type="text", text="Hello")]),
        Message(role=Role.ASSISTANT, content=[TextContent(type="text", text="Hi there!")]),
    ],
)

print(f"Session ID: {session_obj.id}")
print(f"User ID: {session_obj.user_id}")
print(f"Message count: {len(session_obj.messages)}")
```

### Core Functionality

#### Creating Sessions

The `create_session` method creates new conversation sessions for users:

```{code-cell}
import asyncio


async def main():
    # Create a session with auto-generated ID
    user_id = "test_user"
    session = await session_history_service.create_session(user_id)
    print(f"Created session: {session.id}")
    print(f"User ID: {session.user_id}")
    print(f"Messages count: {len(session.messages)}")

    # Create a session with custom ID
    custom_session = await session_history_service.create_session(
        user_id,
        session_id="my_custom_session_id",
    )
    print(f"Custom session ID: {custom_session.id}")


await main()
```

#### Retrieving Sessions

The `get_session` method retrieves specific sessions by user ID and session ID:

```{code-cell}
import asyncio


async def main():
    user_id = "u1"
    # Retrieve an existing session (auto-creates if not exists in in-memory impl)
    retrieved_session = await session_history_service.get_session(user_id, "s1")
    assert retrieved_session is not None


await main()
```

#### Listing Sessions

The `list_sessions` method provides a list of all sessions for a user:

```{code-cell}
import asyncio


async def main():
    user_id = "u_list"
    # Create multiple sessions
    session1 = await session_history_service.create_session(user_id)
    session2 = await session_history_service.create_session(user_id)

    # List all sessions (without message history for efficiency)
    listed_sessions = await session_history_service.list_sessions(user_id)
    assert len(listed_sessions) >= 2

    # Returned sessions don't include message history
    for s in listed_sessions:
        assert s.messages == [], "History should be empty in list view"


await main()
```

#### Appending Messages

The `append_message` method adds messages to session history and supports multiple message formats:

##### Using Dictionary Format

```{code-cell}
import asyncio
from agentscope_runtime.engine.schemas.agent_schemas import Message, TextContent


async def main():
    user_id = "u_append"
    # Create a session and add messages (dict format is also accepted)
    session = await session_history_service.create_session(user_id)

    # Append a single message (Message object)
    message1 = Message(role="user", content=[TextContent(type="text", text="Hello, world!")])
    await session_history_service.append_message(session, message1)

    # Verify message was added
    assert len(session.messages) == 1

    # Append multiple messages at once (mixed formats)
    messages3 = [
        {"role": "user", "content": [{"type": "text", "text": "How are you?"}]},
        Message(role="assistant", content=[TextContent(type="text", text="I am fine, thank you.")]),
    ]
    await session_history_service.append_message(session, messages3)

    # Verify all messages were added
    assert len(session.messages) == 3


await main()
```

#### Deleting Sessions

The `delete_session` method removes specific sessions:

```{code-cell}
# Create and then delete a session
session_to_delete = await session_history_service.create_session(user_id)
session_id = session_to_delete.id

# Verify session exists
assert await session_history_service.get_session(user_id, session_id) is not None

# Delete the session
await session_history_service.delete_session(user_id, session_id)

# Verify session is deleted
assert await session_history_service.get_session(user_id, session_id) is None

# Deleting non-existent sessions doesn't raise errors
await session_history_service.delete_session(user_id, "non_existent_id")
```

### Service Lifecycle

The Session Service follows a simple lifecycle pattern:

```{code-cell}
# Start the service (optional for InMemorySessionHistoryService)
await session_history_service.start()

# Check service health
is_healthy = await session_history_service.health()

# Stop the service (optional for InMemorySessionHistoryService)
await session_history_service.stop()
```

### Implementation Details

The `InMemorySessionHistoryService` stores data in a nested dictionary structure:

+ Top level: `{user_id: {session_id: Session}}`
+ Each Session object contains id, user_id, and messages list
+ Session IDs are auto-generated using UUID if not provided
+ Empty or whitespace-only session IDs are replaced with auto-generated IDs

`TablestoreSessionHistoryService` stores data in aliyun tablestore, example：
```python
from agentscope_runtime.engine.services.session_history import TablestoreSessionHistoryService
from agentscope_runtime.engine.services.utils.tablestore_service_utils import create_tablestore_client

tablestore_session_history_service = TablestoreSessionHistoryService(
    tablestore_client=create_tablestore_client(
        end_point="your_endpoint",
        instance_name="your_instance_name",
        access_key_id="your_access_key_id",
        access_key_secret="your_access_key_secret",
    ),
)
```

```{note}
For production use, consider implementing persistent storage by extending the `SessionHistoryService` abstract base class to support databases or file systems.
```

(memory-service)=

## Details about Memory Service

The Memory Service is designed to store and retrieve long-term memory from databases or in-memory storage.
Memory is organized by user ID at the top level, with the message list serving as the elemental values stored in different locations. Additionally, messages can be grouped by session ID.

### Core Functionality

#### Adding Memory

The `add_memory` method allows you to store messages for a specific user, optionally providing a session ID:

```{code-cell}
import asyncio
from agentscope_runtime.engine.services.memory import InMemoryMemoryService
from agentscope_runtime.engine.schemas.agent_schemas import Message, TextContent

# Add memory without a session ID
user_id = "user1"
messages = [
        Message(
            role="user",
            content=[TextContent(type="text", text="hello world")]
        )
    ]
await memory_service.add_memory(user_id, messages)

```

#### Searching Memory

The `search_memory` method searches for messages based on content keywords:

In the `in-memory` memory service, a simple keyword search algorithm is implemented
to related content based on the query from historical messages.
Other complicated search algorithms could be used to replace the simple method by implementing or overriding the class.

User could use message as a query to search for related content.

```{code-cell}
search_query = [
    Message(
        role="user",
        content=[TextContent(type="text", text="hello")]
    )
]
retrieved = await memory_service.search_memory(user_id, search_query)
```


#### Listing Memory

list memory method provide a paginated interface for listing memory shown below,

```{code-cell}
# List memory with pagination
memory_list = await memory_service.list_memory(
    user_id,
    filters={"page_size": 10, "page_num": 1}
)
```

#### Deleting Memory

Users can delete memory for specific sessions or entire users:

```{code-cell}
# Delete memory for specific session
await memory_service.delete_memory(user_id, session_id)

# Delete all memory for user
await memory_service.delete_memory(user_id)
```


### Service Lifecycle

#### Service Lifecycle Management

The Memory Service follows a standard lifecycle pattern and can be managed through `start()`, `stop()`, `health()`:

```{code-cell}
import asyncio
from agentscope_runtime.engine.services.memory import InMemoryMemoryService

async def main():
    # Create memory service
    memory_service = InMemoryMemoryService()

    # Start service
    await memory_service.start()

    # Check service health
    is_healthy = await memory_service.health()
    print(f"Service health status: {is_healthy}")

    # Stop service
    await memory_service.stop()

await main()
```


#### Implementation Details

The `InMemoryMemoryService` stores data in a dictionary structure:

+ Top level: `{user_id: {session_id: [messages]}}`
+ Default session ID is used when no session is specified
+ Keyword-based search is case-insensitive
+ Messages are stored in chronological order within each session

```{note}
For more advanced memory implementations, consider extending the `MemoryService` abstract base class to support persistent storage or vector databases.
```
