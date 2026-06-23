import requests
from lxml import etree
import json

cookies = {
    'global_cookie': 'xgy0gqcysg1ke4x1o3b5h3x0k10mqndeetn',
    '__utma': '147393320.1225578681.1782021183.1782021183.1782021183.1',
    '__utmc': '147393320',
    '__utmz': '147393320.1782021183.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    'g_sourcepage': 'esf_fy%5Elb_pc',
    'city.sig': 'OGYSb1kOr8YVFH0wBEXukpoi1DeOqwvdseB7aTrJ-zE',
    'csrfToken': 'leyGXLeOwLpa4JtxcCRJg9Ag',
    'otherid': 'dbb7c4661875366f4939bb8d9241403a',
    '__utmt_t0': '1',
    '__utmt_t1': '1',
    '__utmt_t2': '1',
    'city': 'anqing',
    'unique_cookie': 'U_xgy0gqcysg1ke4x1o3b5h3x0k10mqndeetn*27',
    '__utmb': '147393320.75.10.1782021183',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-HK;q=0.7',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
    # 'cookie': 'global_cookie=xgy0gqcysg1ke4x1o3b5h3x0k10mqndeetn; __utma=147393320.1225578681.1782021183.1782021183.1782021183.1; __utmc=147393320; __utmz=147393320.1782021183.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); g_sourcepage=esf_fy%5Elb_pc; city.sig=OGYSb1kOr8YVFH0wBEXukpoi1DeOqwvdseB7aTrJ-zE; csrfToken=leyGXLeOwLpa4JtxcCRJg9Ag; otherid=dbb7c4661875366f4939bb8d9241403a; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; city=anqing; unique_cookie=U_xgy0gqcysg1ke4x1o3b5h3x0k10mqndeetn*27; __utmb=147393320.75.10.1782021183',
}


def url_collect():
    # 收集二手房所有城市的网址(从a-z)
    response = requests.get('https://sh.esf.fang.com/newsecond/esfcities.aspx', cookies=cookies, headers=headers)

    html = response.text
    tree = etree.HTML(html)

    links_url = []
    a_cards = tree.xpath('//div[@class="onCont"]/ul')

    for city_li in a_cards:
        links = city_li.xpath('.//a')
        for list in links:
            link = 'https:' + list.xpath('.//@href')[0]
            if link not in links_url:
                links_url.append(link)
            else:
                continue
    

    with open('citys_url.txt','w') as f:
        f.write(str(links_url))


url_collect()
