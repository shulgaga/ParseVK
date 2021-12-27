import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
API_TOKEN = os.getenv('API_TOKEN')
VERSION = os.getenv('VERSION')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')