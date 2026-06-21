GitHub Trending 监控系统

基于 Scrapy + SQLite + APScheduler 的 GitHub Trending 自动采集与评分系统，每日定时采集多个编程语言的热门仓库，按增长速度评分排序，采集完成后自动发送邮件报告。

功能

多语言采集：自动采集 Python / JavaScript / Go / Java / Rust 五个语言的每日 Trending Top 25
数据清洗：自动去除 star 数中的逗号，提取今日增长数字
评分系统：三维度综合评分（今日增长量 + 项目基数权重 + 连续上榜天数）
去重存储：联合主键 + INSERT OR REPLACE，同一仓库同一天不重复插入
定时调度：APScheduler 每天定时自动运行
采集报告：爬虫结束后控制台输出当日 Top 10 热门项目
邮件通知：采集完成后自动发送邮件报告（含采集状态和条数）

项目结构

plaintext
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
GitTrending_scrapy/
├── scrapy.cfg                          # Scrapy 配置
├── scheduler.py                         # APScheduler 定时调度入口
└── GitTrending_scrapy/
    ├── __init__.py
    ├── items.py                         # 数据模型定义
    ├── settings.py                      # Scrapy 配置（含邮件参数）
    ├── extensions.py                     # Scrapy 扩展（邮件通知）
    ├── middlewares.py                    # 中间件
    ├── pipelines.py                      # 数据清洗 + SQLite 存储 + 评分
    ├── project.db                        # SQLite 数据库
    └── spiders/
        ├── __init__.py
        └── GITthrending_spider.py       # 爬虫主体



技术栈

表格
组件	用途
Scrapy	爬虫框架
SQLite	数据存储
APScheduler	定时调度
smtplib	邮件通知
XPath	页面解析

快速开始

1. 安装依赖

bash
1
2
pip install scrapy apscheduler



2. 配置邮件通知（可选）

编辑 settings.py，填入你的 QQ 邮箱授权码：

python
1
2
3
4
5
6
REPORT_SENDER = "your_email@qq.com"
REPORT_PASSWORD = "your_smtp_auth_code"  # 不是登录密码，是SMTP授权码
REPORT_RECEIVER = "your_email@qq.com"
REPORT_SMTP_SERVER = "smtp.qq.com"
REPORT_SMTP_PORT = 465



3. 运行爬虫

单次运行：

bash
1
2
3
cd GitTrending_scrapy
scrapy crawl GITthrending_spider



定时运行（每天 10:00 自动采集）：

bash
1
2
python scheduler.py



评分规则

表格
维度	规则	分值
今日增长量	≤100 stars	+20
	101-1000 stars	+30
	1001-10000 stars	+40
	>10000 stars	+45
项目基数	<1000 stars（早期项目）	+50
	1001-10000 stars	+35
	10001-100000 stars	-10
	>100000 stars（大项目增长放缓）	-20
连续上榜	连续上榜天数 × 30	每天加30分

数据库结构

sql
1
2
3
4
5
6
7
8
9
10
CREATE TABLE git_trending (
    repo_name          VARCHAR(200),    -- 仓库名 (owner/repo)
    repo_language      VARCHAR(50),     -- 编程语言
    repo_star_total    INTEGER,         -- 总 star 数
    repo_star_today_increase INTEGER,   -- 今日新增 star
    repo_spider_date   DATE,            -- 采集日期
    repo_score         INTEGER DEFAULT 0, -- 综合评分
    PRIMARY KEY (repo_name, repo_spider_date)
);



常用查询

sql
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
-- 今日 Top 10
SELECT * FROM git_trending 
WHERE repo_spider_date = date('now') 
ORDER BY repo_score DESC LIMIT 10;


-- 某仓库历史趋势
SELECT repo_spider_date, repo_star_total, repo_star_today_increase 
FROM git_trending 
WHERE repo_name = 'owner/repo' 
ORDER BY repo_spider_date ASC;


-- 某语言今日上榜项目
SELECT * FROM git_trending 
WHERE repo_spider_date = date('now') AND repo_language = 'Python' 
ORDER BY repo_score DESC;



数据流

plaintext
1
2
3
4
5
6
7
8
9
10
11
12
13
14
GitHub Trending 页面
       ↓
  Scrapy Spider (XPath 解析)
       ↓
  Item Pipeline (数据清洗)
       ↓
  SQLite 存储 (INSERT OR REPLACE 去重)
       ↓
  评分计算 (增长量 + 基数 + 连续天数)
       ↓
  close_spider (控制台报告 Top 10)
       ↓
  Extension (邮件通知采集结果)

