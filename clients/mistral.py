from langchain_mistralai import ChatMistralAI

from clients.llmclient import LLMClient


class MistralClient(LLMClient):
    """
    Client to call Mistral API
    """

    def __init__(self, key: str, model_name: str, prompt_instruction: str = ""):
        """
        Initialize the MistralClient with API key, prompt instruction, and model name.

        :param key: API key for Mistral
        :param prompt_instruction: Custom prompt instruction for the conversation
        :param model_name: Name of the Mistral model to use
        """
        super().__init__(model_name)
        self.client = ChatMistralAI(
            model=model_name,
            temperature=0.5,
            max_retries=3,
        )

        self._init_conversation_context(prompt_instruction)

    def ask(self, user_input: str, context: str = "") -> str:
        """
        Ask something to the model.

        :param user_input: Prompt for the model
        :param context: Additional instructions or context for the model
        :return: Model answer
        """
        user_args = {"input": user_input}

        if context:
            user_args["context"] = context

        try:
            response = self.conversation_chain.run(user_args)
            self.memory.clear()
            return response
        except Exception as e:
            return f"An error occurred: {e}"
