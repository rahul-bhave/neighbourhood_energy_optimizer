import uuid, time
MCP_STORE = {}
def create_mcp(state, profiles, task_state, tools):
    mcp_id = str(uuid.uuid4())
    MCP_STORE[mcp_id] = {
        'neighborhood_state': state,
        'user_profiles': profiles,
        'task_state': task_state,
        'tool_manifest': tools,
        'created_at': time.time()
    }
    return mcp_id
def get_mcp(mcp_id):
    return MCP_STORE.get(mcp_id)
