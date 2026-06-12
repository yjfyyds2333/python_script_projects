from config import logger
from lxml import etree
from crawler.cleaner import clean_area,clean_total_price,clean_unit_price,clean_floor,clean_publish_time,clean_star_num


def parse_html(html,houses_results):
    '''解析网页，获取房屋数据'''
    if not html:
        logger.error('未找到网页代码,无法解析')
        return houses_results
    
    tree = etree.HTML(html)
    try:
        house_cards = tree.xpath('//div[@class="info clear"]')
        houses_links = tree.xpath('//a[@class="noresultRecommend img LOGCLICKDATA"]/@href')

        if not house_cards or len(house_cards) == 0:
            logger.warning('未获取到任何房屋卡片')
    except Exception as e:
        logger.error(f'获取房屋卡片失败,失败原因:{e}')
        return f'{e}'

    for i,house in enumerate(house_cards):
        try:
            logger.info(f'正在爬取第{i+1}条数据.......')

            houses_link = houses_links[i]

            if not houses_links:
                houses_links = None

            try:
                title = house.xpath('.//div[@class="title"]/a/text()')[0]
            except Exception as e:
                logger.error(f'字段获取失败:原因:{e}')

            try:
                total_price = house.xpath('.//div[@class="totalPrice totalPrice2"]/span/text()')[0] 
                total_price = clean_total_price(total_price)
            except Exception as e:
                logger.error(f'字段获取失败:原因:{e}')
            
            try:
                unit_price = house.xpath('.//div[@class="unitPrice"]/span/text()')[0]
                unit_price = clean_unit_price(unit_price)
            except Exception as e:
                logger.error(f'字段获取失败:原因:{e}')

            try:  
                houseinfos = house.xpath('.//div[@class="houseInfo"]/text()')[0]
                house_info_list = houseinfos.split("|")
                area = house_info_list[1].strip()
                area = clean_area(area)

                Floor_Plan = house_info_list[0].strip()
                floor = house_info_list[4].strip()
                floor = clean_floor(floor)
                region = house_info_list[2].strip()
            except Exception as e:
                logger.error(f'字段获取失败:原因:{e}')

            try:
                xiaoqu = house.xpath('.//div[@class="positionInfo"]/a/text()')[0]
                location = house.xpath('.//div[@class="positionInfo"]/a/text()')[1]
            except Exception as e:
                logger.error(f'字段获取失败:原因:{e}')

            try:
                star_infos = house.xpath('.//div[@class="followInfo"]/text()')[0]
                star_list = star_infos.split("/")
                star_num = star_list[0].strip()
                star_num = clean_star_num(star_num)

                publish_time = star_list[1].strip()
                publish_time = clean_publish_time(publish_time)

            except Exception as e:
                logger.error(f'字段获取失败:原因:{e}')
                
            houses_results.append({
                '标题':title,
                '总价':total_price,
                '单价':unit_price,
                '面积':area,
                '户型':Floor_Plan,
                '楼层':floor,
                '朝向':region,
                '小区':xiaoqu,
                '地区':location,
                '关注人数':star_num,
                '发布时间':publish_time,
                '房屋详细页':houses_link,
                })
            
        except Exception as e:
            logger.error(f'获取字段失败,原因:{e}')

    logger.info(f"解析成功,总共提取到{len(houses_results)}条数据")
    return houses_results


            
    