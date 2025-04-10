import os

from pymongo import MongoClient
import certifi
from dotenv import load_dotenv

load_dotenv()


mongoClient = MongoClient(
    os.getenv('APP_DEV_STRING'),
    ssl=True,
    tlsCAFile=certifi.where(),
    maxPoolSize=5,  # Maximum number of connections in the pool
    minPoolSize=5,  # Minimum
)

class Profiles:
    def __init__(self):
        self.db = mongoClient.get_database()
        self.profile = self.db.get_collection("profiles")

    def all_profiles(self):
        return self.profile.find(
            {},
            {
                "firstName": 1,
                "lastName": 1,
                "carrierSummary": 1,
                "highlightedSkills": 1,
                "additionalSkill": -1,
            }
        )
