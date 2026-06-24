## 项目简介

基于 Scrapy CrawlSpider 框架采集古文岛（guwendao.net）古诗文数据，支持文本、图片混合采集，实现了 CrawlSpider 自动链接跟踪、FilesPipeline 文件下载、自定义 Downloader Middleware、MongoDB 存储、Excel 导出和增量采集。

## 核心技术点

| 技术点 | 说明 |
|--------|------|
| CrawlSpider + Rule | 自动跟踪列表页翻页和详情页链接，无需手动 yield Request |
| LinkExtractor | 用正则匹配提取目标链接，过滤无关 URL |
| FilesPipeline | Scrapy 内置文件下载管道，自动下载、去重、SHA1 命名 |
| 自定义 Downloader Middleware | UA 随机池 + 403 自动重试 |
| MongoDB Pipeline | upsert 增量存储，按 poem_id 去重 |
| Excel Pipeline | openpyxl 逐行写入，爬虫结束时保存 |

## 项目结构

```
gushiwen_scrapy/
├── scrapy.cfg
├── gushiwen_scrapy/
│   ├── __init__.py
│   ├── items.py              # Item 定义（含 file_urls 字段）
│   ├── middlewares.py         # 自定义 Downloader Middleware
│   ├── pipelines.py           # MongoDB Pipeline + Excel Pipeline
│   ├── settings.py            # Scrapy 配置
│   ├── user-agents.json       # UA 随机池数据
│   ├── output/
│   │   ├── gushiwen.xlsx      # Excel 导出文件
│   │   └── pictures/
│   │       └── full/          # FilesPipeline 下载的图片（SHA1 命名）
│   └── spiders/
│       ├── __init__.py
│       └── gushiwen_spider.py # CrawlSpider 爬虫
```

## 功能实现

### F1 诗文文本采集（CrawlSpider）

使用 CrawlSpider 的 Rule 自动跟踪链接：

- **翻页 Rule**：`LinkExtractor(allow=r'/default_\d+\.aspx'), follow=True` — 自动跟踪列表页翻页
- **详情 Rule**：`LinkExtractor(allow=r'/shiwenv_\w+\.aspx'), callback='parse_detail'` — 自动进入详情页提取数据

提取字段：标题、作者、朝代、正文、译文、注释

### F2 图片采集（FilesPipeline）

使用 Scrapy 内置 FilesPipeline 自动下载图片：

- Item 中定义 `file_urls` 字段（必须是列表），Pipeline 自动下载
- 文件按 SHA1 哈希命名，自动去重
- 存储路径：`./output/pictures/full/`

### F3 元数据存储（MongoDB Pipeline）

```python
self.collection.update_one(
    {'poem_id': item['poem_id']},
    {'$set': {...}},
    upsert=True  # 存在则更新，不存在则插入
)
```

### F4 自定义 Downloader Middleware

- **UA 随机池**：从 `user-agents.json` 加载 UA 列表，每个请求随机选择
- **403 重试**：响应状态码为 403 时自动换 UA 重试

### F5 增量采集

MongoDB upsert 机制，按 `poem_id` 判断是否已存在，已存在则更新而非重复插入。

### F6 Excel 导出

openpyxl 逐行写入，字段：title、author、dynasty、text、translation

## 环境配置

### 依赖安装

```bash
pip install scrapy pymongo openpyxl python-dotenv
```

### .env 文件

```env
COOKIE=your_cookie_here
```

### MongoDB

默认连接本地 MongoDB，无密码：`MongoClient()`
数据库：`Poems`，集合：`poems`

## 运行

```bash
cd gushiwen_scrapy
scrapy crawl gushiwen_spider
```

## 采集数据示例

| 字段 | 示例 |
|------|------|
| poem_id | 829c726ccb42 |
| title | 静夜思 |
| author | 李白 |
| dynasty | 唐 |
| text | 床前明月光，疑是地上霜。举头望明月，低头思故乡。 |
| translation | 皎洁的月光洒在床前... |

## 踩坑记录

| 坑 | 解决方案 |
|----|----------|
| CrawlSpider 中不能定义 parse 方法 | parse 是 CrawlSpider 内部 Rule 调度用的，覆盖后 Rule 失效 |
| allowed_domains 写错旧域名 | 旧域名 gushiwen.cn 已不可访问，改为 guwendao.net |
| file_urls 必须是列表且字段名固定 | FilesPipeline 只认 `file_urls`（复数），且必须是列表 |
| img_url 为空字符串时传给 FilesPipeline 报错 | 加判断：空则设 `file_urls = []` |
| item 被字典覆盖 | 不要用 `item = {...}` 覆盖，应逐字段 `item['key'] = value` |

## 关键学习点

1. **CrawlSpider vs Spider**：规则驱动 vs 手动控制，列表→详情结构用 CrawlSpider 更简洁
2. **FilesPipeline**：声明式文件下载，只需传 URL 列表，Pipeline 自动处理下载、去重、命名
3. **Pipeline 生命周期**：`open_spider` → `process_item`（逐条）→ `close_spider`
4. **Downloader Middleware**：`process_request`（请求前）、`process_response`（响应后）、`process_exception`（异常时）
