"""Example usage for Agent Governance RBAC Proxy."""
from client import AgentGovernanceRBACProxy

if __name__ == "__main__":
    res = AgentGovernanceRBACProxy.evaluate_tool_call(
        "developer_agent",
        "write_file",
        {"target": "app.py", "content": "print('hello')"}
    )
    print("Authorization Status:", res["status"])
    print("Allowed:", res["allowed"])
