"""
Utils functions for the whole project
"""
from clients.deep_seek import DeepSeekClient
from clients.llmclient import AVAILABLE_MODELS, AvailableModel, LLMClient
from clients.mistral import MistralClient


def get_llm_client(
    model: AvailableModel, key: str, prompt_instruction: str = ""
) -> LLMClient:
    """
    Get the LLM client to start chatting

    :param key: API key
    :param model: Desired model
    :param prompt_instruction: Instruction to give to the LLM
    :return:
    """

    clients = {
        "DEEPSEEK": DeepSeekClient,
        "MISTRAL": MistralClient,
    }

    args_ = {
        "model_name": model.name,
        "key": key,
        "prompt_instruction": prompt_instruction,
    }

    return clients[model.model_family](**args_)


def get_model_type_from_input(user_input: str) -> AvailableModel:
    """
    Get LLM client from user input

    :param user_input: LLM Family
    :return: AvailableClients
    """

    try:
        return AVAILABLE_MODELS[user_input]
    except KeyError:
        raise ValueError(f"Invalid client: {user_input}")
