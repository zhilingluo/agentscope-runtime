# -*- coding: utf-8 -*-
import os

import pytest
from dotenv import load_dotenv

from agentscope_runtime.engine.services.rag_service import LangChainRAGService

if os.path.exists("../../.env"):
    load_dotenv("../../.env")


def load_docs():
    import bs4
    from langchain_community.document_loaders import WebBaseLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    loader = WebBaseLoader(
        web_paths=(
            "https://lilianweng.github.io/posts/2023-06-23-agent/",
            "https://lilianweng.github.io/posts/2023-03-15-prompt"
            "-engineering/",
        ),
        bs_kwargs={
            "parse_only": bs4.SoupStrainer(
                class_=("post-content", "post-title", "post-header"),
            ),
        },
    )
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200,
    )

    docs = text_splitter.split_documents(documents)
    return docs


@pytest.mark.asyncio
async def test_from_docs():
    docs = load_docs()
    rag_service = LangChainRAGService(docs=docs)

    ret_docs = await rag_service.retrieve(
        "What is self-reflection of an AI Agent?",
    )
    assert len(ret_docs) == 1
    assert ret_docs[0].page_content.startswith("Self-Reflection")


@pytest.mark.asyncio
async def test_from_db():
    rag_service = LangChainRAGService(uri="./assets/milvus_demo.db")
    ret_docs = await rag_service.retrieve(
        "What is self-reflection of an AI Agent?",
    )
    assert len(ret_docs) == 1
    assert ret_docs[0].page_content.startswith("Self-Reflection")
