# core/instrumentation.py

from typing import Any, Callable, Dict, Optional
from agentlens.core.event_stream import EventStream

class AgentLensWrapper:
    def __init__(self, agent: Any, event_stream: EventStream):
        self.agent = agent
        self.event_stream = event_stream

    def emit_event(self, event_type: str, data: Dict[str, Any]):
        self.event_stream.emit(event_type, data)

    def __getattr__(self, name: str):
        attr = getattr(self.agent, name)
        if callable(attr):
            def wrapper(*args, **kwargs):
                result = attr(*args, **kwargs)
                self.emit_event(f"{name}_called", {"args": args, "kwargs": kwargs})
                return result
            return wrapper
        return attr

def instrument(agent: Any, event_stream: EventStream) -> Any:
    if isinstance(agent, langchain.Agent):
        return LangChainWrapper(agent, event_stream)
    elif isinstance(agent, autogen.Agent):
        return AutoGenWrapper(agent, event_stream)
    else:
        raise ValueError("Unsupported agent type")

class LangChainWrapper(AgentLensWrapper):
    def __init__(self, agent: langchain.Agent, event_stream: EventStream):
        super().__init__(agent, event_stream)

    def run(self, *args, **kwargs):
        self.emit_event("model_prompt", {"prompt": args[0]})
        result = self.agent.run(*args, **kwargs)
        self.emit_event("model_response", {"response": result})
        return result

class AutoGenWrapper(AgentLensWrapper):
    def __init__(self, agent: autogen.Agent, event_stream: EventStream):
        super().__init__(agent, event_stream)

    def run(self, *args, **kwargs):
        self.emit_event("model_prompt", {"prompt": args[0]})
        result = self.agent.run(*args, **kwargs)
        self.emit_event("model_response", {"response": result})
        return result