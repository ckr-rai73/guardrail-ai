import json
import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.exceptions import InvalidSignature

def generate_agent_keypair():
    """Generates an ED25519 keypair for an agent."""
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    
    # Serialize to PEM for storage/transmission
    priv_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    pub_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    return priv_bytes.decode('utf-8'), pub_bytes.decode('utf-8')

def sign_agent_payload(private_key_pem: str, payload: dict) -> str:
    """Signs a dict payload using the agent's ED25519 private key."""
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode('utf-8'),
        password=None
    )
    
    # Canonicalize the payload before signing
    canonical_payload = json.dumps(payload, sort_keys=True).encode('utf-8')
    
    signature = private_key.sign(canonical_payload)
    return base64.b64encode(signature).decode('utf-8')

def verify_agent_payload(public_key_pem: str, payload: dict, signature_b64: str) -> bool:
    """Verifies that the payload was signed by the upstream agent."""
    public_key = serialization.load_pem_public_key(
        public_key_pem.encode('utf-8')
    )
    
    canonical_payload = json.dumps(payload, sort_keys=True).encode('utf-8')
    signature = base64.b64decode(signature_b64)
    
    try:
        public_key.verify(signature, canonical_payload)
        return True
    except InvalidSignature:
        return False
