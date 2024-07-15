from typing import List


import PySide6.QtCore
import PySide6.QtGui
import PySide6.QtWidgets


import logging


class MyList(PySide6.QtWidgets.QTreeWidget):
    ItemDrop = PySide6.QtCore.Signal(str,int,int)
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

    def _CanDrop(self, event: PySide6.QtGui.QDropEvent):
        if event.source() is self:
            return False, (None, None, None)
        OtherList: MyList = event.source()
        logging.info("Source: %s", event.source().objectName())
        
        logging.info("Source: %s", OtherList.objectName())
        NewItem = OtherList.currentItem()
        result = self._HasItem(NewItem.text(0), NewItem.text(1), NewItem.text(2))
        from datetime import datetime
        
        print("%s %s" % (result, not result))
        return not result, (NewItem.text(0), int(NewItem.text(1)), int(datetime.fromisoformat(NewItem.text(2)).timestamp()))
        
    
    def _HasItem(self, filename: str, filesize: str, LastModified: str)-> bool:
        def CheckTree(tree: PySide6.QtWidgets.QTreeWidgetItem) -> bool | None:
            
            print("%s::%s" % (tree.text(0),filename))
            if tree.text(0) == filename and tree.text(1) == filesize and tree.text(2) == LastModified:
                return True
            for i in range(0,tree.childCount()):
                item = tree.child(i)
                if item.text(0) == filename and item.text(1) == filesize and item.text(2) == LastModified:
                    return True
                CheckTree(item)
            return None
        
        for i in range(0, self.topLevelItemCount()):
            subtreeitem: PySide6.QtWidgets.QTreeWidgetItem = self.topLevelItem(i)
            if CheckTree(subtreeitem):
                print("Found: %s", subtreeitem.text(0))
                return True
        
        return False
    def UpdateTree(self, inList: dict) -> None:
        self._list = inList
        self.clear()
        def GetChildren(InDict: dict) -> List[PySide6.QtWidgets.QTreeWidgetItem]:

            print(InDict)
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
        childs = []
        for l in inList:
            childs.extend(GetChildren(l))
        #childs = GetChildren(inList)
        self.addTopLevelItems(childs)
        
    def startDrag(self, supportedActions: PySide6.QtCore.Qt.DropAction):
        print(self.currentItem())
        logging.info("Started drag")
        self._curr = self.currentItem()
        super().startDrag(supportedActions)

    def dropEvent(self, event: PySide6.QtGui.QDropEvent):
        candrop, droppeditem = self._CanDrop(event)
        if candrop:
            logging.info("Can drop")
            
            super().dropEvent(event)
            event.accept()
            self.ItemDrop.emit(droppeditem[0],droppeditem[1],droppeditem[2])
            
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