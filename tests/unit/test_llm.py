# -*- coding: utf-8 -*-
# pylint: disable=redefined-outer-name,unused-argument
import os

import pytest

from agentscope_runtime.engine.llms import QwenLLM

gt = "Paris"


@pytest.fixture
def env():
    if os.path.exists("../../.env"):
        from dotenv import load_dotenv

        load_dotenv("../../.env")


def test_qwen_generation(env):
    qwen = QwenLLM()
    event = qwen.generate("What is the capital of France?")
    print(event)
    assert gt in event


def test_qwen_chat(env):
    qwen = QwenLLM()
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"},
    ]
    event = qwen.chat(messages)
    print(event)
    assert gt in event
