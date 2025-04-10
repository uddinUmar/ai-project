import getpass
import os
import json
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

from llms.db_profiles import Profiles

load_dotenv()

class LangChainProfiles:
    def __init__(self):
        self.data = Profiles().all_profiles()  # This should return a list of profile dicts

    def generate_prompt(self, question: str):
        profiles=[]
        for profile in self.data:
            profiles.append(profile)
        profiles_json = profiles

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are an assistant who answers based on the following developer profiles:\n{profiles}"),
            ("user", "{question}")
        ])

        return prompt_template.invoke({
            "profiles": profiles_json,
            "question": question
        })

if __name__ == '__main__':
    if not os.environ.get("MISTRAL_API_KEY"):
        os.environ["MISTRAL_API_KEY"] = getpass.getpass("Enter API key for Mistral AI: ")

    model = init_chat_model(model="mistral-large-latest", model_provider="mistralai")

    question = "Give me Java expert Atik's details."
    prompt = LangChainProfiles().generate_prompt(question)


    for token in model.stream(prompt):
        print(token.content, end="")