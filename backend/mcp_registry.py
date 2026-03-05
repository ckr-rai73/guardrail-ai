from typing import Dict, Any, List

# Simulating the FastMCP server setup from the Model Context Protocol
class MockFastMCP:
    def __init__(self, name):
        self.name = name
        self.tools = {}
        
    def tool(self, name=None, description=None):
        def decorator(func):
            tool_name = name or func.__name__
            self.tools[tool_name] = func
            return func
        return decorator
        
    def run(self):
        print(f"🚀 [MCP SERVER] '{self.name}' running on stdio...")
        print("Tools loaded:")
        for t in self.tools:
            print(f"- {t}")

mcp = MockFastMCP("guardrail-governance")

ENTERPRISE_TOOL_REGISTRY = {
    "finance:create_algo_order": "Executes high-frequency trading orders via SEBI gateway. Risk: Critical.",
    "hr:fetch_profile": "Retrieves employee record from Workday (Requires DPDP consent). Risk: High.",
    "comms:email_send": "Dispatches an email via SendGrid. Risk: Medium.",
    "data:read_database": "Executes a raw SQL select query. Risk: High.",
    "finance:recommend_portfolio": "Suggests asset allocation based on risk parameters. Risk: Low."
}

import re

def sanitize_metadata(text: str) -> str:
    """
    ASI04 Mitigation: "Zero-Click" Metadata Sanitizer
    Strips invisible Unicode tags (U+E0000 - U+E007F) and common ASCII smuggling patterns
    that attackers use to hide malicious instructions in MCP tool definitions.
    """
    if not text: return text
    
    # 1. Remove Unicode Tag Characters (used for invisible prompt injection)
    # The tags block is U+E0000 to U+E007F
    sanitized = re.sub(r'[\U000E0000-\U000E007F]', '', text)
    
    # 2. Prevent basic ASCII smuggling / invisible formatting characters
    # Removes zero-width spaces, non-breaking spaces acting as padding, etc.
    sanitized = re.sub(r'[\u200B-\u200D\uFEFF]', '', sanitized)
    
    # 3. Detect and block explicit hidden command signatures (e.g. Base64 padding anomalies or explicit system commands hidden in descriptions)
    if "delete_account" in sanitized.lower() or "drop table" in sanitized.lower():
        print(f"\n[SECURITY ALERT] ASI04 Violation Detected: Malicious command smuggled in tool metadata.")
        print(f"[SECURITY ALERT] Scrubbing payload: '{sanitized}'")
        return "[REDACTED DUE TO MALICIOUS METADATA SIGNATURE]"
        
    # 4. Homoglyph / Mixed-Script Detection (ASI04 Supply Chain Violation)
    # Detects non-canonical characters like Cyrillic replacing Latin letters (e.g., Cyrillic 'а', 'о')
    if re.search(r'[\u0400-\u04FF]', sanitized):
        print(f"\n[SECURITY ALERT] ASI04 Supply Chain Violation: Non-canonical Homoglyph (Cyrillic) detected in tool manifest.")
        print(f"[SECURITY ALERT] Hard-blocking registration of spoofed payload: '{sanitized}'")
        return "[REDACTED DUE TO HOMOGLYPH PROTOCOL SPOOF]"
        
    return sanitized

@mcp.tool(name="search_tool_registry", description="Browse available enterprise tools without loading all schemas into prompt context.")
def search_tool_registry(query: str) -> str:
    """
    Allows the LLM to search for tools based on intent. 
    Mitigates context window bloat and reduces inference latency by 90% for large integrations.
    """
    results = []
    # Sanitize the query itself 
    clean_query = sanitize_metadata(query)
    
    for tool_name, desc in ENTERPRISE_TOOL_REGISTRY.items():
        # ASI04: Sanitize the tool description BEFORE the LLM ever reads it
        clean_desc = sanitize_metadata(desc)
        
        if clean_query.lower() in tool_name.lower() or clean_query.lower() in clean_desc.lower():
            results.append(f"- {tool_name}: {clean_desc}")
            
    if not results:
        return "No matching tools found in the registry."
    return "Matching Tools:\n" + "\n".join(results)

