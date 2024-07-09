import asyncio
from MyFrame import MyFrame
from UsersManager import UsersManager

import PySide6.QtCore
import PySide6.QtWidgets

import logging


class MyWindow(PySide6.QtWidgets.QMainWindow):

    @PySide6.QtCore.Slot(bool)
    async def OnConnect(self, _ = bool):
        await self._users.connect()
        self._leftFrame.box.clear()
        result =await self._users.get_users()
        self._leftFrame.box.clear()
        self._leftFrame.box.addItems(result)

    @PySide6.QtCore.Slot(bool)
    def OnReconnect(self, _ = bool):
        pass
        #grpc_context->Connect("localhost:50051")

    @PySide6.QtCore.Slot(int)
    def leftChangeIndex(self, new_index: int):
        pass
        # QStringList copy = connectedList;
        # grpc_context->GetConnectedList(
        # [this, copy](std::exception_ptr, std::set<std::string> List) {
        #   connectedList.clear();
        #   for (const auto &str : List) {
        #     connectedList.append(QString::fromStdString(str));
        #   }
        #   bool shouldReset = true;
        #   if (copy.size() == connectedList.size()) {
        #     shouldReset = false;
        #     for (int Index = 0; Index < copy.size(); Index++) {
        #       if (copy[Index] != connectedList[Index]) {
        #         shouldReset = true;
        #         break;
        #       }
        #     }
        #   }

        #   if (shouldReset) {
        #     frame1->UpdateCombo(connectedList);
        #     frame2->UpdateCombo(connectedList);
        #   }
        # });

    @PySide6.QtCore.Slot(int)
    def LindexActivated(self, new_index: int):
        if self._leftFrame.box.count() == 0:
            self._leftFrame.tree.clear()

        client = self._leftFrame.box.currentText()
        logging.info("Left Login: [%s]", client)

        # grpc_context->GetFileMap(
        #     client, [this](std::exception_ptr, FsRequestType set) {
        #     frame1->tree->clear();
        #     for (const auto &str : set) {
        #         QListWidgetItem* Item = new QListWidgetItem;
        #         MyListItem* widget = new MyListItem(this);
        #         widget->SetFileInfo(str);
        #         Item->setSizeHint(widget->sizeHint());
        #         frame1->tree->addItem(Item);
        #         frame1->tree->setItemWidget(Item,widget);
        #     }
        # });

    @PySide6.QtCore.Slot(int)
    def RindexActivated(self, new_index: int):
        if self._rightFrame.box.count() == 0:
            self._rightFrame.tree.clear()

        client = self._rightFrame.box.currentText()
        logging.info("Right Login: [%s]", client)

        # grpc_context->GetFileMap(
        #     client, [this](std::exception_ptr, FsRequestType set) {
        #     frame2->tree->clear();
        #     for (const auto &str : set) {
        #         QListWidgetItem* Item = new QListWidgetItem;
        #         MyListItem* widget = new MyListItem(this);
        #         widget->SetFileInfo(str);
        #         Item->setSizeHint(widget->sizeHint());
        #         std::cout<<widget->sizeHint().width()<<" "<<widget->sizeHint().height()<<std::endl;
        #         frame2->tree->addItem(Item);
        #         frame2->tree->setItemWidget(Item,widget);
        #     }
        # });

    def __init__(self, users: UsersManager, parent=None):
        super().__init__(parent)
        self._splitter = PySide6.QtWidgets.QSplitter(self)
        
        
        self._users = users
        self._bar = PySide6.QtWidgets.QMenuBar(self)
        FileMenu: PySide6.QtWidgets.QMenu = self._bar.addMenu("File")
        FileMenu.addSection("Connection")

        Connection = FileMenu.addAction("Connect")
        Connection.triggered.connect(lambda: asyncio.ensure_future(self.OnConnect()))

        REConnection = FileMenu.addAction("Reconnect")
        REConnection.triggered.connect(self.OnReconnect)

        FileMenu.addAction("Disconnect")
        self.setMenuBar(self._bar)
        self._status = PySide6.QtWidgets.QStatusBar(self)
        self.setStatusBar(self._status)

        self.setMinimumWidth(1280)
        self.setMinimumHeight(720)
        
        self._leftFrame = MyFrame()
        self._rightFrame = MyFrame()
        self._leftFrame.tree.setObjectName("left")
        self._rightFrame.tree.setObjectName("left")
        
        self._splitter.setChildrenCollapsible(False)
        self._splitter.addWidget(self._leftFrame)
        self._splitter.addWidget(self._rightFrame)
        
        self.setCentralWidget(self._splitter)