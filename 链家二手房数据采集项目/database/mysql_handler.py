import pymysql
from config import db_config,logger,EXCEL_FILE

def init_db():
    # 连接数据库(已经创建好的)以及创建游标
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    # 执行插入语句
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS lj_houses(
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        `标题` VARCHAR(255) NOT NULL,
        `总价`  INT NOT NULL,
        `单价` INT NOT NULL,
        `面积` FLOAT NOT NULL,
        `户型` VARCHAR(20),
        `楼层` INT NOT NULL,
        `区域` VARCHAR(50),
        `小区` VARCHAR(50),
        `关注人数` INT NOT NULL,
        `发布时间` DATE NOT NULL,
        INDEX idx_district (`区域`),
        INDEX idx_community (`小区`) 
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;'''
    ) 
    
    conn.commit()
    logger.info('数据库初始化成功')
    return conn,cursor

def save_houses(conn,cursor,houses_results):
    if not houses_results or len(houses_results) == 0:
        return '没有数据可以保存'
    for houses_result in houses_results:
        cursor.execute('''
        INSERT INTO lj_houses(`标题`,`总价`,`单价`,`面积`,`户型`,`楼层`,`区域`,`小区`,`关注人数`,`发布时间`)
        VAlUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ''',(
            houses_result.get("标题"),
            houses_result.get("总价"),
            houses_result.get("单价"),
            houses_result.get("面积"),
            houses_result.get("户型"),
            houses_result.get("楼层"),
            houses_result.get("区域"),
            houses_result.get("小区"),
            houses_result.get("关注人数"),
            houses_result.get("发布时间"),
        ))

        conn.commit()
    logger.info(f'成功爬取到{len(houses_results)}条数据)')

def save_to_excel(houses_results):
    import pandas as pd
    try:
        df = pd.DataFrame(houses_results)
        df.to_excel(EXCEL_FILE,index=False)
        logger.info(f"成功导出EXCEL,存放地址为:{EXCEL_FILE}")
    except Exception as e:
        logger.error(f'出错了,:{e}')
        return None
    
    

