import asyncio

import PySide6.QtAsyncio
import PySide6.QtGui
from FilesManager import FilesManager
from MyFrame import MyFrame
import PySide6.Qt
from TransferManager import TransferManager
from UsersManager import UsersManager

import PySide6.QtCore
import PySide6.QtWidgets

import logging

from protos.Files_pb2 import Directory
import protos.Transfer_pb2 as Transfer 


class MyWindow(PySide6.QtWidgets.QMainWindow):

    @PySide6.QtCore.Slot(bool)
    async def OnConnect(self, _ = bool):
        print("OnConnect")
        await self._users.connect()
        
        loop = asyncio.get_event_loop()

        
        loop.create_task(self._files.StreamFiles())              
        loop.create_task(self._transfer.FileTransferProcessUpload())        
        loop.create_task(self._transfer.FileTransferProcessDownload())        
        loop.create_task(self._transfer.FileTransferListener())
        
        result = await self._users.get_users()
        
        self._leftFrame.UpdateCombo(result)
        self._rightFrame.UpdateCombo(result)
        
        self._leftLogin = self._leftFrame.box.currentText()
        self._rightLogin = self._rightFrame.box.currentText()

    async def onDrop(self, right: bool, filename: str, filesize: int, lastdate: int):
        desc = Transfer.FileTransferRequestInit()
        desc.SrcUser.login, desc.DstUser.login = self._leftFrame.box.currentText(), self._rightFrame.box.currentText()
        if not right:
            desc.SrcUser.login, desc.DstUser.login = desc.DstUser.login, desc.SrcUser.login
        desc.SrcFile.Name = desc.DstPath.Name = filename
        desc.SrcFile.FileSize = desc.DstPath.FileSize = filesize
        desc.SrcFile.LastDate = desc.DstPath.LastDate = lastdate
        await self._transfer.FIleTransferProgress(desc)
        

    @PySide6.QtCore.Slot(bool)
    async def OnReconnect(self, _ = bool):
        pass
        #grpc_context->Connect("localhost:50051")

    async def leftChangeIndex(self, new_index: int):
        
        frame = self._leftFrame
        self._leftLogin = frame.box.currentText()
        leftLogin = self._leftLogin
        frame.setEnabled(False)
        files: Directory = await self._files.RequestFilesFromUser(frame.box.currentText())
        if leftLogin != self._leftLogin:
            return
        treeFiles = []
        
        from datetime import datetime

        for file in files.files:
            print(file)
            date = datetime.fromtimestamp(file.LastDate).isoformat()
            treeFiles.append({"%s" % (file.Name): ("%d" % (file.FileSize), "%s" % (date))})
        frame.tree.UpdateTree(treeFiles)
        
        frame.setEnabled(True)
        

    async def rightChangeIndex(self, new_index: int):
        
        frame = self._rightFrame
        self._rightLogin = frame.box.currentText()
        rightLogin = self._rightLogin
        frame.setEnabled(False)
        files: Directory = await self._files.RequestFilesFromUser(frame.box.currentText())
        if rightLogin != self._rightLogin:
            return
        treeFiles = []
        
        from datetime import datetime

        for file in files.files:
            print(file)
            date = datetime.fromtimestamp(file.LastDate).isoformat()
            treeFiles.append({"%s" % (file.Name): ("%d" % (file.FileSize), "%s" % (date))})
        
        frame.tree.UpdateTree(treeFiles)
        
        frame.setEnabled(True)

    def closeEvent(self, _: PySide6.QtGui.QCloseEvent):
        self._files.Quiting = True
        self._transfer.Quiting = True

    def __init__(self, users: UsersManager, files: FilesManager, transfer: TransferManager, parent=None):
        super().__init__(parent)
        self._splitter = PySide6.QtWidgets.QSplitter(self)
        
        self._files = files
        self._users = users
        self._transfer= transfer
        self._bar = PySide6.QtWidgets.QMenuBar(self)
        self._files.event.set()
        FileMenu: PySide6.QtWidgets.QMenu = self._bar.addMenu("File")
        FileMenu.addSection("Connection")

        Connection = FileMenu.addAction("Connect")

        Connection.triggered.connect(lambda: asyncio.ensure_future(self.OnConnect()))

        #REConnection = FileMenu.addAction("Reconnect")
        #REConnection.triggered.connect(self.OnReconnect)

        #FileMenu.addAction("Disconnect")
        self.setMenuBar(self._bar)
        self._status = PySide6.QtWidgets.QStatusBar(self)
        self.setStatusBar(self._status)

        self.setMinimumWidth(1280)
        self.setMinimumHeight(720)
        
        self._leftFrame = MyFrame()
        self._rightFrame = MyFrame()
        self._leftFrame.tree.setObjectName("left")
        self._rightFrame.tree.setObjectName("right")
        self._leftFrame.box.currentIndexChanged.connect(lambda index: asyncio.ensure_future(self.leftChangeIndex(index)))
        self._rightFrame.box.currentIndexChanged.connect(lambda index: asyncio.ensure_future(self.rightChangeIndex(index)))
        self._leftFrame.tree.ItemDrop.connect(lambda x, y ,z: asyncio.ensure_future(self.onDrop(False, x,y,z)))
        self._rightFrame.tree.ItemDrop.connect(lambda x, y ,z: asyncio.ensure_future(self.onDrop(True, x,y,z)))
        self._splitter.setChildrenCollapsible(False)
        self._splitter.addWidget(self._leftFrame)
        self._splitter.addWidget(self._rightFrame)
        
        self.setCentralWidget(self._splitter)