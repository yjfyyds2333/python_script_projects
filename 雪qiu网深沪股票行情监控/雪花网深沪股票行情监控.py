import requests,time
from pymongo import MongoClient
from datetime import datetime
from DrissionPage import ChromiumPage

page = ChromiumPage(9222)
page.get("https://xueqiu.com")
time.sleep(3) # 等待WAF挑战自动完成

# JS挑战完成后cookie自动存在浏览器里,直接拿
raw_cookies = page.cookies()

cookies = {}

xq_a_token = None
for c in raw_cookies:
    cookies[c["name"]] = c["value"]

print(cookies)

# print(f'"xq_a_token":{xq_a_token}')
# page.quit()


headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-HK;q=0.7',
    'origin': 'https://xueqiu.com',
    'priority': 'u=1, i',
    'referer': 'https://xueqiu.com/',
    'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
}

base_params = {
    'page': '1',
    'size': '30',
    'order': 'desc',
    'order_by': 'percent',
    'market': 'CN',
    'type': 'sh_sz',
}

class mongoDb:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client['stock']
        self.collection = self.db['xuehua_stock_sh_sz']
        print(f'数据库初始化完成')
        pass



def crawl():
    p = base_params.copy()

    for page in range(1,168):
        p['page'] = str(page)

        response = requests.get(
            'https://stock.xueqiu.com/v5/stock/screener/quote/list.json',
            params=p,
            cookies=cookies,
            headers=headers,
        )

        data = response.json()
        
        # 字段定义与赋值
        cards = data["data"]["list"]
        if not cards:
            print("未找到卡片")
            continue

        for card in cards:
            stock_code = card["symbol"]
            stock_name = card["name"]
            stock_current = card["current"]
            stock_percent = str(card["percent"]).strip() + "%"
            stock_chg = str(card["chg"]).strip() + "%"
            stock_current_year_percent = str(card["current_year_percent"]).strip() + "%"
            stock_volume = card["volume"]
            stock_amount = card["amount"]
            stock_turnover_rate = str(card["turnover_rate"]).strip() + "%"
            stock_pe_ttm = str(card["pe_ttm"]).strip()
            stock_dividend_yield = str(card["dividend_yield"]).strip() + "%"
            stock_market_capital = card["market_capital"]


            d1.collection.update_one(
                {"stock_code":stock_code},{
                    "$set":{
                        "stock_name":stock_name,
                        "stock_current":stock_current,
                        "stock_percent":stock_percent,
                        "stock_chg":stock_chg,
                        "stock_current_year_percent":stock_current_year_percent,
                        "stock_volume":stock_volume,
                        "stock_amount":stock_amount,
                        "stock_turnover_rate":stock_turnover_rate,
                        "stock_pe_ttm":stock_pe_ttm,
                        "stock_dividend_yield":stock_dividend_yield,
                        "stock_market_capital":stock_market_capital,
                        "update_date": datetime.now()
                    },
                "$push":{
                    "period_history":{
                        "stock_current":stock_current,
                        "stock_volume":stock_volume,
                        "date":datetime.now()
                    }
                }},
                upsert=True
            )

        print(f'采集完成！')

if __name__ == '__main__':
    d1 = mongoDb()
    crawl()





