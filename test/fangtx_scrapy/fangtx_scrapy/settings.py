# Scrapy settings for fangtx_scrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from dotenv import load_dotenv
import os 
from dotenv import load_dotenv

load_dotenv()

BOT_NAME = "fangtx_scrapy"

SPIDER_MODULES = ["fangtx_scrapy.spiders"]
NEWSPIDER_MODULE = "fangtx_scrapy.spiders"

ADDONS = {}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "fangtx_scrapy (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False


# Concurrency and throttling settings
CONCURRENT_REQUESTS = 3
CONCURRENT_REQUESTS_PER_DOMAIN = 2
DOWNLOAD_DELAY = 1.5

RANDOMIZE_DOWNLOAD_DELAY = True

# 限制下载器空闲连接缓存，避免堆积
DOWNLOADER_CLIENT_TCP_KEEPALIVE_CONNECTION_TIMEOUT = 5

ITEM_PIPELINES = {'fangtx_scrapy.pipelines.FangtxScrapyPipeline': 300}

RETRY_ENABLED = True
RETRY_TIMES = 3 
RETRY_HTTP_CODES = [500,502,503,504,408,429]
DOWNLOAD_TIMEOUT = 15   # 超过15秒没响应就放弃这条请求

# 激活中间件
DOWNLOADER_MIDDLEWARES = {
    'fangtx_scrapy.middlewares.FangtxScrapyDownloaderMiddleware':543,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}

# 先用浏览器正常访问房天下，F12复制Cookie
load_dotenv() # 加载.env文件
DEFAULT_REQUEST_HEADERS = {
    'Cookie':os.getenv('FANGTX_COOKIE','')
}

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"

# 启用自定义扩展(优先级500，不影响其他扩展)
EXTENSIONS = {
    'fangtx_scrapy.extensions.SpiderReportExtension':500,
}

# 邮件通知配置
REPORT_SENDER = os.getenv("YX","")  # 发件邮箱
REPORT_PASSWORD = os.getenv("PASSWORD","")   # 不是登录密码，是SMTP专用授权码
REPORT_RECEIVER = os.getenv("YX","")   # 收件邮箱（可以和发件箱一致）
REPORT_SMTP_SERVER = "smtp.qq.com"  # QQ邮箱固定SMTP服务器
REPORT_SMTP_PORT = 465  # SSL端口，固定465


# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "fangtx_scrapy.middlewares.FangtxScrapySpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "fangtx_scrapy.middlewares.FangtxScrapyDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "fangtx_scrapy.pipelines.FangtxScrapyPipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
FEED_EXPORT_ENCODING = "utf-8"
