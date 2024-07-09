from typing import List
from MyListItem import MyListItem


import PySide6.QtCore
import PySide6.QtGui
import PySide6.QtWidgets


import logging


class MyList(PySide6.QtWidgets.QTreeWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setSelectionMode(PySide6.QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
        self.setDragEnabled(True)
        self.setDragDropMode(PySide6.QtWidgets.QAbstractItemView.DragDropMode.DragDrop)
        self.viewport().setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDefaultDropAction(PySide6.QtCore.Qt.DropAction.CopyAction)
        self.setAcceptDrops(True)
        self.setDragDropOverwriteMode(True)

    def dragEnterEvent(self, event: PySide6.QtGui.QDragEnterEvent):
        super().dragEnterEvent(event)
        if event.source() != self:
            event.accept()
        else:
            event.ignore()

    def _CanDrop(self, event: PySide6.QtGui.QDropEvent) -> bool:
        if event.source() is self:
            return False
        OtherList: MyList = event.source()
        logging.info("Source: %s", event.source().objectName())
        
        logging.info("Source: %s", OtherList.objectName())
        NewItem = OtherList.currentItem()
        result = self._HasItem(NewItem.text(0), int(NewItem.text(1)), int(NewItem.text(2)))
        print("%s %s" % (result, not result))
        return not result
        
    
    def _HasItem(self, filename: str, filesize: int, LastModified: int)-> bool:
        def CheckTree(tree) -> bool | None:
            for k, v, in tree.items():
                if k != filename:
                    continue
                if type(v) == dict:
                    result = CheckTree(v)
                    if result != None:
                        return result
                else:
                    if filesize == v[0] and LastModified == v[1]:
                        return True
            return None
        result = CheckTree(self._list)
        if result == None:
            result = False
        return result   
        
    def UpdateTree(self, inList: dict) -> None:
        self._list = inList
        def GetChildren(InDict: dict) -> List[PySide6.QtWidgets.QTreeWidgetItem]:

            lister = [] 
            for k, v in InDict.items():
                if type(v) == dict:
                    children = GetChildren(InDict=v)
                    item = PySide6.QtWidgets.QTreeWidgetItem([k])
                    item.addChildren(children)
                    lister.append(item)
                else:
                    childitem = PySide6.QtWidgets.QTreeWidgetItem([k, "%s" % (v[0]),"%s" % (v[1])])
                    lister.append(childitem)
                    
            return lister
        childs = GetChildren(inList)
        self.addTopLevelItems(childs)
        
    def startDrag(self, supportedActions: PySide6.QtCore.Qt.DropAction):
        print(self.currentItem())
        logging.info("Started drag")
        self._curr = self.currentItem()
        super().startDrag(supportedActions)

    def dropEvent(self, event: PySide6.QtGui.QDropEvent):
        if self._CanDrop(event):
            logging.info("Can drop")
            
            super().dropEvent(event)
            event.accept()
            
        else:
            event.ignore()
            logging.info("Ignore")
        
    def dragMoveEvent(self, event: PySide6.QtGui.QDragMoveEvent):
        if (event.source() != self):
            #logging.info("From Not here")
            event.accept()
        else:
            #logging.info("From here")
            event.ignore()

        super().dragMoveEvent(event)

    def supportedDropActions(self) -> PySide6.QtCore.Qt.DropAction:
        
        return PySide6.QtCore.Qt.DropAction.CopyAction