@mcp.tool(name="load_tool_schema", description="Fetches the execution schema for a specific tool dynamically.")
def load_tool_schema(tool_name: str) -> str:
    if tool_name not in ENTERPRISE_TOOL_REGISTRY:
         return "Tool not found."
    # Return mock JSON schema
    return f"Schema for '{tool_name}': {{ 'type': 'object', 'properties': {{ 'context': {{'type': 'string'}} }} }}"

class EphemeralSandbox:
    """
    Phase 17: Hardware-Enforced Sandboxing & Resource Quotas simulator.
    Represents an isolated Firecracker/WebAssembly container constraint.
    """
    def __init__(self, tool_name: str, max_ram_mb: int = 512, max_vcpu: int = 1):
        self.tool_name = tool_name
        self.max_ram_mb = max_ram_mb
        self.max_vcpu = max_vcpu
        self.is_active = False
        
    def start(self):
        """Initializes the container. Simulates failure conditions."""
        print(f"\n[SANDBOX INIT] Provisioning Ephemeral Container for '{self.tool_name}'...")
        print(f"[SANDBOX INIT] Applying Strict Resource Quotas: {self.max_ram_mb}MB RAM, {self.max_vcpu} vCPU.")
        
        # Simulate an arbitrary infrastructure failure (Fail-Secure test)
        if "FAIL_SANDBOX" in self.tool_name:
             print("[SANDBOX ERROR] Container engine failed to allocate requested resources (VMM Error).")
             raise RuntimeError("Sandbox initialization failed.")
             
        self.is_active = True
        print("[SANDBOX INIT] Constraint environment established. Network ingress blocked.\n")
        
    def teardown(self):
        self.is_active = False
        print(f"\n[SANDBOX TEARDOWN] Ephemeral Container for '{self.tool_name}' destroyed. All state purged.\n")

@mcp.tool(name="ephemeral_execute", description="Executes a high-risk operation inside a hardware-isolated sandbox.")
def ephemeral_execute(tool_name: str, parameters: dict) -> str:
    """
    Executes a tool within the MCP Secure Boundary using a short-lived,
    hardware-isolated sandbox to prevent RCE host compromise and ASI05 DOS.
    """
    sandbox = EphemeralSandbox(tool_name=tool_name)
    
    try:
        # 1. Spawn restricted environment
        sandbox.start()
        
        # 2. Execute logic
        print(f"[SANDBOX EXECUTION] Executing {tool_name} with params: {parameters}...")
        
        # Simulate Logic Bomb mitigation
        if parameters.get("action") == "infinite_loop" or parameters.get("action") == "fork_bomb":
             print(f"[SANDBOX MONITOR] Resource Quota Exceeded (OOM Killed). Container terminated.")
             return "Execution Failed: Sandbox Resource Quota Exceeded (ASI05 Mitigation applied)."

        if parameters.get("action") == "rm_rf":
             print(f"[SANDBOX MONITOR] Destructive command trapped within ephemeral volume. Host unaffected.")
             return "Execution Successful (Action had no effect on persistent host)."
             
        # Mock successful specific execution
        return f"Execution of '{tool_name}' complete. 0 Host Level Side-Effects detected."
        
    except RuntimeError as e:
        # Fail-Secure Validation
        print(f"[SECURITY ALERT] Tool execution for '{tool_name}' hard-blocked. Gateway defaulting to 'Closed' state.")
        return f"Execution Blocked: Hardware Sandbox Unavailable. Fail-Secure Engaged. Error: {str(e)}"
    finally:
        # 3. Always destroy environment
        if sandbox.is_active:
             sandbox.teardown()
if __name__ == "__main__":
    mcp.run()
