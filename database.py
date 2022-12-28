# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 20:21:15 2022

@author: demishu
"""
import datetime
import os
from collections.abc import Iterable
from queue import Queue
from threading import Thread

import numpy as np
import pandas as pd
from sqlalchemy import create_engine, Integer, String, Date, Float, Column,\
    UniqueConstraint, ForeignKey, ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Query
from sqlalchemy.orm.decl_api import DeclarativeMeta

'DIY调试处'
echo = False

today = datetime.datetime.now()
if today >= datetime.datetime(today.year, 6, 1):
    interval = f'{today.year}-{today.year + 1}'
else:
    interval = f'{today.year - 1}-{today.year}'
con = create_engine(f'sqlite:///erp {interval}.db', echo=echo)
'正式部分'
Base = declarative_base()


class RoutineDB(Base):
    __abstract__ = True
    '是否有单号？ （有单号的table就像流水账一般，会重复）。 反例：产品列表'
    with_id = None
    '检测行是否允许有重复'
    accept_duplicates = None
    'subset参数用于把df写入数据库时做检查，到时候input_df参数会删去subset重复的行'
    subset = None

    def format_df(df):
        return df


class Italy_cities_info(RoutineDB):
    __tablename__ = 'info_citta_italiane'
    riga = Column(Integer, primary_key=True, autoincrement=True)
    Prov = Column(String(45), index=True)
    CodProv = Column(String(4), index=True)
    Regione = Column(String(25), index=True)
    CAP_ini = Column('CAP ini', String(20))
    CAP_fin = Column('CAP fin', String(20))


class Clients(RoutineDB):
    __tablename__ = 'lista_clienti'
    riga = Column(Integer, primary_key=True, autoincrement=True)
    ClienteId = Column(Integer, unique=True)
    Nome = Column(String(20), index=True)
    地址 = Column(String(50))
    Prov = Column(String(45), ForeignKey(Italy_cities_info.Prov), index=True)
    CodProv = Column(String(4), ForeignKey(Italy_cities_info.CodProv), index=True)
    CAP = Column(String(20))
    Regione = Column(String(25), ForeignKey(Italy_cities_info.Regione), index=True)
    国家 = Column(String(20))
    电话 = Column(String(20))
    ForeignKeyConstraint((Prov, CodProv, Regione),
                         [Italy_cities_info.Prov, Italy_cities_info.CodProv, Italy_cities_info.Regione],
                         name='fk_info_Clients__city_prov_reg')
    '不允许重复的行'
    subset = ['ClienteId']

    def format_df(df):  # 这是个超后期的功能，没必要现在写
        # 函数根据CAP来补充所有剩下的城市/国家信息
        '把CAP先转换成衣袋里常见的字符'
        df.loc[:, 'CAP'] = df['CAP'].astype(str)
        df.loc[:, 'CAP'] = df['CAP'].apply(lambda x: x if len(x) == 5 else '0' * (5 - len(x)) + x)
        # '''true_series有个Column列，该列表明了df的CAP还是Prov是可用信息（优先Prov),
        # 然后根据可用信息从 cities_info获取剩余信息来填充df'''
        # true_series = df[['Prov','CAP']].notna().copy()
        # true_series ['Column'] = true_series['Prov'].apply( lambda x: 'Prov' if x is True else np.nan)
        # true_series.loc [true_series['Column'].isna(),'Column'] = \
        #     true_series['CAP'].apply( lambda x: 'CAP' if x is True else np.nan)
        # print(true_series)
        # for col in ['Prov', 'CAP']:
        #     print(f'\n\n\n开始{col}部分的循环')
        #     '''ref_df是 df [col].notna()部分的【引用】！！！！，直接修改df本身。
        #     例子：在col为Prov时，ref_df就是df[Prov].notna()的所有行,
        #     修改ref_df==直接修改df[Prov].notna()的部分'''
        #     ref_df = df.loc[true_series['Column'] == col, :]
        #     print(ref_df)
        #     if ref_df.empty:
        #         print(f'df的{col}列没有有效信息，跳过剩余部分')
        #         continue
        #     cities_info = pd.read_sql_table(Italy_cities_info.__tablename__, con, index_col = 'riga')
        #     cities_info = cities_info.set_index(col, drop =True)
        #     if 'riga' in cities_info.columns:
        #         cities_info.drop('riga', axis = 1, inplace = True)
        #     print(cities_info)
        #     for cities_col in cities_info.columns:
        #         print(f'开始填充df的{cities_col}列')
        #         print(ref_df[cities_col])
        #         print(ref_df[col])
        #         ''
        #         ref_df.loc[:,cities_col] = ref_df.loc[:,col]\
        #                 .apply(lambda x: cities_info.loc[x, cities_col])

        #         print(df)
        # # for column in cities_info.columns:
        # #     df[df[f'{column} check'],column] = 
        # print(df)
        return df


class Articles(RoutineDB):
    __tablename__ = 'lista_articoli'
    riga = Column(Integer, primary_key=True, autoincrement=True)
    ArtId = Column(Integer, unique=True)
    Articolo = Column(String(10), index=True)
    ColoreId = Column(Integer, index=True)
    Colore = Column(String(10))
    尺码 = Column(String(10))
    件数_箱 = Column("件数/箱", Integer)
    标准售价_件 = Column("标准售价（件）", Float, index=True)
    UniqueConstraint('Articolo', '标准售价（件）', name='ArtPrice')
    UniqueConstraint('Articolo', 'ColoreId', name='ArtArt')

    '不允许重复的列（复合唯一索引）'
    subset = ['ArtId', 'Articolo', 'ColoreId']

    def format_df(df):
        df.loc[:, 'Articolo'] = df['Articolo'].astype(str)
        df.loc[:, "ArtId"] = range(1, len(df['Articolo']) + 1)
        return df


class Stocks(RoutineDB):
    '''这张表用于记录
    ‘1311 黑色 30件/箱 10箱
    1311 黑色 29件/箱 1箱
    1311黑色 27件/箱 1箱’
    这样的数据， 因此， [Articolo, ColoreId,件数/箱] 是这里的subset
    '''

    __tablename__ = 'lista_rimanenze'
    riga = Column(Integer, primary_key=True, autoincrement=True)
    ArtId = Column(Integer, ForeignKey(Articles.ArtId), unique=True)
    库存_件 = Column('库存（件）', Integer)
    库存_箱 = Column('库存（箱）', Integer)

    '不允许重复的列（复合唯一索引）'
    subset = ['ArtId']

    def format_df(df):
        '''需要对比产品表的信息，自动补全空白信息。'''
        '自动补全空白列名'
        articles_info = pd.read_sql_table('lista_articoli', con, index_col='riga')
        articles_info = articles_info[['ArtId', 'Articolo', 'ColoreId', '件数/箱', '标准售价（件）']]

        '补全箱数、件数'
        df = pd.merge(df, articles_info, on='ArtId')
        df.loc[:, 'Articolo'] = df['Articolo'].astype(str)
        columns_order = list(df.columns)
        boxes = df.fillna(method='ffill', axis=1)[
            df['库存（箱）'].isna()][['Articolo', '库存（箱）', '件数/箱']]  # 如果箱数空，则补全箱数：准备箱数boxes_df
        boxes.loc[:, '库存（箱）'] = boxes['库存（箱）'] // boxes['件数/箱']
        boxes = boxes[['Articolo', '库存（箱）']]
        pcs = df.fillna(method='bfill', axis=1)[
            df['库存（件）'].isna()][['Articolo', '库存（件）', '件数/箱']]  # 如果件数空，则补全件数:准备件数pcs_df
        pcs.loc[:, '库存（件）'] = pcs['库存（件）'] * pcs['件数/箱']
        pcs = pcs[['Articolo', '库存（件）']]
        df = df.combine_first(boxes)  # 补全箱数
        df = df.combine_first(pcs)  # 补全件数
        df.loc[:, ['库存（件）', '库存（箱）']] = df.loc[:, ['库存（件）', '库存（箱）']].astype(int)
        df = df[columns_order]
        df.loc[:, 'Articolo'] = df['Articolo'].astype(str)
        df.loc[:, ['ColoreId', '件数/箱']] = df[['ColoreId', '件数/箱']].astype(int)
        df = df[['ArtId', '库存（件）', '库存（箱）']]
        return df


class Sales(RoutineDB):
    __tablename__ = 'lista_vendite'
    riga = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Integer, index=True)
    Data = Column(Date)
    ClienteId = Column(Integer, ForeignKey(Clients.ClienteId, name='fk_Cli_Sales'))
    ArtId = Column(Integer, ForeignKey(Articles.ArtId), index=True)
    件数_箱 = Column('件数/箱', Integer, index=True)
    箱数 = Column(Integer, index=True)
    件数 = Column(Integer)
    单价_件 = Column('单价（件）', Float, index=True)
    总价 = Column(Float, index=True)
    加单费 = Column(Float)
    折扣 = Column(Float)
    付款方式 = Column(String(20), index=True)
    付款金额 = Column(Float, index=True)
    欠款金额 = Column(Float)

    '有单据'
    with_id = True

    def format_df(df):
        '补全[件数/箱，单价（件）]列名'
        articles_info = pd.read_sql_table(Articles.__tablename__, con, index_col='riga')
        articles_info = articles_info[['ArtId', '件数/箱', '标准售价（件）']]
        articles_info = articles_info.rename(columns={'标准售价（件）': '单价（件）'})
        articles_info.set_index('ArtId', inplace=True)  # 设置（ArtId）索引
        for column in articles_info.columns:  # 补全所有列
            df.loc[df[column].isna(), column] = df[df[column].isna()] \
                ['ArtId'].apply(lambda x: articles_info.loc[x, column])

        '补全空白日期'
        df.loc[:, 'Data'] = df['Data'].fillna(
            datetime.datetime.now()
        )
        '设置格式'
        df.loc[:, "Data"] = df['Data'].apply(lambda x: x.date() if isinstance(x, datetime.datetime) else x)
        '重新计算件数/总价'
        df.loc[:, '件数/箱'] = df['件数/箱'].astype(int)
        df.loc[:, '箱数'] = df['箱数'].astype(int)
        df.loc[:, '件数'] = df['件数/箱'] * df['箱数']
        df.loc[:, '单价（件）'] = df['单价（件）'].astype(float)
        df.loc[:, '总价'] = df['单价（件）'] * df['件数']
        '填空'
        df.loc[:, ['加单费', '折扣']] = df[['加单费', '折扣']].fillna(0)
        '付款方式为欠款的单据默认全欠'
        df.loc[df['付款方式'] == '欠款', '付款金额'] = 0
        '计算欠款金额'
        df_groupby = df[['id', '总价']].groupby('id').sum()
        df.loc[:, '欠款金额'] = df['id'].apply(lambda x: df_groupby.at[x, '总价']) \
                                - df['付款金额'] + df['加单费'] - df['折扣']
        return df


# 备份
# class Sales(RoutineDB):
#     __tablename__ = 'lista_vendite'
#     riga = Column(Integer, primary_key = True, autoincrement = True)
#     id = Column(Integer, index = True)
#     Data = Column(Date)
#     ClienteId = Column(Integer, ForeignKey(Clients.ClienteId, name = 'fk_Cli_Sales'))
#     Articolo = Column(String(10))
#     ColoreId = Column(Integer)
#     件数_箱 = Column('件数/箱', Integer)
#     箱数 = Column(Integer, index = True)
#     件数 = Column(Integer)
#     单价_件 = Column('单价（件）', Float)
#     总价 = Column(Float, index = True)
#     加单费 = Column(Float)
#     折扣 = Column(Float)
#     付款方式 = Column(String(20), index = True)
#     付款金额 = Column(Float, index = True)
#     欠款金额 = Column(Float)
#     ForeignKeyConstraint(
#             [Articolo, ColoreId, 件数_箱,单价_件],
#             [Articles.Articolo, Articles.ColoreId, Articles.件数_箱, Articles.标准售价_件], 
#             name = 'fk_Sto_Sales')
#     Index('SalArt', Articolo, ColoreId, 件数_箱,单价_件)

#     '有单据'
#     with_id = True

#     def format_df (df):
#         '补全[件数/箱，单价（件）]列名'
#         articles_info = pd.read_sql_table(Articles.__tablename__, con, index_col= 'riga')
#         articles_info = articles_info [['Articolo','ColoreId','件数/箱','标准售价（件）']]
#         articles_info = articles_info.rename(columns={'标准售价（件）':'单价（件）'})
#         articles_info.loc[:,['Articolo','ColoreId']] = articles_info.loc \
#             [:,['Articolo','ColoreId']].astype(str)     #把Articolo和ColoreId转化成str
#         articles_info.set_index(['Articolo','ColoreId'], inplace = True)    #设置（Art,ColId）复合索引
#         df.loc[:,['Articolo','ColoreId']] = df.loc[:,['Articolo','ColoreId']].astype(str) #df的Art和Col也转化成str
#         df['Search index'] = df[['Articolo','ColoreId']].apply(
#             lambda x: tuple(x), axis = 1).values.tolist()   #创造索引列：（Art,ColId），用于索引
#         for column in articles_info.columns:    #补全所有列
#             df.loc[df[column].isna(),column] = df[df[column].isna()]\
#                 ['Search index'].apply(lambda x: articles_info.loc[x,column])
#         df.drop('Search index', axis =1, inplace=True) #删去索引列
#         '补全空白日期'
#         df.loc[:,'Data'] = df['Data'].fillna(
#             datetime.datetime.now()
#             )
#         '设置格式'
#         df.loc[:,"Data"] = df['Data'].apply(lambda x: x.date() if isinstance(x, datetime.datetime) else x)
#         df.loc[:,'Articolo'] = df.loc[:,'Articolo'].astype(str)
#         df.loc[:,'ColoreId'] = df['ColoreId'] .astype(int)
#         '重新计算件数/总价'
#         df.loc[:,'件数'] = df['件数/箱'] * df['箱数']
#         df.loc [:,'总价'] = df['单价（件）'] *df['件数']
#         '填空'
#         df.loc[:,['加单费','折扣']] = df[['加单费','折扣']].fillna(0)
#         '付款方式为欠款的单据默认全欠'
#         df.loc[df['付款方式'] == '欠款','付款金额'] = 0
#         '计算欠款金额'
#         df_groupby = df[['id', '总价']].groupby('id').sum()
#         df.loc[:,'欠款金额'] = df['id'].apply(lambda x: df_groupby.at[x,'总价'])\
#                                 - df['付款金额'] + df['加单费'] - df['折扣']
#         return df    

class Replenishment(RoutineDB):  # 未测试
    __tablename__ = 'lista_rifornimenti'
    riga = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Integer, index=True)
    Documento = Column(String(10), index=True)  # 柜单
    ArtId = Column(Integer, ForeignKey(Articles.ArtId), index=True)
    件数_箱 = Column('件数/箱', Integer, index=True)
    件数 = Column(Integer)
    箱数 = Column(Integer)
    运费 = Column(Float)
    Data = Column(Date, index=True)

    '有单据'
    with_id = True


class AccIdMapping(RoutineDB):  # todo
    '财务id和原id的映射表'
    __tablename__ = 'acc_id_mapping'
    riga = Column(Integer, primary_key=True, autoincrement=True)
    id = Column('财务id', Integer, unique=True)
    原id = Column(Integer, index=True)
    原id表名 = Column(String(20), index=True)
    项目名称 = Column(String(50), index=True)

    table_dict = {"客户": Clients, "款式": Articles}

    @classmethod
    def format_df(cls, df):  # todo
        "如果传入的df是空白的，就获取全部的客人/款式，来尝试生成完整的映射表"
        acc_id_mapping = pd.read_sql_table(cls.__tablename__, con, index_col='riga')
        if df.empty:
            clients = pd.read_sql_table(Clients.__tablename__, con, index_col='riga')
            print(clients)
            clients['原id表名'] = '客户'
            clients['项目名称'] = clients['Nome']
            clients = clients[['ClienteId', '原id表名', '项目名称']]
            clients.rename(columns={"ClienteId": "原id"}, inplace=True)

            articles = pd.read_sql_table(Articles.__tablename__, con, index_col='riga')
            articles['原id表名'] = '款式'
            articles['项目名称'] = articles['Articolo'].apply(lambda x: str(x)) + '-' + articles['Colore']
            articles = articles[['ArtId', '原id表名', '项目名称']]
            articles.rename(columns={"ArtId": "原id"}, inplace=True)
            df = pd.concat([clients, articles])
            df['财务id'] = np.nan
            df = df[['财务id', '原id', '原id表名', '项目名称']]
            df.reset_index(drop=True, inplace=True)
            df.index += 1
        else:
            pass
        if acc_id_mapping.empty:
            df.loc[:, '财务id'] = range(1, df.shape[0] + 1)

        else:  # todo 没测试
            print(df)
            df = df.combine_first(acc_id_mapping)
            df.loc[:, '财务id'] = df['财务id'].astype(int)
            print(df)
            print(type(df['财务id'].max() + 1), df['财务id'].max() + 1)
            df.loc[df['财务id'].isna(), '财务id'] = range(
                int(df['财务id'].max() + 1),
                int(df['财务id'].max() + 1 + df[df['财务id'].isna()].shape[0])
            )

            ...
        return df


class Accounting(RoutineDB):
    __tablename__ = 'libro_giornale'
    riga = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Integer, index=True)
    Data = Column(Date, index=True)
    ContoDare = Column(String(50))
    ContoDareId = Column(Integer, ForeignKey(AccIdMapping.id), index=True)
    ContoAvere = Column(String(50))
    ContoAvereId = Column(Integer, ForeignKey(AccIdMapping.id), index=True)
    ImportoDare = Column(Float)
    ImportoAvere = Column(Float)
    checked = Column(Integer, index=True)
    Nota = Column(String)
    GiornoIscrizione = Column(Date, index=True)

    '有单据的表'
    with_id = True

    def format_df(df):
        df["GiornoIscrizione"] = df["GiornoIscrizione"].fillna(
            datetime.datetime.now()
        )
        df.loc[:, 'Data'] = df['Data'].apply(lambda x: x.date())
        df.loc[:, "GiornoIscrizione"] = df['GiornoIscrizione'].apply(lambda x: x.date())
        return df


Base.metadata.create_all(con)
SQLAlchemySession = sessionmaker(bind=con)


class MySession:

    def __init__(self, Session=SQLAlchemySession):
        self._session = Session()
        self._con = self._session.bind

    @property
    def session(self):
        return self._session

    @property
    def con(self):
        return self._con

    def read_sql_query(self, QueryObj):
        '检查QueryObj是不是Query类。'
        if isinstance(QueryObj, Query):
            query_obj = QueryObj
            df = pd.read_sql_query(query_obj.statement, self._con)

            df = df.fillna(np.nan)

            if 'riga' in df.columns:
                df.set_index('riga', drop=True, inplace=True)
            return df
        else:
            print(f'输入的QueryObj {QueryObj} 参数不是SQLAlchemy.orm.Query类，请检查后重试')

    def read_sql_table(self, BaseClass):
        '检查BaseClass是不是DeclarativeMeta类'
        if isinstance(BaseClass, DeclarativeMeta):
            QueryObj = self.session.query(BaseClass.__table__)
            df = pd.read_sql_query(QueryObj.statement, con=self._con)
            df = df.fillna(np.nan)
            df.set_index('riga', drop=True, inplace=True)
            return df
        else:
            print(f"输入的的BaseClass {BaseClass}不是继承Base的子类，请检查后重试")

    def __help_input_excel(self, i, couple, length, q):
        print("进度条")
        print(f"{i}/{length}")
        BaseClass, path = couple
        if isinstance(BaseClass, DeclarativeMeta):
            if isinstance(path, str):
                if os.path.isfile(path):  # 检测path是不是文件路径，如果不是文件路径就检查path是不是DataFrame
                    if path.endswith('.csv'):
                        df = pd.read_csv(path)
                    elif path.endswith('.xlsx') or path.endswith('.xls'):
                        df = pd.read_excel(path)
                    else:
                        print(f'参数path = {path} 不是xlsx/xls/csv文件，请重试')
                        return
                    self._input_df(BaseClass, df, q)
                else:
                    print(f'path:{path} 不是文件，请重试。')
                    return
            elif isinstance(path, pd.DataFrame):  # 如果是DataFrame就直接赋值
                df = path
                self._input_df(BaseClass, df, q)
            else:
                print(f'参数 path = {path} 既不是路径也不是DataFrame，请重试')
        else:
            print(f"BaseClass {BaseClass}不是Base的子类，请重试")

    def __trasform_into__inputable_tuple(self, args=None, kwargs=None):
        '''这个函数接受input_excel的args和kwargs，因此这个函数的形参应该为args， kwargs而不是*args, **kwargs'''

        def true_if_no_str_iterable(CheckObj):
            return bool(isinstance(CheckObj, Iterable) and not isinstance(CheckObj, str))

        def __return_tuple_BaseClass_PathOrDataFrame(first, second):
            couple = ()
            if isinstance(first, DeclarativeMeta):
                if isinstance(second, pd.DataFrame) or os.path.isfile(second):
                    couple = (first, second)
            elif isinstance(second, DeclarativeMeta):
                if isinstance(first, pd.DataFrame) or os.path.isfile(first):
                    couple = (second, first)
            return couple

        if not args:
            if kwargs:  # 如果args为空， 先把kwargs改写成args，然后直接调用args的部分
                args = []
                for k, v in kwargs.items():
                    if isinstance(k, DeclarativeMeta):
                        couple = (k, v)
                    elif isinstance(v, DeclarativeMeta):
                        couple = (v, k)
                    else:
                        print(f'字典kwargs {kwargs}里的 {k}:{v}中没有Base的子类，请重试')
                        continue
                    args.append(couple)
                args = tuple(args)
        while True:
            if true_if_no_str_iterable(args):
                if isinstance(args, dict):
                    print('args是dict，正在转换成tuple(BaseClass, path or DataFrame)')
                    items = []
                    couple = ()
                    for k, v in args.items():
                        couple = __return_tuple_BaseClass_PathOrDataFrame(k, v)
                        if couple:
                            items.append(couple)
                            couple = ()
                    args = tuple(items)
                    break
                if len(args) == 1:
                    if true_if_no_str_iterable(args[0]):
                        print('args被包在tuple内部了，正在取出args并赋值给args')
                        args = args[0]
                    else:
                        print(f'args：{args}不符合规范，请重试')
                        return
                if len(args) == 2:
                    first, second = args
                    couple = __return_tuple_BaseClass_PathOrDataFrame(first, second)
                    if couple:
                        print('args已格式化成(BaseClass, path or DataFrame)')
                        args = (couple,)
                        break
            print('尝试格式化args')
            if true_if_no_str_iterable(args):
                try:
                    check_tuple = (True if len(couple) == 2 else False for couple in args)
                    check_series = pd.Series(check_tuple)
                    if true_if_no_str_iterable(args) and check_series.all():
                        items = []
                        print('开始排序')
                        for item in args:
                            first, second = item
                            couple = __return_tuple_BaseClass_PathOrDataFrame(first, second)
                            if couple:
                                items.append(couple)
                        print('排序成功，开始返回')
                        args = tuple(items)
                        break
                    else:
                        continue
                except TypeError:
                    print(f'args：{args}不符合输入格式，请重试')
                    return
            else:
                print(f'args{args}不是Iterable,请重试')
                return

        print("args格式化成功，开始返回args.\n")
        return args

    def input_excel(self, *args, **kwargs):
        """可用的参数：{Table1:path1, Table2:path2, ...}
            [[Table1,path1],[Table2,path2],...]
        """
        args = self.__trasform_into__inputable_tuple(args, kwargs)
        if args is None:
            print('请检查args是不是符合要求的迭代器')
            return
        '到这里位置， args应该是((BaseClass,path/df),)这样的格式了'
        q = Queue()
        results = []
        threads = []
        length = len(args)
        for i, couple in enumerate(args, start=1):
            '多线程写入'
            threads.append(Thread(target=self.__help_input_excel(i, couple, length, q)))
            threads[-1].start()
            if couple[0] in (Italy_cities_info, Clients, Articles):
                threads[-1].join()
        for couple in args:
            results.append((couple, q.get()))
        return results

    def _input_df(self, BaseClass, df, q=None):
        """"""
        '获取df和数据库里的db，检查是否重复输入'
        df = BaseClass.format_df(df)
        db_df = self.read_sql_table(BaseClass)

        '填充np.nan为'' '
        df = df.fillna('')
        if not db_df.empty:
            db_df.index += 1
        db_df = db_df.fillna('')

        '获取riga（也叫indice）的最大值'
        max_indice = db_df.index.max()
        if max_indice is np.nan:
            max_indice = 0
        '传参'
        with_id = BaseClass.with_id
        accept_duplicates = BaseClass.accept_duplicates
        subset = BaseClass.subset
        q_valid = False
        if isinstance(q, Queue):
            q_valid = True
        # 完成传参

        if len(df.columns) != len(db_df.columns):
            '检查输入的df是不是缺斤少两（缺列）'
            check_array = list(df.columns)
            check_array = [True if x in db_df.columns else False for x in check_array]
            check_array = np.array(check_array)
            if check_array.all():
                return_text = '输入的DataFrame缺少个别列，请检查'
                raise return_text
                if q_valid:
                    q.put(return_text)
        else:
            '检查列名是不是完全一致'
            df = df[db_df.columns]
            if not (df.columns == db_df.columns).all():
                return_text = f'''输入的DataFrame列名不符合数据表规范，
                      请修改成以下列名再重试\n{list(db_df.columns)}'''
                raise return_text
                if q_valid:
                    q.put(return_text)

        '''如果是有单据的'''
        if with_id:
            df = df[db_df.columns]
            print(df)
            print(db_df)
            # print(df==db_df)
            print(f'{BaseClass.__tablename__}有id列，开始检查')
            '如果是with_id的table的话，除了max_index还需要获取max_id'
            max_id = db_df['id'].max()
            if max_id is np.nan:
                max_id = 0
            df['新表'] = True
            df.index += max_indice + 1
            df = pd.concat([df, db_df])
            df.loc[:, '新表'] = df['新表'].fillna(False)
            no_duplicates_cols = []
            for col in df.columns:
                if col in ('id', '新表'):
                    continue
                no_duplicates_cols.append(col)

            '''不知道为啥，这段代码不能放在_input_df开头，总之这样写可以保证新输入的行
            和之前输入的行被识别成同一行，然后被drop_duplicates掉'''
            if not db_df.empty:
                dtypes = db_df.dtypes.to_dict()
                for col, dtype in dtypes.items():
                    df.loc[:, col] = df[col].astype(dtype)
            print(df)
            df = df.drop_duplicates(subset=no_duplicates_cols, keep=False)
            print(df)
            df.loc[df['新表'] == True, 'id'] = df.loc[df['新表'] == True, 'id'] - df.loc[df['新表'] == True, 'id'].min()
            df.loc[df['新表'] == True, "id"] += max_id + 1
            df = df[df['新表']]
            print(df)
            df.drop('新表', axis=1, inplace=True)

        elif accept_duplicates:  # 2022/09/23不知道这个参数存在的意义，也许能删掉
            '修正riga，不然to_sql容易报错'
            print(f"{self._table_name}允许出现重复行，正在写入")
        else:
            print(f"{BaseClass.__tablename__}不允许{subset if subset is not None else ''}出现重复行，正在删除")
            df = df.rename(columns={df.index.name: 'riga'})
            if subset is None:
                subset = list(df.columns)
            df['新表'] = True
            df.index += max_indice + 1
            df = pd.concat([db_df, df], axis=0)
            df['新表'] = df['新表'].fillna(False)
            if not db_df.empty:
                dtypes = db_df.dtypes.to_dict()
                for col, dtype in dtypes.items():
                    df.loc[:, col] = df[col].astype(dtype)
            df = df.drop_duplicates(subset=subset, keep=False)
            df = df[df['新表'] == True]
            df = df.drop('新表', axis=1)
        df = df.reset_index(drop=True)
        df.index += max_indice + 1
        df = df.replace('', np.nan)
        if df.empty:
            return_text = '数据库里已经有df包含的数据了，故此不写入重复的数据。'
            print(return_text)
            if q_valid:
                q.put(return_text)
        else:
            print(f'\n正在往{BaseClass.__tablename__}里写入：\n{df}\n')
            df.to_sql(BaseClass.__tablename__, self._con, if_exists="append", index=True, index_label="riga")
            return_text = '写入成功'
            print(return_text)
            if q_valid:
                q.put(return_text)


if __name__ == '__main__':
    session = MySession()
    # cities_info = pd.read_excel("./测试用excel/informazioni citta.xlsx", dtype = np.str_) #后期功能，没必要现在写
    # session.input_excel( (Italy_cities_info, cities_info))                                #后期功能，没必要现在写

    acc_id_mapping = session.read_sql_table(AccIdMapping)
    'todo'
    df = pd.DataFrame()
    df = AccIdMapping.format_df(df)

    input_tuple = (
        (Accounting, './测试用excel/财务记账表.xlsx'),
        (Articles, "./测试用excel/产品表.xlsx"),
        (Clients, './测试用excel/客户列表.xlsx'),
        (Stocks, "./测试用excel/库存表.xlsx"),
        (Sales, "./测试用excel/销售记录.xlsx"),
        (AccIdMapping, pd.DataFrame())
    )
    try_dict = (('./测试用excel/财务记账表.xlsx', Accounting),
                ("./测试用excel/产品表.xlsx", Articles),
                ('./测试用excel/客户列表.xlsx', Clients),
                ("./测试用excel/库存表.xlsx", Stocks),
                (pd.DataFrame(), AccIdMapping)
                )

    results = session.input_excel(input_tuple)
    acc = session.read_sql_table(Accounting)
    art = session.read_sql_table(Articles)
    cities_info = session.read_sql_table(Italy_cities_info)
    clients = session.read_sql_table(Clients)
    stocks = session.read_sql_table(Stocks)
    sales = session.read_sql_table(Sales)
    acc_id_mapping = session.read_sql_table(AccIdMapping)
