from lxml import etree
from config import logger
import re

def parse_movies(html,movies_results):
    '''解析HTML，返回电影数据列表'''
    if not html:
        logger.warning("HTML内容为空,无法解析")
        return movies_results
    
    tree = etree.HTML(html)
    
    items = tree.xpath('//div[@class="item"]')
    print(f'一共获取到{len(items)}条信息')

    if not items or len(items) == 0:
        logger.error("找不到电影条目")
    try:
        for i,item in enumerate(items):
            try:
                print(f'正在抓取第{i+1}条信息')
                movie_name = item.xpath('.//span[@class="title"]/text()')[0].strip() 
                rating_num = item.xpath('.//span[@class="rating_num"]/text()')[0]
                rating_people = item.xpath('.//span[contains(text(),"人评价")]/text()')[0]
                rating_people = re.sub(r'[^\d]','',str(rating_people))
                intro =item.xpath('.//div[@class="bd"]/p/text()')[0].strip()
                link = item.xpath('.//div[@class="pic"]/a/@href')[0]
            except Exception as e:
                logger.warning(f'出现错误:{e}')

            movies_results.append({
                '电影名':movie_name,
                '评分':rating_num,
                '评价人数':rating_people,
                '简介':intro,
                '主页链接':link
            })

    except Exception as e:
        logger.error(f'出现错误:{e}')
    
    logger.info(f"解析成功,本页提取到{len(movies_results)}条数据")

    return movies_results



        

    