# Scrapy settings for guwendao_scrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "guwendao_scrapy"

SPIDER_MODULES = ["guwendao_scrapy.spiders"]
NEWSPIDER_MODULE = "guwendao_scrapy.spiders"

ADDONS = {}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "guwendao_scrapy (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Concurrency and throttling settings
#CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 1
CONCURRENT_REQUESTS = 1     # 并发数为1，礼貌爬虫
LOG_LEVEL = "INFO"          # 只显示INFO级别日志，不然输出太乱

ITEM_PIPELINES = {'guwendao_scrapy.pipelines.GuwendaoScrapyPipeline':300}

# 激活中间件
DOWNLOADER_MIDDLEWARES = {
    'guwendao_scrapy.middlewares.GuwendaoScrapyDownloaderMiddleware':543,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    # 数字是优先级,100-1000,越小越先执行
}

RETRY_ENABLED = True
RETRY_TIMES = 3 
RETRY_HTTP_CODES = [500,502,503,504,408,429]
# 注意：403不要加进去，403是对方主动拒绝，重试没用只会被封的更快
DOWNLOAD_TIMEOUT = 15 # 超过15秒没响应就放弃这条请求

# 启动自定义扩展(优先级500,不影响其他扩展)
EXTENSIONS = {
    'guwendao_scrapy.extensions.SpiderReportExtension':500,
}
# 邮件通知配置（替换为你自己的信息）
REPORT_SENDER = "3608872992@qq.com"  # 发件邮箱
REPORT_PASSWORD = "ntmnxkkehemodaba"  # 不是登录密码，是SMTP专用授权码
REPORT_RECEIVER = "3608872992@qq.com"  # 收件邮箱（可以和发件箱一致）
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
#    "guwendao_scrapy.middlewares.GuwendaoScrapySpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "guwendao_scrapy.middlewares.GuwendaoScrapyDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "guwendao_scrapy.pipelines.GuwendaoScrapyPipeline": 300,
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
