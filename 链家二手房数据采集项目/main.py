from config import logger,LJ_BASE_URL
from crawler.request_handler import fetch_page,init_browser,close_browser
from crawler.parse import parse_html
from crawler.paginator import get_next_url,has_nex_url
from database.mysql_handler import save_houses,save_to_excel,init_db
import time,random
from analysis.charts import zhu_chart,zhe_chart,bin_chart,avg_total_price,avg_unix_price


def main():
    # 1.初始化定义
    CURRENT_PAGE = 1
    current_url = LJ_BASE_URL + f'pg{CURRENT_PAGE}'
    conn,cursor = init_db()
    houses_results = []
    # 启动浏览器
    init_browser()

    try:
        while True:
            logger.info(f'开始爬取{current_url}')
            time.sleep(random.uniform(1.1,2.2))

            # 2.请求网址，得到源代码
            html = fetch_page(current_url)
            if html is None:
                break

            # 3.解析网址,采集数据
            houses_results = parse_html(html,houses_results)
            if houses_results is None:
                break

            # 4.判断是否还有下一页并获取下一页
            if not has_nex_url(html,CURRENT_PAGE):
                logger.info('已经没有下一页了,即将结束爬虫')
                break

            CURRENT_PAGE += 1
            current_url = get_next_url(CURRENT_PAGE)
            logger.info(f'下一页的网址是{current_url}')


    
    except Exception as e:
        logger.error(f'程序异常退出:原因:{e}')

    
    finally:
        # 5.保存数据
        save_houses(conn,cursor,houses_results)
        save_to_excel(houses_results)
        cursor.close()
        conn.close()
        close_browser()
        logger.info('数据库连接关闭')

def data_parse():
    print(f"经数据分析，东莞市链家二手房的平均房价为:{avg_unix_price}元/m²")
    print(f"经数据分析，东莞市链家二手房的平均总房价为:{avg_total_price}元")
    zhu_chart()
    zhe_chart()
    bin_chart()

    logger.info('√数据分析成功，导出图表成功!')

if __name__ == "__main__":
    # main()
    data_parse()


    


