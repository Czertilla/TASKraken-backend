from utils.settings import Settings
from utils.singleton import Singleton
from .contextmanager import lifespan

class Settings(Settings, Singleton):
    app_name: str = "Lizzard Dungeon Master"
    app_presets: dict ={
        'title': app_name,
        'lifespan': lifespan
    }
