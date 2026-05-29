# ✅ 正确导入：导入模块里的具体函数，不是模块本身
from config import DOUBAN_BASE_URL, logger
from crawler.request_handler import fetch_page
from crawler.parser import parse_movies  # 导入解析函数
from crawler.paginator import has_nexturl,get_nexturl  # 导入分页函数
from database.mysql_handler import init_db, save_movies,save_to_excel


def main():
    movies_results = []
    CURRENT_PAGE = 0
    conn,cursor = init_db()
    current_url = DOUBAN_BASE_URL + f'start={CURRENT_PAGE}&filter='
    
    try:
        while True:
            logger.info(f'开始抓取:{current_url}')

            # 1.请求页面
            html = fetch_page(current_url)
            if html is None:
                break
            
            # 2.解析页面
            movies = parse_movies(html,movies_results=movies_results)

            if movies is None:
                break

            # 4.判断下一页
            if not has_nexturl(html):
                logger.info("已到最后一页，爬虫结束") 
                break

            # 5.生成下一页url
            CURRENT_PAGE += 25
            current_url = get_nexturl(CURRENT_PAGE)
            print(f'下一页的网址是:{current_url}')
        
        # 3.保存数据
        save_movies(conn,cursor,movies)
        save_to_excel(movies)

    except Exception as e:
        logger.error(f"程序异常退出:{e}")
        
    finally:
        # 确保数据库连接关闭
        cursor.close()
        conn.close()
        logger.info("数据库连接关闭")


if __name__ == "__main__":
    main()