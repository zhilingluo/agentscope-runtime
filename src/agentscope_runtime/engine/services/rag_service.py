# -*- coding: utf-8 -*-

from langchain_community.embeddings import DashScopeEmbeddings
from langchain_milvus import Milvus

from .base import ServiceWithLifecycleManager


class RAGService(ServiceWithLifecycleManager):
    """
    RAG Service
    """


DEFAULT_URI = "milvus_demo.db"


class LangChainRAGService(RAGService):
    """
    RAG Service using LangChain
    """

    def __init__(self, uri=None, docs=None):
        self.embeddings = DashScopeEmbeddings()
        self.vectorstore = None

        if uri:
            self.uri = uri
            self.from_db()
        elif docs:
            self.uri = DEFAULT_URI
            self.from_docs(docs)
        else:
            raise ValueError("Either uri or docs must be provided.")

    def from_docs(self, docs=None):
        if docs is None:
            docs = []

        self.vectorstore = Milvus.from_documents(
            documents=docs,
            embedding=self.embeddings,
            connection_args={
                "uri": self.uri,
            },
            drop_old=False,
        )

    def from_db(self):
        self.vectorstore = Milvus(
            embedding_function=self.embeddings,
            connection_args={"uri": self.uri},
            index_params={"index_type": "FLAT", "metric_type": "L2"},
        )

    async def retrieve(self, query: str, k: int = 1) -> list:
        if self.vectorstore is None:
            raise ValueError(
                "Vector store not initialized. Call build_index first.",
            )
        return self.vectorstore.similarity_search(query, k=k)

    async def start(self) -> None:
        """Starts the service."""
        self.embeddings = DashScopeEmbeddings()
        self.vectorstore = None

    async def stop(self) -> None:
        """Stops the service."""

    async def health(self) -> bool:
        """Checks the health of the service."""
        return True
