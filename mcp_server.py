"""MCP server for Agent Governance RBAC Proxy."""
import sys
import json
from client import AgentGovernanceRBACProxy

def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [{
                "name": "authorize_tool_call",
                "description": "Verifies RBAC privileges and security constraints for agent actions",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "agent_role": {"type": "string"},
                        "tool_name": {"type": "string"},
                        "arguments": {"type": "object"}
                    },
                    "required": ["agent_role", "tool_name", "arguments"]
                }
            }]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        if params.get("name") == "authorize_tool_call":
            args = params.get("arguments", {})
            res = AgentGovernanceRBACProxy.evaluate_tool_call(
                args.get("agent_role", ""),
                args.get("tool_name", ""),
                args.get("arguments", {})
            )
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
