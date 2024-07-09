from concurrent.futures import ThreadPoolExecutor
import threading
import logging
from typing import Iterator
import time
import asyncio
import typing
import PySide6
from PySide6.QtCore import (Qt, QObject, Signal, Slot)
from PySide6.QtGui import (QColor, QFont, QPalette)
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QMainWindow, QVBoxLayout, QWidget)


        
import grpc.aio

from FilesManager import FilesManager
from MyWindow import MyWindow
from UsersManager import UsersManager


async def run(channel):
    UsersInfo = UsersManager(channel)
    FilesInfo = FilesManager(channel)
        
    logging.info("Connecting to [%s]", "localhost:50051")
    await UsersInfo.connect()
    logging.info("Pending connections...")
    print(await UsersInfo.get_users())
    asyncio.create_task(FilesInfo.StreamFilesRequest())
    asyncio.create_task(FilesInfo.StreamFilesReceive())
    login = input()
    result = FilesInfo.RequestFiles(login)
        
    logging.info("Getting files from [%s]", login)
    await asyncio.run(result)#(fut=result,timeout=1)
    await UsersInfo.disconnect()
        
        
if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)
    
    app = PySide6.QtWidgets.QApplication(sys.argv)
    channel = grpc.aio.insecure_channel("localhost:50051")
    users = UsersManager(channel=channel)
    w = MyWindow(users)
    w.show()
    