import uuid, time
import threading
MCP_STORE = {}
_LOCK = threading.Lock()

def create_mcp(state, profiles, task_state, tools):
    mcp_id = str(uuid.uuid4())
    with _LOCK:
        MCP_STORE[mcp_id] = {'neighborhood_state':state, 'user_profiles':profiles, 'task_state':task_state, 'tool_manifest':tools, 'created_at':time.time()}
    return mcp_id

def get_mcp(mcp_id):
    with _LOCK:
        return MCP_STORE.get(mcp_id)

