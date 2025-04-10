import getpass
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage , HumanMessage

load_dotenv()

if __name__ == '__main__':
    if not os.environ.get("MISTRAL_API_KEY"):
        os.environ["MISTRAL_API_KEY"] = getpass.getpass("Enter API key for Mistral AI: ")

    model = init_chat_model(model="mistral-large-latest", model_provider="mistralai")

    Messages = [
        SystemMessage("Java and Python expert"),
        HumanMessage("give me one Question related to my skills")
    ]

    for tokens in model.stream(Messages):
        print(tokens.content,end="")


        # human message stored in array