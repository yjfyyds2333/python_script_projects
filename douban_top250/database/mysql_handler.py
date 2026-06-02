from config import DB_PATH,EXCEL_FILE,logger
import pymysql
import pandas as pd

def init_db():
    # 创建数据库并连接
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='Yjf15113137810',
        db='movies_top250'
    )
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS douban_movies (
        id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
        电影名 TEXT,
        评分 TEXT,
        评价人数 INT NOT NULL,
        简介 TEXT,
        主页链接 TEXT
    )
    ''')

    conn.commit()
    logger.info("数据库初始化成功")
    return conn,cursor

def save_movies(conn,cursor,movies):
    '''批量保存电影到数据库'''
    if not movies:
        return '没有数据可以保存'
    
    for movie in movies:

        cursor.execute('''
    INSERT INTO douban_movies(电影名,评分,评价人数,简介,主页链接)
    VAlUES(%s,%s,%s,%s,%s)
    ''',(
        movie.get("电影名"),
        movie.get("评分"),
        movie.get("评价人数"),
        movie.get("简介"),
        movie.get("主页链接")
    ))
        
    conn.commit()
    logger.info(f'成功保存{len(movies)}条数据')

def save_to_excel(movies):
    df = pd.DataFrame(movies)
    df.to_excel(EXCEL_FILE,index=False)