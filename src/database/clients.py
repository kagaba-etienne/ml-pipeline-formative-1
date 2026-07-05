import os
from generated.postgres_client import Prisma
from dotenv import load_dotenv

# Ensure environment variables are loaded
load_dotenv()

# We initialize a global Prisma instance for the application to reuse.
# Connection and disconnection lifecycle will be handled in main.py.
postgres_client = Prisma()
