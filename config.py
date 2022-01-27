import os

from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN_VK = os.getenv('ACCESS_TOKEN_VK')
VERSION = os.getenv('VERSION')
BOT_API_KEY = os.getenv('BOT_API_KEY')
METHOD_WALL_SEARCH = os.getenv('METHOD_WALL_SEARCH')
SECRET_KEY = os.getenv('SECRET_KEY')