import getpass
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage , HumanMessage

from llms.db_profiles import Profiles

load_dotenv()

class LangChainProfiles:
    def __init__(self):
        self.data = Profiles().all_profiles()
        print(self.data)

    def message_generate(self):
        profiles=[]
        for profile in self.data:
            profiles.append(profile)
        Messages = [
            SystemMessage(f"Give answers related to this ;here is all the profiles :{profiles}"),
            HumanMessage("give me Java expert Atik's details ")
        ]
        return Messages


if __name__ == '__main__':
    if not os.environ.get("MISTRAL_API_KEY"):
        os.environ["MISTRAL_API_KEY"] = getpass.getpass("Enter API key for Mistral AI: ")

    model = init_chat_model(model="mistral-large-latest", model_provider="mistralai")

    Messages = LangChainProfiles().message_generate()

    for tokens in model.stream(Messages):
        print(tokens.content,end="")


