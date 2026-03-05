"""
Phase 103: RAG-Enhanced Dynamic Policy Enforcement.
In-memory vector database with cosine similarity for regulatory chunk retrieval.
Ensures policy engine always reflects latest regulations without code changes.
"""
import hashlib
import math
import time
import uuid
from typing import Dict, Any, List, Optional, Tuple


class RegulatoryChunk:
    """A single chunk of regulatory text with its embedding."""

    def __init__(self, chunk_id: str, source: str, section: str, text: str,
                 version: int = 1, metadata: Optional[Dict[str, Any]] = None):
        self.chunk_id = chunk_id
        self.source = source
        self.section = section
        self.text = text
        self.version = version
        self.metadata = metadata or {}
        self.embedding = self._compute_embedding(text)
        self.indexed_at = time.time()

    @staticmethod
    def _compute_embedding(text: str, dim: int = 64) -> List[float]:
        """
        Generates a deterministic pseudo-embedding from text using SHA-256.
        In production, this would use a model like text-embedding-ada-002.
        """
        text_lower = text.lower().strip()
        h = hashlib.sha256(text_lower.encode()).hexdigest()
        raw = [int(h[i:i+2], 16) / 255.0 for i in range(0, min(len(h), dim * 2), 2)]
        # Pad to dim if needed
        while len(raw) < dim:
            ext_h = hashlib.sha256((text_lower + str(len(raw))).encode()).hexdigest()
            raw.extend([int(ext_h[i:i+2], 16) / 255.0 for i in range(0, min(len(ext_h), (dim - len(raw)) * 2), 2)])
        raw = raw[:dim]
        # L2 normalize
        norm = math.sqrt(sum(x * x for x in raw)) or 1.0
        return [x / norm for x in raw]


