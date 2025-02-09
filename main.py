from config.config import client_type, key
from helpers.utils import get_llm_client

if __name__ == "__main__":

    client = get_llm_client(client_type, key)

    response1 = client.ask("Quelle est la capitale de la France ?")
    print("Assistant:", response1)  # expected: "La capitale de la France est Paris."

    response2 = client.ask("Quel est la population de cette ville ?")
    print(
        "Assistant:", response2
    )  # expected: Données sur la population de Paris (the history of the conversation is tracked)
