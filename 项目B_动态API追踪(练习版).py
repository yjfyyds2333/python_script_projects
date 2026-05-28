import requests
import os 
import sqlite3

dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(dir)

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36'
}

# 全局初始化：连接数据库、建表(只需在最开始时执行一次)
conn = sqlite3.connect("quotes.db")
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS quotes_table(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT,
    author TEXT
)
''')
conn.commit() # 提高表结构创建

api_infos = []
current_page = 1

while True:
    url = f'http://quotes.toscrape.com/api/quotes?page={current_page}'

    print(f"开始抓取第{current_page}页的信息.......")

    try:
        response = requests.get(url,headers=headers,timeout=10)
        # 增加状态码校验,非200直接报错走异常处理
        response.raise_for_status()
        api_info = response.json()
    except Exception as e:
        print(f"请求或解析失败,第{current_page}页终止,错误信息:{e}")
        break

    # 数据处理与批量写入
    quotes_list = api_info.get("quotes",[])

    # 处理数据
    for quote in quotes_list:
        text = quote["text"]
        author = quote["author"]["name"]

        # 插入单条数据
        cursor.execute('''
        INSERT INTO quotes_table(text,author)
        VALUES(?,?)
        ''',(text,author)
        )

    # 性能优化：按页提交事务,减少磁盘 I/O 损耗
    conn.commit()
    print(f"第{current_page}页成功写入数据库")

    if not api_info.get("has_next") or not quotes_list:
        print(f"已经到达最后一页，共{current_page}页,采集自动停止。")
        break

    current_page += 1

    if current_page >= 6:
        break

# 流程闭环:退出前释放数据库连接资源
cursor.close()
conn.close()




