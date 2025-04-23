from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableConfig
from models.configuration import Configuration


_llm = ChatOpenAI(
    model_name="gpt-4",
    temperature=0,
)

def get_llm():
    return _llm

def _ensure_configurable(config: RunnableConfig) -> Configuration:
    """Get Params that configure the search algorithm."""
    configurable = config.get("configurable", {})
    return {
        **configurable,
        "max_depth" : configurable.get("max_depth", 10),
        "threshold" : config.get("threshold", 0.6),
        "k": configurable.get("k", 5),
        "beam_size" : configurable.get("beam_size", 3),
    }
