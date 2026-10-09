"""Agent API Governance & RBAC Policy Proxy.
100% Python Standard Library.
"""

import json

class AgentGovernanceRBACProxy:
    """Enforces fine-grained permissions on agent tool calls and data access scopes."""
    
    ROLE_PERMISSIONS = {
        "viewer_agent": ["read_dom", "list_directory", "query_database"],
        "developer_agent": ["read_dom", "write_file", "run_test", "commit_patch"],
        "deployer_agent": ["read_dom", "write_file", "deploy_release", "rollback_service"]
    }
    
    SENSITIVE_PATTERNS = ["DROP TABLE", "DELETE FROM", "rm -rf", "api_key=", "TOKEN="]
    
    @classmethod
    def evaluate_tool_call(cls, agent_role: str, tool_name: str, arguments: dict) -> dict:
        allowed_tools = cls.ROLE_PERMISSIONS.get(agent_role, [])
        if tool_name not in allowed_tools:
            return {
                "allowed": False,
                "status": "DENIED_RBAC",
                "message": f"Role '{agent_role}' is not authorized to invoke tool '{tool_name}'."
            }
            
        arg_str = json.dumps(arguments)
        for pattern in cls.SENSITIVE_PATTERNS:
            if pattern in arg_str:
                return {
                    "allowed": False,
                    "status": "DENIED_SAFETY_POLICY",
                    "message": f"Dangerous pattern '{pattern}' prohibited by runtime security policy."
                }
                
        return {
            "allowed": True,
            "status": "AUTHORIZED",
            "message": f"Tool '{tool_name}' execution permitted for role '{agent_role}'."
        }
