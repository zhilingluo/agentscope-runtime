# -*- coding: utf-8 -*-
import pytest

from agentscope_runtime.engine import Runner
from agentscope_runtime.engine.agents.llm_agent import LLMAgent
from agentscope_runtime.engine.schemas.context import Context
from agentscope_runtime.engine.llms import QwenLLM
from agentscope_runtime.engine.schemas.agent_schemas import (
    Message,
    TextContent,
    RunStatus,
    MessageType,
    AgentRequest,
)
from agentscope_runtime.engine.helpers.helper import simple_call_agent
from agentscope_runtime.engine.services.context_manager import (
    ContextManager,
    create_context_manager,
)
from agentscope_runtime.engine.services.memory_service import (
    InMemoryMemoryService,
)
from agentscope_runtime.engine.services.session_history_service import (
    Session,
    InMemorySessionHistoryService,
)


@pytest.mark.asyncio
async def test_llm_agent():
    USER_ID = "user_1"
    SESSION_ID = "session_001"  # Using a fixed ID for simplicity

    from dotenv import load_dotenv

    load_dotenv("../../.env")
    llm_agent = LLMAgent(
        model=QwenLLM(),
        name="llm_agent",
        description="A simple LLM agent",
    )

    context_manager = ContextManager(
        session_history_service=InMemorySessionHistoryService(),
    )
    context = Context(
        agent=llm_agent,
        context_manager=context_manager,
        user_id=USER_ID,
        session=Session(
            id=SESSION_ID,
            user_id=USER_ID,
            messages=[
                Message(
                    role="user",
                    content=[
                        TextContent(text="What is the capital of France?"),
                    ],
                ),
            ],
        ),
        request=AgentRequest(
            input=[
                Message(
                    role="user",
                    content=[
                        TextContent(text="What is the capital of France?"),
                    ],
                ),
            ],
        ),
    )
    gt = "Paris"
    all_result = ""
    print("\n")
    async for message in llm_agent.run_async(context):
        print(message)

        if (
            message.object == "message"
            and MessageType.MESSAGE == message.type
            and RunStatus.Completed == message.status
        ):
            all_result = message.content[0].text

    assert gt in all_result


@pytest.mark.asyncio
async def test_llm_agent_runner():
    USER_ID = "user_1"
    SESSION_ID = "session_001"

    from dotenv import load_dotenv

    load_dotenv("../../.env")
    llm_agent = LLMAgent(
        model=QwenLLM(),
        name="llm_agent",
        description="A simple LLM agent",
    )

    gt = "Paris"

    async with create_context_manager() as context_manager:
        runner = Runner(
            agent=llm_agent,
            context_manager=context_manager,
            environment_manager=None,
        )

    all_result = ""
    print("\n")
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
        session_id=SESSION_ID,
    )

    async for message in runner.stream_query(
        user_id=USER_ID,
        request=request,
    ):
        print(message)

        if (
            message.object == "message"
            and MessageType.MESSAGE == message.type
            and RunStatus.Completed == message.status
        ):
            all_result = message.content[0].text

    assert gt in all_result


@pytest.mark.asyncio
async def test_llm_agent_runner_session():
    USER_ID = "user_1"
    SESSION_ID = "session_001"

    from dotenv import load_dotenv

    load_dotenv("../../.env")
    llm_agent = LLMAgent(
        model=QwenLLM(),
    )

    session_history_service = InMemorySessionHistoryService()
    await session_history_service.create_session(
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    async with create_context_manager(
        session_history_service=session_history_service,
    ) as context_manager:
        runner = Runner(
            agent=llm_agent,
            context_manager=context_manager,
            environment_manager=None,
        )

        first_round_answser = await simple_call_agent(
            "what is the capital of France",
            runner,
            USER_ID,
            SESSION_ID,
        )
        second_round_answer = await simple_call_agent(
            "what is my previous question",
            runner,
            USER_ID,
            SESSION_ID,
        )
        gt = "capital of France"
        neg_gt = "Paris"

        assert gt in second_round_answer and neg_gt not in second_round_answer

        print("first round answer is " + first_round_answser)
        print("second round answer is " + second_round_answer)


@pytest.mark.asyncio
async def test_llm_agent_runner_memory():
    USER_ID = "user_1"
    SESSION_ID = "session_001"
    SESSION_ID2 = "session_002"

    from dotenv import load_dotenv

    load_dotenv("../../.env")
    llm_agent = LLMAgent(
        model=QwenLLM(),
    )

    session_history_service = InMemorySessionHistoryService()
    await session_history_service.create_session(
        user_id=USER_ID,
        session_id=SESSION_ID,
    )
    memory_service = InMemoryMemoryService()

    async with create_context_manager(
        session_history_service=session_history_service,
        memory_service=memory_service,
    ) as context_manager:
        runner = Runner(
            agent=llm_agent,
            context_manager=context_manager,
            environment_manager=None,
        )

        first_round_answser = await simple_call_agent(
            "what is the capital of France",
            runner,
            USER_ID,
            SESSION_ID,
        )
        second_round_answer = await simple_call_agent(
            "what is my previous question",
            runner,
            USER_ID,
            SESSION_ID2,
        )
        gt = "capital of France"

        assert gt in second_round_answer

        print("first round answer is " + first_round_answser)
        print("second round answer is " + second_round_answer)
