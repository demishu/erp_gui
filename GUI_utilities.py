# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 15:45:05 2022
@author: demishu
"""
import datetime
import os

from PyQt6 import uic
from PyQt6.QtCore import QDate, QByteArray
from PyQt6.QtGui import QIcon, QPixmap, QImage, QColor
from PyQt6.QtWidgets import QFrame

from icon import b64_icon


def get_icon(img_data = None, color=None, fmt='png'):
    """
    通过base64编码的图片字符串获取QIcon对象
    :param img_data: Base64编码的图片字符串
    :param color: 图片需要填充的颜色
    :param fmt: 图片的格式
    :return: 
    """
    if not img_data:
        pix = QPixmap(32, 32)
    else:
        data = QByteArray().fromBase64(img_data.encode())
        image = QImage()
        image.loadFromData(data, fmt)
        pix = QPixmap.fromImage(image)
    if color:
        pix.fill(QColor(color))

    return QIcon(pix)

def set_interval(first_day:str or None = None, last_day = None, interval = 365, fmt="%Y/%m/%d"):
    """set_interval(第一天,最后一天，间隔，格式)-->     (第一天，最后一天)     \n
        函数可以只输入(第一天)或者(间隔)-->           （第一天，今天）          \n
        默认返回                                     （上一个6月1日，今天）   \n
        fmt参数用于将输入的日期格式转换成datetime对象，然后统一输出成QDate
    """
    if last_day is None:
        last_day = datetime.datetime.now()
    else:
        try:
            last_day = datetime.datetime.strptime(last_day, fmt)
        except:
            raise("检查输入的最后一天")
    if first_day:
        try:
            first_day = datetime.datetime.strptime(first_day,fmt)

        except:
            raise('检查输入的第一天。')
    elif isinstance(interval,int):
        if last_day >= datetime.datetime(last_day.year,6, 1):
            prev_fi_year_first_day = datetime.datetime(last_day.year,6, 1)
        else:
            prev_fi_year_first_day = datetime.datetime(last_day.year-1,6, 1)
        fi_year_days = (last_day-prev_fi_year_first_day).days
        if interval > fi_year_days:
            first_day= prev_fi_year_first_day
        else:
            first_day = last_day - datetime.timedelta(interval)
    else:
        raise('输入的参数有误，请检查后重试。')
    first_day = QDate(first_day.year, first_day.month, first_day.day)
    last_day = QDate(last_day.year, last_day.month, last_day.day)
    return first_day, last_day

def get_DisName(series):
    '''用于给clients_df 新增DisName列，用于在GUI内展示
        clients_df['DisName'] = clients_df[['Nome','Prov','国家']]
                                    .apply(get_DisName, axis =1)
    '''
    DisName, prov, paese = series
    if DisName =='--':
        return DisName
    from numpy import nan
    if prov is not nan and prov !='':
        DisName += ' - ' + prov
    else:
        DisName += ' - ' + paese
    return DisName


class PartMetaClass(QFrame):
    def __init__(self, parent = None):
        super().__init__(parent)
        
        #如果有_ui_path这个属性
        if hasattr(self, "_ui_path"):
            if os.path.exists(self._ui_path):
                Form, GUI = uic.loadUiType(self._ui_path)
                self.root = GUI() 
                self.form = Form()
            else:
                raise IOError (f"设置UI异常.\n没找到UI文件：{self._ui_path}")
        
        #如果有_UiClass这个属性
        elif hasattr(self, "_UiClass"):
            self.root = self
            Form = self._UiClass
            self.form = Form()
        
        else:
            raise Exception("没有UI可以设置，显示空窗口没意思，就抛异常好了。")
            
        icon = get_icon(b64_icon)
        self.root.setWindowIcon(icon)
        self.form.setupUi(self.root)
        self.root.show()            