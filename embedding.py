from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")

embedding=GoogleGenerativeAIEmbeddings(
   model="gemini-embedding-001",
   google_api_key=GOOGLE_API_KEY
)