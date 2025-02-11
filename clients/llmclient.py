from abc import ABC, abstractmethod
from dataclasses import dataclass

from langchain.chains.conversation.base import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate


class LLMClient(ABC):
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.client = None
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", input_key="input", return_messages=True
        )

    @abstractmethod
    def ask(self, prompt: str, context: str = "") -> str:
        raise NotImplementedError

    def _init_conversation_context(self, prompt_instruction: str):
        """
        Configuration of every component needed to start the conversation.

        :param prompt_instruction: Custom prompt instruction for the conversation
        """

        if not prompt_instruction:
            prompt_template = """
            Here is the history of the conversation:
            {chat_history}

            User: {input}
            Assistant:
            """
        else:
            prompt_template = prompt_instruction
        input_variables = ["input", "chat_history"]

        prompt = PromptTemplate(
            template=prompt_template, input_variables=input_variables
        )

        self.conversation_chain = ConversationChain(
            llm=self.client, memory=self.memory, prompt=prompt, verbose=True
        )


@dataclass
class AvailableModel:
    name: str
    model_family: str


AVAILABLE_MODELS = {
    "mistral-large": AvailableModel(
        model_family="MISTRAL", name="mistral-large-latest"
    ),
    "codestral-latest": AvailableModel(model_family="MISTRAL", name="codestral-latest"),
    "deepseek-r1": AvailableModel(model_family="DEEPSEEK_R1", name="deepseek-chat"),
}
