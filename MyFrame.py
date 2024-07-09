import random
from MyList import MyList


import PySide6


import logging
from typing import List


class MyFrame(PySide6.QtWidgets.QWidget):
    
    
    def __init__(self, parent = None):
        super().__init__(parent)
        self.box = PySide6.QtWidgets.QComboBox()
        self.vbox = PySide6.QtWidgets.QVBoxLayout()
        self.tree = MyList()
        self.tree.setColumnCount(3)
        self.tree.setHeaderLabels(["Name", "Size", "Last Modified date"])
        self.tree.setColumnWidth(0, 350)
        self.vbox.addWidget(self.box)
        self.vbox.addWidget(self.tree)
        self.setLayout(self.vbox)
        self.setMinimumWidth(500)
        files = {
            "%s" % (self): (random.randint(1,2*1024*1024), random.randint(10,1024*1024*1024)),
            "filename2.jpg": (5, 7),
        }
        self.tree.UpdateTree(files)
        
    
    def UpdateCombo(self, inList: List[str]) -> str | None:
        logging.info("UpdateCombo")
        currText = self.box.currentText()
        self.box.clear()
        self.box.addItems(List)

        if inList.count() == 0:
            return None
        try:
            index = inList.index(currText)
        except ValueError:
            return inList[0]

        for i, v in inList.__iter__():
            if v == currText:
                self.box.setCurrentIndex(i)
                return currText

        return None