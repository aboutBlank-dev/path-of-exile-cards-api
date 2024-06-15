from dotenv import load_dotenv
from supabase import create_client, Client
import os

#Load the environment variables
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
db = create_client(url, key)