class RagPolicyStore:
    """
    Phase 103: In-memory vector database for regulatory text retrieval.
    Supports indexing, top-k cosine similarity search, versioning, and rollback.
    """

    # Pre-built regulatory corpus
    REGULATORY_CORPUS = [
        # EU AI Act
        {"source": "EU_AI_ACT", "section": "Article 6 - Classification Rules",
         "text": "AI systems intended for use as safety components in critical infrastructure, "
                 "including water, gas, heating and electricity supply, shall be classified as high-risk. "
                 "High-risk AI systems require conformity assessment before market placement."},
        {"source": "EU_AI_ACT", "section": "Article 9 - Risk Management",
         "text": "A risk management system shall be established, implemented, documented and maintained "
                 "in relation to high-risk AI systems. The system shall consist of a continuous iterative "
                 "process run throughout the entire lifecycle of the AI system."},
        {"source": "EU_AI_ACT", "section": "Article 13 - Transparency",
         "text": "High-risk AI systems shall be designed and developed in such a way to ensure that their "
                 "operation is sufficiently transparent to enable users to interpret the system output and "
                 "use it appropriately. An appropriate type and degree of transparency shall be ensured."},
        {"source": "EU_AI_ACT", "section": "Article 14 - Human Oversight",
         "text": "High-risk AI systems shall be designed and developed to be effectively overseen by natural "
                 "persons during the period in which the AI system is in use. Human oversight shall aim to "
                 "prevent or minimise risks to health, safety or fundamental rights."},
        {"source": "EU_AI_ACT", "section": "Article 15 - Accuracy and Robustness",
         "text": "High-risk AI systems shall be designed and developed in such a way to achieve an appropriate "
                 "level of accuracy, robustness and cybersecurity, and perform consistently in those respects "
                 "throughout their lifecycle."},

        # FINRA
        {"source": "FINRA", "section": "Rule 3110 - Supervision",
         "text": "Each member shall establish and maintain a system to supervise the activities of each "
                 "associated person that is reasonably designed to achieve compliance with applicable "
                 "securities laws and regulations. Written supervisory procedures are required."},
        {"source": "FINRA", "section": "Rule 3120 - Supervisory Control",
         "text": "Each member shall designate and specifically identify one or more principals who shall "
                 "establish, maintain, and enforce a system of supervisory control policies and procedures "
                 "that test and verify supervisory procedures."},

        # SEC
        {"source": "SEC", "section": "Rule 206(4)-7 - Compliance Programs",
         "text": "Investment advisers registered with the SEC must adopt and implement written policies "
                 "and procedures reasonably designed to prevent violation of the Investment Advisers Act. "
                 "Annual review of adequacy and effectiveness is required."},

        # RBI
        {"source": "RBI", "section": "AI Circular - Governance Framework",
         "text": "Regulated entities deploying AI models must establish a governance framework including "
                 "board-level oversight, model validation, bias testing, and explainability requirements. "
                 "AI decisions affecting customers must be auditable and reversible."},
        {"source": "RBI", "section": "AI Circular - Data Protection",
         "text": "AI systems handling customer data must comply with data localization requirements. "
                 "Personal data used for AI training must be anonymized. Consent mechanisms must be "
                 "implemented for data processing activities."},

        # SEBI
        {"source": "SEBI", "section": "LODR Reg. 17 - Board Governance",
         "text": "Listed entities must ensure that the board of directors exercises effective oversight "
                 "over AI-driven trading and advisory systems. Quarterly compliance reports on AI system "
                 "performance, risk metrics, and incident logs must be submitted."},
        {"source": "SEBI", "section": "LODR Reg. 17 - Risk Management",
         "text": "AI-based algorithmic trading systems must implement circuit breakers, position limits, "
                 "and kill switches. Real-time monitoring of AI-generated orders is mandatory. "
                 "Risk management committee must review AI system behavior quarterly."},

        # Internal Governance
        {"source": "INTERNAL", "section": "Guardrail.ai Constitution - Veto Protocol",
         "text": "All agent actions must pass through the Veto Protocol before execution. The protocol "
                 "applies binary approve/reject decisions based on safety, compliance, and ethical criteria. "
                 "No autonomous action may bypass the veto gate."},
        {"source": "INTERNAL", "section": "Guardrail.ai Constitution - Shadow Verification",
         "text": "Critical operations require dual verification through the Shadow Model. An independent "
                 "second opinion is obtained via a separate LLM to prevent single-point-of-failure in "
                 "governance decisions. Divergence triggers escalation."},
        {"source": "INTERNAL", "section": "Guardrail.ai Constitution - Audit Trail",
         "text": "Every governance decision must be recorded in the immutable Merkle-anchored audit trail. "
                 "Vector clock timestamps ensure causal ordering. PQC signatures guarantee non-repudiation. "
                 "Audit records are retained for a minimum of 7 years."},
    ]

    def __init__(self):
        self.chunks: List[RegulatoryChunk] = []
        self.current_version: int = 0
        self.version_snapshots: Dict[int, List[str]] = {}  # version -> list of chunk_ids
        self._index_corpus()

    def _index_corpus(self):
        """Indexes the pre-built regulatory corpus."""
        print("[RAG-STORE] Indexing regulatory corpus...")
        for entry in self.REGULATORY_CORPUS:
            chunk = RegulatoryChunk(
                chunk_id=f"REG-{uuid.uuid4().hex[:8].upper()}",
                source=entry["source"],
                section=entry["section"],
                text=entry["text"],
                version=0,
            )
            self.chunks.append(chunk)
        self.current_version = 1
        self.version_snapshots[0] = [c.chunk_id for c in self.chunks]
        print(f"[RAG-STORE] Indexed {len(self.chunks)} regulatory chunks (v{self.current_version})")

    def ingest_chunks(self, source: str, chunks_data: List[Dict[str, str]]) -> int:
        """
        Ingests new regulatory chunks into the store.
        Returns the new version number.
        """
        new_ids = []
        for cd in chunks_data:
            chunk = RegulatoryChunk(
                chunk_id=f"REG-{uuid.uuid4().hex[:8].upper()}",
                source=source,
                section=cd.get("section", "Unknown"),
                text=cd["text"],
                version=self.current_version,
            )
            self.chunks.append(chunk)
            new_ids.append(chunk.chunk_id)

        self.version_snapshots[self.current_version] = [c.chunk_id for c in self.chunks]
        self.current_version += 1
        print(f"[RAG-STORE] Ingested {len(new_ids)} chunks from '{source}' (v{self.current_version})")
        return self.current_version

    def retrieve_top_k(self, query: str, k: int = 3, source_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieves top-k regulatory chunks most similar to the query.
        Uses cosine similarity over hash-based embeddings.
        """
        query_embedding = RegulatoryChunk._compute_embedding(query)

        scored = []
        for chunk in self.chunks:
            if source_filter and chunk.source != source_filter:
                continue
            score = self._cosine_similarity(query_embedding, chunk.embedding)
            scored.append((score, chunk))

        scored.sort(key=lambda x: x[0], reverse=True)

        results = []
        for score, chunk in scored[:k]:
            results.append({
                "chunk_id": chunk.chunk_id,
                "source": chunk.source,
                "section": chunk.section,
                "text": chunk.text,
                "relevance_score": round(score, 4),
                "version": chunk.version,
            })

        return results

    def rollback(self, target_version: int) -> bool:
        """Rolls back the index to a specific version."""
        if target_version not in self.version_snapshots:
            print(f"[RAG-STORE] Version {target_version} not found. Cannot rollback.")
            return False

        valid_ids = set(self.version_snapshots[target_version])
        self.chunks = [c for c in self.chunks if c.chunk_id in valid_ids]
        self.current_version = target_version + 1
        print(f"[RAG-STORE] Rolled back to v{target_version}. {len(self.chunks)} chunks active.")
        return True

    def get_stats(self) -> Dict[str, Any]:
        sources = {}
        for c in self.chunks:
            sources[c.source] = sources.get(c.source, 0) + 1
        return {
            "total_chunks": len(self.chunks),
            "current_version": self.current_version,
            "sources": sources,
            "versions_available": sorted(self.version_snapshots.keys()),
        }

    @staticmethod
    def _cosine_similarity(a: List[float], b: List[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a)) or 1.0
        norm_b = math.sqrt(sum(x * x for x in b)) or 1.0
        return dot / (norm_a * norm_b)


# Singleton
GLOBAL_RAG_POLICY_STORE = RagPolicyStore()
