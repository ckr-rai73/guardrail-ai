"""Abstract base for knowledge sources and concrete implementations."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class KnowledgeSource(ABC):
    """Base class for all knowledge sources."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    async def verify(self, claim: str, context: Optional[Dict] = None) -> bool:
        """Return True if the claim is supported by this source."""
        pass


class VectorKnowledgeSource(KnowledgeSource):
    """Knowledge source backed by a vector database (Chroma, Pinecone, etc.)."""

    def __init__(self, name: str, collection, embedding_model):
        super().__init__(name)
        self.collection = collection
        self.embedding_model = embedding_model

    async def verify(self, claim: str, context: Optional[Dict] = None) -> bool:
        # For simulation: embed claim, query top 1, compute similarity
        # This is a placeholder; real implementation would use actual vector DB
        # For Phase 116, we'll mock it to return True for claims containing "fact"
        if "fact" in claim.lower():
            return True
        return False


class APIKnowledgeSource(KnowledgeSource):
    """Knowledge source that calls an external API (e.g., knowledge graph, weather service)."""

    def __init__(self, name: str, api_url: str, api_key: Optional[str] = None):
        super().__init__(name)
        self.api_url = api_url
        self.api_key = api_key

    async def verify(self, claim: str, context: Optional[Dict] = None) -> bool:
        # Placeholder: mock implementation
        return "api" in claim.lower()
