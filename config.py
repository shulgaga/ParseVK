import os

from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN_VK = os.getenv('ACCESS_TOKEN_VK')
API_TOKEN_VK = os.getenv('API_TOKEN_VK')
VERSION = os.getenv('VERSION')
BOT_API_KEY = os.getenv('BOT_API_KEY')
METHOD_GROUP_SEARCH = os.getenv('METHOD_GROUP_SEARCH')
METHOD_WALL_SEARCH = os.getenv('METHOD_WALL_SEARCH')