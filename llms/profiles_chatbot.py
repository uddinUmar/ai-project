import os
from mistralai import Mistral
from dotenv import load_dotenv

from llms.db_profiles import Profiles

load_dotenv()

api_key = os.getenv('MISTRAL_API_KEY')
if not api_key:
    raise ValueError("MISTRAL_API_KEY is not set in the environment.")

user_input = input("user: ")

class ChatBotOnProfiles:
    def __init__(self, api_key, user_input):
        self.api_key = api_key
        self.user_input = user_input
        self.data = Profiles().all_profiles()

    def connect_ai(self):
        model = "mistral-large-latest"
        client = Mistral(api_key=self.api_key)

        # Format profiles data as a readable string
        profile_texts = []
        for profile in self.data:
            highlighted_skills = ', '.join([skill.get('name', '') for skill in profile.get('highlightedSkills', [])])
            additional_skills = ', '.join([skill.get('name', '') for skill in profile.get('additionalSkill', [])])
            text = text = f"""
            Name: {profile.get('firstName', '')} {profile.get('lastName', '')}
            Summary: {profile.get('carrierSummary', '')}
            Highlighted Skills: {highlighted_skills}
            Additional Skills: {additional_skills}
            Location: {profile.get('currentLocation', '')}
            """
            profile_texts.append(text)

        system_message = "Here are some candidate profiles:\n" + "\n---\n".join(profile_texts[:5])  # Limit to first 5 for token safety

        chat_response = client.chat.complete(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": system_message
                },
                {
                    "role": "user",
                    "content": self.user_input,
                },
            ]
        )

        print("\nAI:", chat_response.choices[0].message.content)


if __name__ == '__main__':
    bot = ChatBotOnProfiles(api_key, user_input)
    bot.connect_ai()
