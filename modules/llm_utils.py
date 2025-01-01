from langchain_community.chat_models import ChatOpenAI

def initialize_openai(api_key, base_url, model_name="openai/gpt-3.5-turbo"):
    """
    Initializes the OpenAI client
    """
    return ChatOpenAI(api_key=api_key, base_url=base_url, temperature=0.2)
