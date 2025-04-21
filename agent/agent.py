from langchain_openai import ChatOpenAI

# TODO: Pool Of LLMs
_llm = ChatOpenAI(
    model_name="gpt-4",
    temperature=0,
)

def get_llm():
    return _llm
