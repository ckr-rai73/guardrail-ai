# Initialize auth package
import os
import uuid
from datetime import datetime, timedelta
import secrets
from fastapi import HTTPException, Security, Request
from fastapi.security import OAuth2PasswordBearer
import jwt

# Mock OAuth 2.1 PKCE Configuration
SECRET_KEY = os.getenv("JWT_SECRET", secrets.token_hex(32))
ALGORITHM = "HS256"
# In a real PKCE flow, the token comes from an Authorization server
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# In-memory store for task-scoped token validation
# Maps a specific token to an agent task scope (action + agent_id)
_task_token_registry = {}

def create_task_scoped_token(agent_id: str, action_scope: str, expires_delta_minutes: int = 15):
    """
    Simulates granting a short-lived, task-scoped OAuth 2.1 token to an agent.
    This prevents ASI03 Privilege Abuse by ensuring tokens die quickly and only work for 1 task.
    """
    expire = datetime.utcnow() + timedelta(minutes=expires_delta_minutes)
    
    # Payload restricted specifically to the agent and the exact tool/action
    payload = {
        "sub": agent_id,
        "scope": action_scope, # e.g. "finance:execute_order"
        "exp": expire,
        "jti": str(uuid.uuid4()) # JWT ID for revocation
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    _task_token_registry[payload["jti"]] = payload
    return token

async def verify_task_scoped_token(request: Request, token: str = Security(oauth2_scheme)):
    """
    Middleware dependency to verify that the request has a valid task-scoped token.
    Throws a 401/403 if the token is invalid, expired, or wrong scope.
    """
    try:
        # Decode and verify token signature and expiration
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        jti = payload.get("jti")
        scope = payload.get("scope")
        
        # Check against in-memory registry (simulating a token introspection endpoint)
        if jti not in _task_token_registry:
            raise HTTPException(status_code=401, detail="Token revoked or not found in registry.")
            
        # Optional: Add scope validation based on request path here
        if request.url.path == "/api/finance/order" and scope != "finance:execute_order":
             raise HTTPException(status_code=403, detail=f"Token Scope '{scope}' does not authorize access to this endpoint.")
             
        # Inject the validated payload into the request state for downstream use
        request.state.agent_token_payload = payload
        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Task-Scoped Token has expired. Agents must request a new token per task.")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate token signature.")
