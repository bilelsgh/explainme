"""
DeepSeek Client using langchain
"""
from langchain_openai.chat_models.base import BaseChatOpenAI

from clients.llmclient import LLMClient


class DeepSeekClient(LLMClient):
    """
    Client to call DeepSeek API
    """

    def __init__(self, key: str, model_name: str, prompt_instruction: str = ""):
        """
        Initialize the DeepSeekClient with API key, prompt instruction, and model name.

        :param key: API key for DeepSeek
        :param prompt_instruction: Custom prompt instruction for the conversation
        :param model_name: Name of the DeepSeek model to use
        """

        super().__init__(model_name)
        self.client = BaseChatOpenAI(
            model=model_name,
            openai_api_key=key,
            openai_api_base="https://api.deepseek.com",
            max_tokens=1024,
        )

        self._init_conversation_context(prompt_instruction)

    def ask(self, user_input: str, context: str = "") -> str:
        """
        Ask something to the model

        :param user_input: Prompt for the model
        :param context: (str) Additional instructions
        :return response: Model answer
        """

        user_args = {"input": user_input}

        if context:
            user_args["context"] = context

        try:
            response = self.conversation_chain.run(user_args)
            return response
        except Exception as e:
            return f"An error occurred: {e}"
