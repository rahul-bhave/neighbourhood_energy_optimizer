import uuid, time
def envelope(sender, to, mtype, payload, mcp_id=None):
    return {
        'msg_id': str(uuid.uuid4()),
        'from': sender,
        'to': to,
        'type': mtype,
        'mcp_context_id': mcp_id,
        'payload': payload,
        'timestamp': time.time()
    }
