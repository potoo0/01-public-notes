#!/u01/miniconda3/bin/python
from typing import List

import time
import argparse
import pandas as pd
from pangres import upsert
from sqlalchemy import create_engine, inspect

from loguru import logger


def insert2Db(conn_str: str, table: str, df: pd.DataFrame):
    """插入或更新数据到关系型数据库.

    Args:
        conn_str: 连接字符串, 带驱动名. 如: mysql+pymysql://...
        table: 数据表名称
        df: 待插入的 dataframe, 其 index 必须命名! 并且对应数据表的主键
    """
    engine = create_engine(conn_str)
    # 获取数据表字段类型
    insp = inspect(engine)
    col_dtype = {}
    for col_def in insp.get_columns(table):
        col_dtype[col_def['name']] = col_def['type']

    # 一次至多传输 1024 * 1024 byte, 即 1MB 的数据
    chunk_byte_size = 1024 * 1024
    chunk_row = int(df.shape[0] / max(1, df.memory_usage(deep=True).sum() / chunk_byte_size))

    # 主键重复时更新
    # create_schema, add_new_columns, adapt_dtype_of_empty_db_columns 不需要,
    # 表在 db 里已经创建好, 这些字段为 False 可以加快效率
    res_chunks_gen = upsert(
        engine=engine,
        df=df,
        table_name=table,
        if_row_exists='update',
        dtype=col_dtype,
        chunksize=chunk_row,
        yield_chunks=True,
        create_schema=False,
        add_new_columns=False,
        adapt_dtype_of_empty_db_columns=False
    )

    res_row_cnt = 0
    for chunk_gen in res_chunks_gen:
        res_row_cnt += chunk_gen.rowcount
        if not chunk_gen.closed:
            chunk_gen.close()
    if df.shape[0] <= res_row_cnt:
        logger.info(f'共 {df.shape[0]} 条记录, 处理 {res_row_cnt} 条记录.')
    else:
        logger.error('--------------- 错误 ---------------')
        logger.error(f'共 {df.shape[0]} 条记录, 处理 {res_row_cnt} 条记录.')


def buildDf(csvpath: str, colunms: List[str], pk: List[str], sep=','):
    """从 csv 文件构建 dataframe.

    Args:
        csvpath: csv 文件路径
        colunms: csv 列名，与数据表字段对应
        pk: 主键
        sep: csv 文件列分隔符, 默认为英文逗号

    Returns:
        dataframe
    """
    df = pd.read_csv(
        csvpath,
        header=None,
        names=colunms,
        sep=sep
    )
    if not pk:
        logger.error('错误, 主键不能为空!')
        raise ValueError('错误, 主键不能为空!')
    df.set_index(pk, inplace=True)

    return df


def cmdArg():
    parser = argparse.ArgumentParser(description='同步 csv 到 mysql.')
    parser.add_argument(
        "--conn_str",
        dest="conn_str",
        type=str,
        required=True,
        help="数据库连接字符串, 已默认 utf8, 如: mysql://root:root@localhost:3306/testdb"
    )
    parser.add_argument(
        "--username",
        dest="username",
        type=str,
        required=True,
        help="数据库用户名"
    )
    parser.add_argument(
        "--password",
        dest="password",
        type=str,
        required=True,
        help="数据库密码"
    )
    parser.add_argument(
        "--table",
        dest="table",
        type=str,
        required=True,
        help="数据库表名"
    )
    parser.add_argument(
        "--pk",
        dest="pk",
        type=str,
        required=True,
        help="数据表主键"
    )
    parser.add_argument(
        "--csvpath",
        dest="csvpath",
        type=str,
        required=True,
        help="csv 文件路径"
    )
    parser.add_argument(
        "--colunms",
        dest="colunms",
        type=str,
        required=True,
        help="csv 文件路径"
    )
    parser.add_argument(
        "--sep",
        dest="sep",
        type=str,
        default=',',
        help="csv 文件间隔符, 默认为英文逗号"
    )
    args = parser.parse_args()

    # 为 conn_str 拼接账户以及驱动, 如果是 mysql 则添加驱动 pymysql
    acc = ''
    if args.username:
        acc = f'{args.username}:{args.password}@'
    args.conn_str = f'mysql+pymysql://{acc}{args.conn_str.split("mysql://")[1]}'
    # 为 conn_str 加编码, 默认为 utf8
    charset = 'charset=utf8'
    if 'charset=' not in args.conn_str:
        if '?' in args.conn_str:
            args.conn_str += '&' + charset
        else:
            args.conn_str += '?' + charset

    # 转化 pk, colunms 为 List[str]
    args.pk = args.pk.split(',')
    args.colunms = args.colunms.split(',')
    return args


def main():
    args = cmdArg()
    logger.info(f'参数: {args}')
    df = buildDf(args.csvpath, args.colunms, args.pk, args.sep)
    insert2Db(args.conn_str, args.table, df)


if __name__ == '__main__':
    st = time.time()
    main()
    logger.info(f'time cost: {time.time() - st}')
