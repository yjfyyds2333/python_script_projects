import requests,time,random
from config import HEADERS,TIMEOUT,logger

# 发送请求
def fetch_page(url):
    try:
        response = requests.get(url,headers=HEADERS,timeout=TIMEOUT)
        time.sleep(random.uniform(1.5,2.5))
        response.raise_for_status() # 非200状态码抛出异常
        logger.info(f"请求成功:{url}")
        return response.text
    
    except Exception as e:
        logger.error(f"请求失败:{url},错误:{e}")
        return None

