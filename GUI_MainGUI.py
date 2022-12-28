# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 14:46:11 2022

@author: demishu
"""
import sys
from functools import partial

from PyQt6.QtWidgets import QApplication

from GUI_SalesPart import SalesPart
from GUI_utilities import PartMetaClass


class StocksPart(PartMetaClass):
    def __init__(self, parent=None):
        self._ui_path = "./销售管理主界面.ui"
        super().__init__(parent)


class AccountingPart(PartMetaClass):
    def __init__(self, parent=None):
        self._ui_path = "./销售管理主界面.ui"
        super().__init__(parent)


class ArticlesPart(PartMetaClass):
    def __init__(self, parent=None):
        self._ui_path = "./销售管理主界面.ui"
        super().__init__(parent)


class ReplenishmentPart(PartMetaClass):
    def __init__(self, parent=None):
        self._ui_path = "./销售管理主界面.ui"
        super().__init__(parent)


class ClientsPart(PartMetaClass):
    def __init__(self, parent=None):
        self._ui_path = "./销售管理主界面.ui"
        super().__init__(parent)


class MainGUI(PartMetaClass):  # todo多线程优化
    def __init__(self, parent=None):
        self._ui_path = "./MainGUI.ui"
        super(MainGUI, self).__init__(parent)
        self.button_class_dict = {
            self.form.SalesButton: SalesPart,
            self.form.StocksButton: StocksPart,
            self.form.AccountingButton: AccountingPart,
            self.form.ArticlesButton: ArticlesPart,
            self.form.ReplenishmentButton: ReplenishmentPart,
            self.form.ClientsButton: ClientsPart
        }
        # obj_list存放窗口, 给每个part分别创建一个list，每创建一个part的窗口就塞进相对应的list里。
        self.obj_list = [[] for part in self.button_class_dict]
        for i, Button in enumerate(self.button_class_dict.keys()):
            # 关联GUI按钮和open_GUI方法
            Button.clicked.connect(partial(self.open_GUI, Button, i))

    def open_GUI(self, button, i) -> None:
        print(f'{self.button_class_dict[button]}')
        '将类赋值给class_obj'
        class_obj = self.button_class_dict[button]
        # 相对应的列表添加对象
        self.obj_list[i].append(class_obj())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = MainGUI()
    sys.exit(app.exec())
