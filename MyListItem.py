import protos.Files_pb2 as Files


import PySide6.QtCore
import PySide6.QtWidgets


class MyListItem(PySide6.QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(40)

        self.hLayout = PySide6.QtWidgets.QHBoxLayout()
        self.lFilename = PySide6.QtWidgets.QLabel()
        self.lSize = PySide6.QtWidgets.QLabel()
        self.lLastDate = PySide6.QtWidgets.QLabel()
        self.hLayout.addWidget(self.lFilename,50)
        self.hLayout.addWidget(self.lSize,20)
        self.hLayout.addWidget(self.lLastDate,30)

        self.setLayout(self.hLayout)

    @PySide6.QtCore.Slot(Files.File)
    def setFileInfo(self, NewFileInfo: Files.File):
        self.file = NewFileInfo
        self.lFilename.setText(self.file.Name)
        self.lSize.setText(self.file.FileSize)
        self.lLastDate.setText(self.file.LastDate)

    def FileInfo(self):
        return self.file

    FileInfo = PySide6.QtCore.Property(Files.File, setFileInfo, FileInfo)