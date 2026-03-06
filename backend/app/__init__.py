# Backend package initialization

from .interop import HandshakeProtocol, ExternalAgentWrapper, verify_attestation

__all__ = [
    "HandshakeProtocol",
    "ExternalAgentWrapper",
    "verify_attestation"
]
