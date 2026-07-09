import os
from typing import Optional

import langchain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.base_language import BaseLanguageModel


def detect_provider(model: str) -> str:
    if model.startswith("claude"):
        return "anthropic"
    if model.startswith("gpt-") or model.startswith("text-"):
        return "openai"
    raise ValueError(
        f"Cannot detect LLM provider for model '{model}'. "
        "Use a claude-* or gpt-* model name."
    )


def get_api_key(provider: str, api_key: Optional[str] = None) -> Optional[str]:
    if api_key:
        return api_key
    if provider == "anthropic":
        return os.getenv("ANTHROPIC_API_KEY")
    if provider == "openai":
        return os.getenv("OPENAI_API_KEY")
    return None


def make_llm(
    model: str,
    temp: float,
    api_key: Optional[str] = None,
    streaming: bool = False,
    provider: Optional[str] = None,
) -> BaseLanguageModel:
    if provider is None:
        provider = detect_provider(model)

    key = get_api_key(provider, api_key)
    callbacks = [StreamingStdOutCallbackHandler()] if streaming else []

    if provider == "anthropic":
        from langchain.chat_models import ChatAnthropic

        return ChatAnthropic(
            model=model,
            temperature=temp,
            streaming=streaming,
            callbacks=callbacks,
            anthropic_api_key=key,
        )

    if model.startswith("gpt-3.5-turbo") or model.startswith("gpt-4"):
        return langchain.chat_models.ChatOpenAI(
            temperature=temp,
            model_name=model,
            request_timeout=1000,
            streaming=streaming,
            callbacks=callbacks,
            openai_api_key=key,
        )

    if model.startswith("text-"):
        return langchain.OpenAI(
            temperature=temp,
            model_name=model,
            streaming=streaming,
            callbacks=callbacks,
            openai_api_key=key,
        )

    raise ValueError(f"Invalid model name: {model}")


def make_embeddings(openai_api_key: Optional[str] = None):
    key = openai_api_key or os.getenv("OPENAI_API_KEY")
    if key:
        from langchain.embeddings.openai import OpenAIEmbeddings

        return OpenAIEmbeddings(openai_api_key=key)

    from langchain.embeddings import HuggingFaceEmbeddings

    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
