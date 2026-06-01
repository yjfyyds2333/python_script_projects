import os 
import logging
import pandas as pd

# 用绝对路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 日志文件夹与文件创建
LOG_DIR = os.path.join(BASE_DIR,"logs")
os.makedirs(LOG_DIR,exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR,'crawler.log')

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s - %(module)s:%(lineno)d %(funcName)s",
    handlers=[
        logging.FileHandler(LOG_FILE,encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# 创建一个logging对象
logger = logging.getLogger()

# EXCEL文件路径与定义
EXCEL_DIR = os.path.join(BASE_DIR,'output')
os.makedirs(EXCEL_DIR,exist_ok=True)
EXCEL_FILE = os.path.join(EXCEL_DIR,'result.xlsx')

# 数据库配置
db_config = {
    "host":"localhost",
    "user":"root",
    "password":"Yjf15113137810",
    "db":"lj_houses_info",
    "charset":"utf8mb4"
}

# 全局定义区
LJ_BASE_URL = 'https://dg.lianjia.com/ershoufang/'

HEADERS = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    'Cookie':'SECKEY_ABVK=w8wlvtOaoB4kmJTXucFLMP4Ga8NAfL4zOdoAP6fzLGs%3D; lianjia_uuid=0e7b857b-dcb8-46e8-a9c7-9e4586d17ce5; select_city=441900; _jzqckmp=1; _ga=GA1.2.499664437.1780104192; _gid=GA1.2.1028464489.1780104192; crosSdkDT2019DeviceId=-qx4kti-j3e6x6-l3tfne7an0r48sr-qdyjemfc8; login_ucid=2000000540908395; lianjia_token=2.001243e109489f178e03eec838cf528cf7; lianjia_token_secure=2.001243e109489f178e03eec838cf528cf7; security_ticket=MLvvXzcjqZk+gGR9cpDpm5d4rgH7fm9blCUTfLrIKc5328yUv4K3VCm0nZ/Y8pGkyqcWTnCYwGIiywv78lJ/CqiajGxvgX3RSLyFSmLh+v/r85V8z1Wz9QFepISKR4HxDYFQCPLAlZ1TEreQMzx5J9iPL0a0YJy2zIANuVIZsH8=; ftkrc_=cb3e4b54-62cc-44f0-8a1d-a35e87e33622; lfrc_=db8deb76-106c-4658-b0a5-3e1890e3630b; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2219e67435e689fa-0007ef8c7fcc7e-26061151-2073600-19e67435e6984a%22%2C%22%24device_id%22%3A%2219e67435e689fa-0007ef8c7fcc7e-26061151-2073600-19e67435e6984a%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; lianjia_ssid=68a121df-d910-40a4-ac1d-2bda9b757bca; _jzqx=1.1780104184.1780126755.2.jzqsr=google%2Ecom|jzqct=/.jzqsr=hip%2Elianjia%2Ecom|jzqct=/; Hm_lvt_678d9c31c57be1c528ad7f62e5123d56=1780129129; _qzjc=1; _jzqa=1.1840263579898225700.1779848929.1780126755.1780131602.5; _jzqc=1; Hm_lvt_46bf127ac9b856df503ec2dbf942b67e=1779848928,1780104184,1780126753,1780131602; HMACCOUNT=9CF8D4A7BC376536; hip=cbvIZHtWlfrzwFeFJi3qVAn96lzXV813wKVRm6k5Bvqcp-79D47Typa8YXL-r_kbVT48RZKVuPhPnCgzyYPIZMFqs9MFmh0ibZH7W7RZgV1qas37V4LdSxDxhYfPoxyAiEZBKxQ1UQAbibifwjP87ussMUg89mNcYP56i-CL-vsKgbcr_Zv8V0lcaOHZjQWid5wUdchMfnS5vLXvQ24YIJBGGenfuMAiSenPr0M74kYW-OU7KBW5znXOoheFEB8rrkvkZEHfY8Lg4yKuUbJ3euOqbGyYrhqUHXzp; _gat=1; _gat_global=1; _gat_new_global=1; _gat_dianpu_agent=1; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiNjA5ZGM4NmQ0NzM4ODg3MDk0ZWIzZDAzNzA4OGYxOGYwYmEwNDMxN2RiODI3NTUyNmFiOTcwOTEzYTZjZjQxNDIyM2RhODg4YTkzNDlkN2RhYTk1ZjJjMjk3YWE2MTQ4ZTIxMTg4YzEzZWVlZDVlZjUwMmY0YTNkMGYyMWJlNGZiNTY4ZTFhY2QyNWQ5NzA2ZGJhNDE3YTBjMjc2MjA1MzVhNzU4MGIzNzcyM2QyMGJiNGYwMWEwODRmMTFhODhkNTQxMGEwYjZiOThjODQ2NGY2YzdjOTlhNGQ4ZmYxODdlNDBmYzNjOGZmNmNkNmFiMWI5YTBjYzcyYmMwY2I0M1wiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCI2NzM5MzNjNVwifSIsInIiOiJodHRwczovL2RnLmxpYW5qaWEuY29tL2Vyc2hvdWZhbmcvIiwib3MiOiJ3ZWIiLCJ2IjoiMC4xIn0=; Hm_lpvt_46bf127ac9b856df503ec2dbf942b67e=1780132222; _qzja=1.51924843.1780104184404.1780130768583.1780131601611.1780132216459.1780132222172.0.0.0.29.5; _qzjb=1.1780130768583.9.0.0.0; _qzjto=29.5.0; _jzqb=1.6.10.1780131602.1; _ga_8EKBN6G64V=GS2.2.s1780130785$o4$g1$t1780132224$j60$l0$h0',
    'Accept-anguage':'zh-CN,zh;q=0.9,en;q=0.8,zh-HK;q=0.7',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
}

TIMEOUT = 10

# playwright相关定义区
playwright = None # 总指挥官
browser = None # 浏览器
context = None # 独立会话(解决Cookie失效!)
page = None # 网页标签页

# 数据分析定义区
df = pd.read_excel(EXCEL_FILE,engine="openpyxl")
df = df.dropna(subset=["单价","面积","朝向"])
df["发布时间"] = pd.to_datetime(df["发布时间"],errors="coerce") 
df["publish_month"] = df["发布时间"].dt.to_period("M")
monthly_counts = df.groupby("publish_month")["标题"].count()

# 图表保存基础路径
CHART_BASE_DIR = EXCEL_DIR
