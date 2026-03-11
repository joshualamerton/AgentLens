from core.event_stream import publish_event
import time

def instrument_tool(agent_name, tool_name, func):

    def wrapper(*args, **kwargs):

        event = {
            "event": "tool_call",
            "agent": agent_name,
            "tool": tool_name,
            "input": args,
            "timestamp": time.time()
        }

        publish_event(event)

        result = func(*args, **kwargs)

        publish_event({
            "event": "tool_result",
            "agent": agent_name,
            "tool": tool_name,
            "result": result,
            "timestamp": time.time()
        })

        return result

    return wrapper
