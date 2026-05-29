import os 
import logging 
from datetime import datetime

# 1.项目根目录(所有文件都用这个拼接路径)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2.日志文件夹创建
LOG_DIR = os.path.join(BASE_DIR,"logs")
os.makedirs(LOG_DIR,exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR,"crawler.logs")

# 3.日志配置(带文件、行号、函数名,报错秒定位)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s - %(module)s:%(lineno)d (%(funcName)s)",
    handlers=[
        logging.FileHandler(LOG_FILE,encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger() # 导出日志对象

# 4.全局变量
DOUBAN_BASE_URL = "https://movie.douban.com/top250?"

# 推荐的请求头配置（可直接复制）
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Referer': 'https://movie.douban.com/',  # 防盗链验证
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cookie':'bid=-knyR4yZRtc; _ga=GA1.2.717167617.1779964022; _gid=GA1.2.1323419641.1779964022; ll="118297"; _ga_Y4GN1R87RG=GS2.1.s1779964021$o1$g0$t1779964039$j42$l0$h0; _pk_id.100001.4cf6=db6c4c15f9498b08.1779964041.; __yadk_uid=IkVaNDTpWnOnnhK5m7dhbsTOXkSxm0qv; _vwo_uuid_v2=DD13FD979B89149DE58609315DF70EBEF|e642c04f72392c443383c77ff76a7671; __utmc=30149280; __utmc=223695111; ap_v=0,6.0; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1780038628%2C%22https%3A%2F%2Fsec.douban.com%2F%22%5D; _pk_ses.100001.4cf6=1; dbcl2="292314355:EJXnmVWrnEM"; ck=cQdS; __utma=30149280.717167617.1779964022.1780029111.1780038656.5; __utmb=30149280.0.10.1780038656; __utmz=30149280.1780038656.5.4.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utma=223695111.717167617.1779964022.1780029111.1780038656.5; __utmb=223695111.0.10.1780038656; __utmz=223695111.1780038656.5.4.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; push_noty_num=0; push_doumail_num=0'
}

TIMEOUT = 10

DB_PATH = os.path.join(BASE_DIR,"douban_movies.db") # 数据库路径

# excel文件夹创建
EXCEL_DIR = os.path.join(BASE_DIR,"output")
os.makedirs(EXCEL_DIR,exist_ok=True)
EXCEL_FILE = os.path.join(EXCEL_DIR,f"豆瓣电影TOP250_{datetime.now().strftime("%Y%m%d")}.xlsx")

