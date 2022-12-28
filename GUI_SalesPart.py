# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 14:51:32 2022

@author: demishu
"""
import datetime
import sys
from collections.abc import Iterable
from functools import partial
from typing import Any

import numpy as np
import pandas as pd
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QDoubleValidator, QIntValidator, QKeySequence, QShortcut
from PyQt6.QtWidgets import QLineEdit, QTreeWidgetItem, \
    QTableWidgetItem, QStyledItemDelegate, \
    QComboBox, QMessageBox, QApplication

from GUI_utilities import set_interval, PartMetaClass, get_DisName
from database import MySession, Sales, Clients, Articles
from 销售管理主界面 import Ui_Form as SalesPartUi
from 销售管理单据管理 import Ui_details as OrderWindowUi


class SalesPart(PartMetaClass):
    def __init__(self, parent=None):
        """parent 默认空白。"""
        '初始化'
        self._UiClass = SalesPartUi
        self._session = MySession()
        super().__init__(parent)

        '设置标题'
        self.root.setWindowTitle('销售管理主界面')
        # 用于装OderWindow实例，以确保可以打开任意数量的单据管理窗口。
        self.windows_list = []
        # QTreeWidget显示的列
        self.tree_disp_col = ['单据', '日期', '客户', '箱数', '件数', '总金额', '付款方式', '欠款金额']

        '获取客户df,并保存'
        query = self._session.session.query(Clients)
        self._clients_df = self._session.read_sql_query(query)
        self._clients_df['DisName'] = self._clients_df[['Nome', 'Prov', '国家']].apply(get_DisName, axis=1)
        self._clients_df.loc[-1] = '--'
        self._clients_df.sort_index(inplace=True)
        self._clients_df.set_index('ClienteId', drop=True, inplace=True)
        '开始更新界面'
        self._insert_data_to_tree()
        '设置日期'
        start_date, end_date = set_interval()
        self.form.StartDateEdit.setDate(start_date)
        self.form.EndDateEdit.setDate(end_date)
        '设置validator'
        self._set_validator()
        '设置关联'
        # 重置单据
        self.form.ResetButton.clicked.connect(self._insert_data_to_tree)
        # 关联'新建'和'单据管理'界面
        self.form.CreateNewOrderButton.clicked. \
            connect(partial(self._open_detail_windows, new_windows=True))
        # 更新'客户列表'和'付款方式'
        self.form.DIYSearchCheckBox.clicked.connect(self._update_DIY_section)
        # 关联'双击单据n'打开'单据n'的界面
        self.form.tree.itemDoubleClicked.connect \
            (partial(self._open_detail_windows, new_windows=False))
        self.form.SearchButton.clicked.connect(self._DIYSearch)
        # 关联'删除'和 'self.删除功能'
        self.form.DeleteButton.clicked.connect(self._delete_selected_treeItem)
        self.form.DeleteButton.clicked.connect(self._update_amount_label)
        self.form.tree.itemSelectionChanged.connect(self._show_selected)

    def _set_validator(self):
        """设置一些Widget的validator"""
        validator = QDoubleValidator(self.form.UpperLimitLineEdit)
        self.form.UpperLimitLineEdit.setValidator(validator)
        validator = QDoubleValidator(self.form.LowerLimitLineEdit)
        self.form.LowerLimitLineEdit.setValidator(validator)
        validator = QDoubleValidator(self.form.DebtUpperLimitLineEdit)
        self.form.DebtUpperLimitLineEdit.setValidator(validator)
        validator = QDoubleValidator(self.form.DebtLowerLimitLineEdit)
        self.form.DebtLowerLimitLineEdit.setValidator(validator)

    def _show_selected(self):
        """UI左下角填充数字进去"""
        boxes = 0
        pcs = 0
        amounts = 0
        for child in self.form.tree.selectedItems():
            box = int(child.text(3))
            pc = int(child.text(4))
            amount = float(child.text(5))
            boxes += box
            pcs += pc
            amounts += amount
        boxes = f'{boxes} 箱'
        pcs = f'{pcs} 件'
        amounts = f"{amounts:.2f} €"
        self.form.SelectedBoxesNumLabel.setText(boxes)
        self.form.SelectedPcsNumLabel.setText(pcs)
        self.form.SelectedAmountNumLabel.setText(amounts)

    def _get_current_tree_df(self):
        """返回当前QTreeWidget显示的数据，以df的方式"""
        # 获取根节点数量,即行数
        n_row = self.form.tree.topLevelItemCount()
        headers = self.form.tree.headerItem()
        n_col = headers.columnCount()
        datas = []
        for row in range(n_row):
            data = []
            for col in range(n_col):
                # 循环获取根节点,即每一行
                item = self.form.tree.topLevelItem(row)
                text = item.text(col)
                data.append(text)
            datas.append(data)
        df = pd.DataFrame(datas, columns=self.tree_disp_col, index=range(len(datas)))
        df.loc[:, ['总金额', '欠款金额']] = df[['总金额', '欠款金额']].astype(float)
        df.loc[:, ['单据', '箱数', '件数']] = df.loc[:, ['单据', '箱数', '件数']].astype(int)
        return df

    def _DIYSearch(self):
        """自定义查询的查询功能"""
        # 如果DIY查询为真，则执行以下代码
        if self.form.DIYSearchCheckBox.isChecked():
            '筛选条件'
            start_date = self.form.StartDateEdit.date().toPyDate()
            end_date = self.form.EndDateEdit.date().toPyDate()
            client = self.form.ClientComBox.currentText()
            payment = self.form.PaymComBox.currentText()
            amount_upper_limit = None
            if self.form.UpperLimitCheckBox.isChecked():
                amount_upper_limit = self.form.UpperLimitLineEdit.text()
                amount_upper_limit = float(amount_upper_limit) if amount_upper_limit != "" else 0
            amount_lower_limit = None
            if self.form.LowerLimitCheckBox.isChecked():
                amount_lower_limit = self.form.LowerLimitLineEdit.text()
                amount_lower_limit = float(amount_lower_limit) if amount_lower_limit != "" else 0
            debt_upper_limit = None
            if self.form.DebtUpperLimitCheckBox.isChecked():
                debt_upper_limit = self.form.DebtUpperLimitLineEdit.text()
                debt_upper_limit = float(debt_upper_limit) if debt_upper_limit != "" else 0
            debt_lower_limit = None
            if self.form.DebtLowerLimitCheckBox.isChecked():
                debt_lower_limit = self.form.DebtLowerLimitLineEdit.text()
                debt_lower_limit = float(debt_lower_limit) if debt_lower_limit != "" else 0

            '获取当前tree并根据条件筛选'
            df = self._get_current_tree_df()
            df.loc[:, '日期'] = df.loc[:, '日期'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').date())
            df = df[df['日期'] >= start_date][df['日期'] <= end_date]
            if client != '--':
                df = df[df['客户'] == client]
            if payment != '--':
                df = df[df['付款方式'] == payment]
            if amount_upper_limit:
                df = df[df['总金额'] <= amount_upper_limit]
            if amount_lower_limit:
                df = df[df['总金额'] >= amount_lower_limit]
            if debt_upper_limit:
                df = df[df['欠款金额'] <= debt_upper_limit]
            if debt_lower_limit:
                df = df[df['欠款金额'] >= debt_lower_limit]

            self._insert_data_to_tree(df)

        else:
            '重置当前QTreeWidget的列表'
            self._insert_data_to_tree()

    def _update_amount_label(self):
        """更新右下角的TotAmountNumLabel"""
        df = self._get_current_tree_df()
        amount_values = df['总金额'].sum()
        amount_values = f'{amount_values:.2f} €'
        self.form.TotAmountNumLabel.setText(amount_values)

    def _update_DIY_section(self, paym_default: str = None, client_default: str = None):
        '更新DIY区'
        self._update_paym_combox(paym_default)
        self._update_client_combox(client_default)

    def _update_paym_combox(self, default_value: str = None):
        '更新付款方式列表，如果传参default_value就尝试将其显示出来'
        self.form.PaymComBox.clear()
        paym_list = ['--', '现金', '银行', '欠款']
        self.form.PaymComBox.addItems(paym_list)
        if default_value and (default_value in paym_list):
            self.form.ClientComBox.setCurrentIndex(paym_list.index(default_value))

    def _update_client_combox(self, default_value: str = None):  # 更新客户列表
        """更新客户列表，如果传参default_value就尝试将其显示出来"""
        self.form.ClientComBox.clear()
        df = self._clients_df.copy()
        clients_list = df['DisName'].values.tolist()
        self.form.ClientComBox.addItems(clients_list)
        if default_value and (default_value in clients_list):
            self.form.ClientComBox.setCurrentIndex(clients_list.index(default_value))

    def _insert_data_to_tree(self, df: pd.DataFrame or None = None):
        """在没有传参dataframe进来时，用数据库的数据填充GUI；
                    传参dataframe进来时，展示传进来的参数"""
        self.form.tree.clear()
        if df is None or isinstance(df, bool):
            df = self._session.read_sql_table(Sales)
            bills_set = set(df['id'])  # 拉去已有的单据列表
            '生成一个新的dataframe，用于填充GUI的数据'
            dataframe = pd.DataFrame(columns=self.tree_disp_col)
            for i, bill in enumerate(bills_set):  # 填充dataframe
                df_id = df[df['id'] == bill]
                date_clienteId_payment = df_id[['Data', 'ClienteId', '付款方式']].values[0]
                boxes_pcs_amount = df_id[['箱数', '件数', '总价']].apply(lambda x: x.sum())
                extralargeCost_discount = df_id[['加单费', '折扣']].values[0]
                extralarge_cost, discount = extralargeCost_discount  # 获取加单费和折扣，用于计算总金额=sum（总价）+加单费-折扣
                if extralarge_cost is pd.NA or extralarge_cost in (np.nan, '', None):
                    extralarge_cost = 0
                if discount is np.nan or discount == '' or discount is None or discount is pd.NA:
                    discount = 0
                date, clienteId, payment = date_clienteId_payment
                '日期'
                date = date.strftime('%Y-%m-%d')
                '客人'
                clients_df = self._clients_df.copy()
                cliente = clients_df.at[clienteId, 'DisName']
                boxes, pcs, amount = boxes_pcs_amount
                '总金额'
                amount = float(amount) + float(extralarge_cost) - float(discount)  # 计算总金额
                amount = f'{amount:.2f}'
                '欠款'
                debt = df_id['欠款金额'].values[0]
                debt = f'{debt:.2f}'
                dataframe.loc[i, self.tree_disp_col] = [bill, date, cliente, boxes, pcs, amount, payment, debt]
                dataframe.loc[:, ['箱数', '件数']] = dataframe[['箱数', '件数']].astype(int)
        else:
            dataframe = df
            dataframe.loc[:, ['总金额', '欠款金额']] = dataframe[['总金额', '欠款金额']].applymap(
                lambda x: f"{x:.2f}" if x is not np.nan else '')
        dataframe = dataframe.applymap(lambda x: str(x))  # QTreeWidgetItem只接受str
        rows = dataframe.to_numpy().tolist()
        final_rows = []
        len_row = len(rows[0])
        for row in rows:  # 这里得考虑优化一下，双重loop，太慢了
            tree_item = QTreeWidgetItem(self.form.tree, row)
            [tree_item.setTextAlignment(i, Qt.AlignmentFlag.AlignCenter)
             for i in range(0, len_row)]
            final_rows.append(tree_item)
        self.form.tree.insertTopLevelItems(0, final_rows)  # 填入GUI
        self._update_amount_label()

    def _delete_selected_treeItem(self):
        """用于删除被选中的QtreeWidget的items"""
        warning_value = QMessageBox.warning(self, '你正在尝试删除销售记录',
                                            '是否删除当前选中的记录？\n注意！删除后无法恢复',
                                            QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.No)
        if warning_value is QMessageBox.StandardButton.Yes:
            selected_items = self.form.tree.selectedItems()
            for item in selected_items:
                id_num = item.text(0)  # 获取第0行（单据）的text
                self._session.session.query(Sales.__table__).filter(Sales.id == id_num).delete()
                self._session.session.commit()
                item.removeChild(item)
                print('删除成功')

    def _open_detail_windows(self, new_windows: bool or None = False):
        """如果没输入item，则传输个空df，反之有内容的df"""
        if new_windows:  # 如果要打开空白窗口，传参空白df
            df = pd.DataFrame()
        else:  # 不然的话，获取df信息，并传参df
            item = self.form.tree.selectedItems()[0]
            if item:
                id_num = item.text(0)
                query = self._session.session.query(Sales).filter(Sales.id == id_num)
                df = self._session.read_sql_query(query)

                query = self._session.session.query(Articles.ArtId, Articles.Articolo, Articles.Colore)
                articles_info = self._session.read_sql_query(query)
                articles_info.set_index("ArtId", inplace=True)  # 设置ArtId索引
                df['Articolo'] = df['ArtId'].apply(lambda x: articles_info.loc[x, 'Articolo'])
                df['Colore'] = df['ArtId'].apply(lambda x: articles_info.loc[x, 'Colore'])

        self.windows_list.append(object())
        self.windows_list[-1] = OrderWindow(df=df)


class OrderWindow(PartMetaClass):  # 单据管理界面，SalesPart里双击TreeWidget或单击新建按钮，才能打开这个界面
    def __init__(self, parent=None, df: pd.DataFrame or None = None):
        # self._ui_path ="./销售管理单据管理.ui"           
        self._UiClass = OrderWindowUi  # 初始化
        self.table_widget_value_col = ['Data', 'ClienteId', '付款方式', '付款金额', '加单费', '折扣']
        self.table_dis_col = ['Articolo', 'Colore', '件数/箱', '箱数', '件数', '单价（件）', '总价']
        self._session = MySession()
        super().__init__(parent)  # 初始化
        '设置标题'
        self.root.setWindowTitle('单据管理')
        '商品df'
        self._article_df = self._session.read_sql_table(Articles)
        '客人df'
        clients_df = self._session.read_sql_table(Clients)
        clients_df.loc[-1] = "--"  # 创建空白项
        clients_df = clients_df.sort_index()
        clients_df['DisName'] = clients_df[['Nome', 'Prov', '国家']].apply(get_DisName, axis=1)
        self._clients_df = clients_df
        '快捷键'
        QShortcut(QKeySequence('Alt+D'), self.form.table, self._clean_selected_cells)
        QShortcut(QKeySequence(QKeySequence.StandardKey.Delete), self.form.table, self._clean_selected_cells)

        '更新第一行的各个Widget（客户，日期，等等）'
        self._update_widgets()
        x, today = set_interval()
        del x
        '设置日期'
        self.form.SaleDateEdit.setDate(today)
        '关联功能'
        self.form.NewRowButton.clicked.connect(self._insert_new_row)
        self.form.DeletRowButton.clicked.connect(self._remove_selected)
        self.form.PaymentLineEdit.textChanged.connect(self._update_amount_label)
        self.form.DiscountLineEdit.textChanged.connect(self._update_amount_label)
        self.form.ExtraLargeLineEdit.textChanged.connect(self._update_amount_label)
        self.form.PaymComBox.currentIndexChanged.connect(self._update_paym_lineEdit)
        self.form.table.itemSelectionChanged.connect(self._show_selected)
        self.form.SaveButton.clicked.connect(self._save_order)
        '输入信息'
        if df is not None:
            if isinstance(df, pd.DataFrame):
                self._df = df
                self._insert_and_init_data_to_table(df)

    @property
    def article_df(self):
        """深拷贝article_df"""
        return self._article_df.copy()

    def _clean_selected_cells(self):
        items = self.form.table.selectedItems()
        for item in items:
            if isinstance(item, QTableWidgetItem):
                item.setText("")

    def _update_widgets(self):
        self._update_client_combox()
        self._update_paym_combox()
        self._update_bill_combox()

    def _update_paym_lineEdit(self, idx: int):
        """设置付款方式lineEdit，如果为欠款，就不可输入金额，反之可以输入金额。"""
        if idx == 0:
            self.form.PaymentLineEdit.setEnabled(False)
        else:
            self.form.PaymentLineEdit.setEnabled(True)

    def _update_bill_combox(self, default_value=None):
        """更新单据列表，如果传参default_value就尝试将其显示出来，不然就新生成一个单据并显示新单据"""
        self.form.BillComBox.clear()
        df = self._session.read_sql_table(Sales)
        id_list = df['id'].unique()  # 排重
        id_list = [str(id_num) for id_num in id_list]  # 转成string
        self.form.BillComBox.addItems(id_list)
        if default_value and default_value in id_list:  # 如果再id_list里有default_value，就显示default_value
            self.form.BillComBox.setCurrentIndex(id_list.index(default_value))
        elif default_value not in id_list:  # 不然新增id并显示新id
            id_list = [int(id_num) for id_num in id_list]
            new_id = str(max(id_list) + 1)
            id_list.append(new_id)
            id_list = [str(id_num) for id_num in id_list]
            self.form.BillComBox.clear()
            self.form.BillComBox.addItems(id_list)
            self.form.BillComBox.setCurrentIndex(id_list.index(new_id))

    def _update_client_combox(self, default_value: str = None):  # 更新客户列表
        """更新客户列表，如果传参default_value就尝试将其显示出来，反之显示'--'"""
        self.form.ClientComBox.clear()
        df = self._clients_df.copy()
        clients_list = df['DisName'].values.tolist()
        self.form.ClientComBox.addItems(clients_list)

        if default_value and default_value in clients_list:
            self.form.ClientComBox.setCurrentIndex(clients_list.index(default_value))

    def _update_paym_combox(self, default_value: str = None):
        """更新付款方式列表，如果传参default_value就尝试将其显示出来，反之默认显示'欠款'"""
        self.form.PaymComBox.clear()
        paym_list = ['欠款', '现金', '银行']
        self.form.PaymComBox.addItems(paym_list)
        if default_value and default_value in paym_list:
            self.form.PaymComBox.setCurrentIndex(paym_list.index(default_value))

    def _update_amount_label(self):
        """更新右下角的TotAmountNumLabel"""
        extralarge_cost = self.form.ExtraLargeLineEdit.text()
        extralarge_cost = float(extralarge_cost)  # 还需要测试
        discount = self.form.DiscountLineEdit.text()
        discount = float(discount)  # 还需要测试
        payment_value = self.form.PaymentLineEdit.text()
        payment_value = float(payment_value)
        df = self._get_current_table_df
        amount_values = df['总价'].sum()
        amount_values = amount_values + extralarge_cost - discount  # 待检验
        debt_value = amount_values - payment_value
        amount_values = f'{amount_values:.2f} €'
        debt_value = f'{debt_value} €'
        self.form.TotAmountValue.setText(amount_values)
        self.form.TotDebtValue.setText(debt_value)

    @property
    def _get_current_table_df(self):
        try:
            n_row = self.form.table.rowCount()  # 获取根节点数量,即行数
            n_col = self.form.table.columnCount()
            datas = []
            for row in range(n_row):
                data = []
                for col in range(n_col):
                    item = self.form.table.item(row, col)  # 循环获取根节点,即每一行
                    if not isinstance(item, type(None)):
                        text = item.text()
                        data.append(text)
                if data:
                    datas.append(data)
            df = pd.DataFrame(columns=self.table_dis_col, data=datas)
            df.loc[:, ['箱数', '件数']] = df[['箱数', '件数']].applymap(lambda x:
                                                                        0 if x == '' else int(x))
            df.loc[:, '总价'] = df['总价'].apply(lambda x: 0 if x == '' or x is None else float(x))
            return df
        except ValueError:
            return pd.DataFrame(columns=self.table_dis_col)
        except Exception as e:
            print(sys.exc_info())
            msg = f'\n错误信息:\n{e}\n'
            print(msg)
            return pd.DataFrame(columns=self.table_dis_col)

    def _format_table(self, n_row: int):
        """格式化n行，若n小于10，则默认10行"""
        'Articolo列'
        self.form.table.clear()
        self.form.table.setColumnCount(len(self.table_dis_col))
        self.form.table.setHorizontalHeaderLabels(self.table_dis_col)
        if n_row <= 10:
            n_row = 10
        self.form.table.setRowCount(n_row)

        '获取产品列表'
        df = self.article_df
        df.loc[-1, :] = ''
        df = df.sort_values(by=['Articolo'])

        '设置代理'
        pcs_boxes_amount_delegate = PcsBoxesAmountDelegate(parent=self)
        pcs_boxes_amount_delegate.commitData.connect(self._set_None_if_zero)
        self.form.table.setItemDelegate(pcs_boxes_amount_delegate)
        self.article_delegate_combox = ArticleDelegate(parent=self, df=df)  # 传输产品df，后续就可以少查询很多次
        self.form.table.setItemDelegateForColumn(0, self.article_delegate_combox)
        self.article_delegate_combox.commitData.connect(self._set_color_delegate)

    def _set_color_delegate(self):
        """设置颜色列的代理"""
        n_row = self.form.table.rowCount()  # 获取行数
        if n_row <= 10:
            n_row = 10
        # 获取table款号列的信息
        articles = []
        for row in range(n_row):
            item = self.form.table.item(row, 0)
            if isinstance(item, QTableWidgetItem):  # item不是QTableWidgetItem就是None
                item = item.text()
            articles.append(item)
        '设置代理'
        df = self.article_df
        self.color_delegate_combox = ColorDelegate(parent=self, df=df, articles=articles)
        self.form.table.setItemDelegateForColumn(1, self.color_delegate_combox)

    def _show_selected(self):
        """UI左下角填充数字进去"""
        boxes = 0
        pcs = 0
        amounts = 0
        rows = set()
        for child in self.form.table.selectedItems():
            row = child.row()
            rows.add(row)
        for row in rows:
            box = self._get_item_text(row, 3)
            if box.isdigit():
                box = int(box)
            else:
                box = 0
            pc = self._get_item_text(row, 4)
            if pc.isdigit():
                pc = int(pc)
            else:
                pc = 0

            amount = self._get_item_text(row, 6)
            if amount.replace('.', '').isdigit():
                amount = float(amount)
            else:
                amount = 0
            boxes += box
            pcs += pc
            amounts += amount
        boxes = f'{boxes} 箱'
        pcs = f'{pcs} 件'
        amounts = f"{amounts:.2f} €"
        self.form.SelectedBoxesNumLabel.setText(boxes)
        self.form.SelectedPcsNumLabel.setText(pcs)
        self.form.SelectedAmountValue.setText(amounts)

    def _set_None_if_zero(self, editor: QTableWidgetItem or None = None):
        if not isinstance(editor, QTableWidgetItem):
            if editor is None:
                return
        elif editor.text() == '0':
            editor.setText("")

    def _insert_and_init_data_to_table(self, df: pd.DataFrame):
        """"""
        "格式化Table"
        n_row = df.shape[0]
        self._format_table(n_row)

        if not df.empty:

            '获取参数'
            date, clientId, payment, payment_value, extralarge_cost, discount = df[self.table_widget_value_col].values[
                0]
            id_num = str(df['id'].values[0])
            date = datetime.datetime.strptime(str(date), '%Y-%m-%d')
            date = QDate(date.year, date.month, date.day)
            if extralarge_cost is None or extralarge_cost is np.nan:
                extralarge_cost = 0
            if discount is None or discount is np.nan:
                discount = 0
            if payment_value is None or payment_value is np.nan:
                payment_value = 0
            extralarge_cost = f'{extralarge_cost:.2f}'
            discount = f'{discount:.2f}'
            payment_value = f'{payment_value:.2f}'
            cliente_df = self._clients_df.copy()
            cliente_df.set_index('ClienteId', inplace=True, drop=True)
            cliente = cliente_df.at[clientId, 'DisName']
            '显示参数'
            self.form.SaleDateEdit.setDate(date)  # 日期
            self._update_client_combox(cliente)  # 客人
            self._update_paym_combox(payment)  # 付款方式
            self._update_bill_combox(id_num)  # 单据id
            self.form.ExtraLargeLineEdit.setText(extralarge_cost)  # 加单费
            self.form.DiscountLineEdit.setText(discount)  # 折扣
            self.form.PaymentLineEdit.setText(payment_value)
            '插入数据'
            temp_df = df[self.table_dis_col]  # 获取数据
            temp_df = temp_df.applymap(lambda x: f'{x:.2f}' if isinstance(x, float) else str(x))
            for row in range(n_row):
                for col, column_name in enumerate(self.table_dis_col):
                    data = temp_df.iloc[row, col]
                    item = QTableWidgetItem(data)
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.form.table.setItem(row, col, item)
        '输入完了数据再关联'
        "如果df为空的话直接关联"
        self._update_amount_label()
        self._set_color_delegate()
        self.form.table.cellChanged.connect(self._proccess_data)

    def _get_item_text(self, row: int, col: int) -> str:
        item = self.form.table.item(row, col)
        if isinstance(item, QTableWidgetItem):
            text = item.text()
            return text
        elif item is None:
            return ""
        else:
            raise ValueError(f"{item}不是QTableWidgetItem也不是None，请检查。")

    def _to_QTW(self, variable, dtype=int):
        if dtype is int:
            variable = f'{int(variable)}'
        elif dtype is float:
            variable = f'{variable:.2f}'
        elif dtype is str:
            pass
        variable = QTableWidgetItem(variable)
        variable.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
        return variable

    def _proccess_data(self, row: int, col: int) -> None:
        """在输入完初始信息后，每输入/修改表格，都会触发这个函数"""
        print("正在处理信息")
        print(f'第{col + 1}列')
        self.form.table.blockSignals(True)  # 暂停接收信号 #不然_proccess_data自己触发自己，会死循环的
        if col == 0:  # 如果把款号设成"",就删除整行；反之把颜色设成""
            article = self._get_item_text(row, col)
            if not article:
                self._remove_row(row)
            # else:
            #     color = self._to_QTW('', str)
            #     self.form.table.setItem(row, 1, color)

        if col == 1:  # 如果设置了颜色（也就是款号和颜色齐了后），就获取“件数/箱”和“单价”，并设置第2列和第5列
            color = self._get_item_text(row, col)
            article = self._get_item_text(row, 0)
            df = self.article_df
            if (not color) or (not article):  # 如果颜色/款号缺少一个信息，就设置“件数/箱”空白
                pcs_per_box = self._to_QTW('', str)
                self.form.table.blockSignals(False)
                self.form.table.setItem(row, 2, pcs_per_box)
            else:
                '检索df["Articolo"] == article) & (df["Colore"] == color)的Series,获取只包含 "件数/箱"列的Series'
                try:
                    pcs_per_box_and_price = df[(df["Articolo"] == article) & (df['Colore'] == color)][
                        ['件数/箱', '标准售价（件）']].values.tolist()[0]
                except IndexError:
                    print('输入的Articolo和Colore有误，重试')
                    return
                self.form.table.blockSignals(False)
                pcs_per_box, price = pcs_per_box_and_price
                pcs_per_box = self._to_QTW(pcs_per_box)
                self.form.table.setItem(row, 2, pcs_per_box)  # 显示在Table上
                price = self._to_QTW(price, float)
                self.form.table.setItem(row, 5, price)

        elif col in (2, 3):
            pcs_per_box = self._get_item_text(row, 2)
            boxes = self._get_item_text(row, 3)
            if pcs_per_box.isdigit() and boxes.isdigit():
                pcs = int(pcs_per_box) * int(boxes)
                pcs = self._to_QTW(pcs)
                self.form.table.blockSignals(False)
                self.form.table.setItem(row, 4, pcs)
            elif pcs_per_box == '' or boxes == '':
                pcs = ''
                pcs = QTableWidgetItem(pcs)
                self.form.table.blockSignals(False)
                self.form.table.setItem(row, 4, pcs)

        elif col == 4:  # 件数
            pcs_per_box = self._get_item_text(row, 2)
            pcs = self._get_item_text(row, 4)
            boxes = self._get_item_text(row, 3)
            if pcs.isdigit() and boxes.isdigit():
                if int(boxes) != 0:
                    if int(pcs) % int(boxes) == 0:
                        pcs_per_box = int(pcs) / int(boxes)
                        pcs_per_box_item = self._to_QTW(pcs_per_box)
                    else:
                        pcs_per_box_item = QTableWidgetItem('不可用')
                    self.form.table.setItem(row, 2, pcs_per_box_item)
            '完成‘件数’和‘件数/箱’、‘箱数’的联动后，还需要设置‘件数’和‘总金额’的联动'
            price = self._get_item_text(row, 5)
            if price.replace('.', '').isdigit() and pcs.isdigit():
                amount = float(price) * int(pcs)
                amount = self._to_QTW(amount, float)
                self.form.table.setItem(row, 6, amount)
                self._update_amount_label()
            elif price == '' or pcs == '':
                amount = self._to_QTW('', str)
                self.form.table.setItem(row, 6, amount)
                self._update_amount_label()

        elif col == 5:  # 单价
            price = self._get_item_text(row, col)

            price_item = self._to_QTW(price, str)
            price_item = QTableWidgetItem(price_item)
            self.form.table.setItem(row, col, price_item)
            pcs = self._get_item_text(row, 4)

            if price.isdigit() and pcs.isdigit():
                price = float(price)
                pcs = int(pcs)
                amount = f'{price * pcs :.2f}'
                amount = QTableWidgetItem(amount)
                self.form.table.setItem(row, 6, amount)
                self._update_amount_label()
            else:
                amount = ''
                amount = QTableWidgetItem(amount)
                self.form.table.setItem(row, 6, amount)
                self._update_amount_label()
        self.form.table.blockSignals(False)  # 恢复接收信号

    def _insert_new_row(self):
        n_rows = self.form.table.rowCount()
        self.form.table.setRowCount(n_rows + 1)

    def _remove_selected(self):
        items = self.form.table.selectedItems()
        if isinstance(items, Iterable) and not isinstance(items, str):
            for item in items:
                row = item.row()
                self._remove_row(row)
            if not items:  # 如果items是空列表
                row = self.form.table.rowCount() - 1
                article = self.form.table.item(row, 0)
                article = article.text() if isinstance(article, QTableWidgetItem) else article
                if not article:
                    self._remove_row(row)
        elif isinstance(items, QTableWidgetItem):
            row = items.row()
            self._remove_row(row)

    def _remove_row(self, row: int):
        self.form.table.removeRow(row)
        n_rows = self.form.table.rowCount()
        if n_rows < 10:  # remove_selected里有loop，这里不需要用while
            self._insert_new_row()

    def _save_order(self):  # todo
        """传参进来的df先存成self._df，然后要保存时，self._get_current_table_df获取当前的df，对比self._df。
        如果self._df.empty，那么就是新的单据， 反之则调用alter语句。"""
        '获取self._df（如果有）和table_df（get_current_table_df） 两个dataframe'
        if hasattr(self, "_df"):
            db_df = self._df.copy()
        else:
            db_df = pd.DataFrame()
        table_df = self._get_current_table_df
        if table_df.empty:
            QMessageBox.about(self, '提示', '当前单据有空白行，请检查后重试')
            return
        '先填充ArtId'
        articles = self.article_df
        articles = articles[['ArtId', 'Articolo', 'ColoreId', 'Colore']]
        articles.set_index(['Articolo', 'Colore'], inplace=True)
        table_df['Search_index'] = table_df[['Articolo', 'Colore']].apply(
            lambda x: tuple(x), axis=1).values.tolist()
        for col in articles.columns:
            table_df[col] = table_df['Search_index'].apply(lambda x: articles.loc[x, col])
        table_df.drop('Search_index', axis=1, inplace=True)
        '再检查客户名字，填充ClienteId'
        client_name = self.form.ClientComBox.currentText()
        if client_name != '--':
            clients_df = self._clients_df.copy()
            clients_df.set_index('DisName', inplace=True, drop=True)
            client_id = clients_df.at[client_name, "ClienteId"]
            table_df['ClienteId'] = client_id
        else:
            QMessageBox.about(self, '你没选客户', '当前客户为“--”,请选择正确的客户重试')
            return
        id_num = self.form.BillComBox.currentText()
        id_num = int(id_num)
        table_df['id'] = id_num
        data = self.form.SaleDateEdit.date().toPyDate()
        data = data.strftime('%Y-%m-%d')
        table_df['Data'] = str(data)
        articles_df = self._article_df[['Articolo', 'ColoreId', 'Colore']].copy()
        articles_df.set_index(['Articolo', 'Colore'], drop=True, inplace=True)
        table_df['Search index'] = table_df[['Articolo', 'Colore']].apply(
            lambda x: tuple(x), axis=1).values.tolist()  # 创造索引列：（Art,ColId），用于索引
        table_df.loc[:, 'Colore'] = table_df['Search index'].apply(lambda x: articles_df.loc[x, 'ColoreId'])
        table_df = table_df.rename(columns={'Colore': 'ColoreId'})
        table_df.drop('Search index', axis=1, inplace=True)
        extralarge = self.form.ExtraLargeLineEdit.text()
        extralarge = float(extralarge)
        table_df['加单费'] = extralarge
        discount = self.form.DiscountLineEdit.text()
        discount = float(discount)
        table_df['折扣'] = discount
        payment = self.form.PaymComBox.currentText()
        table_df['付款方式'] = payment

        payment_value = self.form.PaymentLineEdit.text()
        payment_value = float(payment_value)
        table_df['付款金额'] = payment_value
        debt_value = self.form.TotDebtValue.text()
        debt_value = float(debt_value.replace('€', ''))
        tot_amount = self.form.TotAmountValue.text()
        tot_amount = float(tot_amount.replace('€', ''))
        if debt_value == tot_amount:
            table_df['付款方式'] = '欠款'
        table_df['欠款金额'] = debt_value
        '需要先填充table_df的列才能对比'
        if db_df.empty:
            query = self._session.session.query(Sales).where(Sales.id == 1)
            df = self._session.read_sql_query(query)
            dtypes = df.dtypes.to_dict()
            for col, dtype in dtypes.items():
                table_df.loc[:, col] = table_df[col].astype(dtype)
            result = self._session.input_excel(Sales, table_df)
            print(f'{result}\n\n')
            msg = result[-1][-1]
            print(msg)
            QMessageBox.about(self, '提示', msg)
        # else:
        #     print(table_df ==db_df)
        pass


class ArticleDelegate(QStyledItemDelegate):
    def __init__(self, parent=None, df: pd.DataFrame = None):
        """\n给OrderWindow代理Articolo"""
        super().__init__(parent)
        if isinstance(df, pd.DataFrame):
            self.df = df
        else:
            self.df = pd.DataFrame()

    def createEditor(self, parent, option: Any, index: Any):
        """"""
        '获取产品df'
        product_list = self.df.Articolo.unique()
        product_list = [str(x) for x in product_list]
        article_combox = QComboBox(parent)
        article_combox.setEditable(True)
        article_combox.addItems(product_list)
        article_combox.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        article_combox.lineEdit().setAlignment(Qt.AlignmentFlag.AlignLeft)

        return article_combox


class ColorDelegate(QStyledItemDelegate):
    def __init__(self, parent=None, df: pd.DataFrame = None, articles: Iterable = []):
        """\n给OrderWindow代理Colore"""
        super().__init__(parent)
        if isinstance(df, pd.DataFrame):
            self.df = df
        else:
            self.df = pd.DataFrame(columns=['Articolo', 'Colore'])
        self.articles = articles

    def createEditor(self, parent, option: Any, index: Any):
        article = self.articles[index.row()]
        temporary_df = self.df.loc[self.df['Articolo'] == article, :].copy()
        temporary_df.loc['', :] = ''
        self.df.loc[self.df['Articolo'] == article, :] = self.df[self.df['Articolo'] == article].sort_values(['Colore'])
        color_list = self.df[self.df['Articolo'] == article]['Colore'].values.tolist()
        color_combox = QComboBox(parent)
        color_combox.setEditable(True)
        color_combox.addItems(color_list)
        color_combox.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        color_combox.lineEdit().setAlignment(Qt.AlignmentFlag.AlignLeft)
        return color_combox


class PcsBoxesAmountDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        """给剩下的列代理LineEdit（除了总金额）"""
        super().__init__(parent)

    def createEditor(self, parent, option: Any, index: Any):
        if index.column() != 6:  # 如果不是总金额，就用LineEdit代理
            lineedit = QLineEdit(parent)
            lineedit.setAlignment(Qt.AlignmentFlag.AlignLeft)
            if index.column() == 5:  # 如果是价格列，就检查是不是浮点
                validator = QDoubleValidator(parent=lineedit)
                validator.setBottom(0)
                lineedit.setValidator(validator)
            else:  # 其余列全部检查是不是整数
                validator = QIntValidator(parent=lineedit)
                validator.setBottom(0)
                lineedit.setValidator(validator)
            return lineedit
        else:  # pass掉就等于禁止修改总金额
            pass


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        gui = SalesPart()
        sys.exit(app.exec())

    except Exception as e:
        import traceback
        import time

        traceback.print_exc()
        print(e)
        time.sleep(10000000)
