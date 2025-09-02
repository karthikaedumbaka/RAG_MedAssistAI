import os
from pinecone import Pinecone
from dotenv import load_dotenv

# Load your .env file
load_dotenv()

pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
print("Available indexes:", pc.list_indexes())
