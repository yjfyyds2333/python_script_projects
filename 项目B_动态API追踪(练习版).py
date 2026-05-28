import requests
import os 
import sqlite3

dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(dir)

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36'
}

api_infos = []
page_alrealy = 0

while True:
    url = f'http://quotes.toscrape.com/api/quotes?page={page_alrealy+1}'

    print(f"开始抓取第{page_alrealy+1}页的信息.......")

    response = requests.get(url,headers=headers)
    api_info = response.json()

    # 连接/创建数据库(用sqlite3,python内置数据库)
    conn = sqlite3.connect("quotes.db") # 不存在则自动创建
    cursor = conn.cursor() # 创建游标(执行SQL)

    # 处理数据
    for quote in api_info["quotes"]:
        text = quote["text"]
        author = quote["author"]["name"]

        # 创建表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS quotes_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            author TEXT
        )
        ''')

        conn.commit()

        # 插入单条数据
        cursor.execute('''
        INSERT INTO quotes_table(text,author)
        VALUES(?,?)
        ''',(text,author)
        )
        conn.commit()

    # 查询数据
    cursor.execute("SELECT * FROM quotes_table")
    all_data = cursor.fetchall() # 获取全部
    for row in all_data:
        print(row)

    # 关闭连接
    conn.close()

    if api_info["has_next"]:
        pass
    else:
        break

    page_alrealy += 1
    if page_alrealy >= 5:
        break


