

from FilesManager import FilesManager
from UsersManager import UsersManager


class ConnectionManager:
    def __init__(self):
        self._users = UsersManager
        self._files = FilesManager
    
    