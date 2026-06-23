# 房天下二手房监控系统

基于 Scrapy + MongoDB + APScheduler 的全国二手房房源增量采集与监控系统。

## 项目简介

定时采集房天下（fang.com）全国各城市二手房列表页数据，存入 MongoDB，支持增量更新和历史价格变动追踪。每天自动运行一次，只采集新增房源或价格变动的房源，跳过未变化的数据。

## 功能特性

- **全国城市覆盖**：自动采集房天下所有城市二手房列表页 URL，支持批量采集
- **列表页采集**：标题、总价、单价、面积、户型、朝向、楼层、小区、区域
- **数据清洗**：面积去单位、楼层提取数字、单价提取数字
- **MongoDB 存储**：按房源 ID 去重，upsert 自动更新
- **增量采集**：已存在且价格未变的房源自动跳过
- **价格变动追踪**：$push 记录每次价格变动历史
- **重试机制**：Scrapy 内置重试中间件，失败最多重试 3 次
- **定时调度**：APScheduler 每天定时自动触发采集
- **邮件通知**：爬虫结束后自动发送采集报告邮件（基于 close_spider 信号）

## 技术栈

| 组件 | 技术 |
|------|------|
| 采集框架 | Scrapy |
| 数据库 | MongoDB (PyMongo) |
| 定时调度 | APScheduler |
| 数据清洗 | re 正则表达式 |
| 邮件通知 | smtplib |
| 城市URL采集 | requests + lxml |

## 项目结构

```
fangtx_scrapy/
├── scrapy.cfg                       # Scrapy 项目配置
├── scheduler.py                     # APScheduler 定时调度入口
├── url_collect.py                   # 城市URL采集脚本
└── fangtx_scrapy/
    ├── __init__.py
    ├── items.py                     # 数据模型定义
    ├── middlewares.py               # 下载中间件（UA轮换/重试）
    ├── pipelines.py                 # 数据管道（MongoDB存储+增量更新）
    ├── settings.py                  # 项目配置
    ├── extensions.py                # 扩展（邮件通知）
    ├── user-agents.json             # UA池（备用）
    └── spiders/
        ├── __init__.py
        ├── fangtx_spider.py         # 主爬虫
        ├── citys_url.json           # 全国城市URL列表
        └── citys_url.txt            # 城市URL文本备份
```

## 数据字段说明

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| house_id | string | 房源唯一ID（从URL提取） | "5419481" |
| house_title | string | 房源标题 | "南山三房 南向精装" |
| house_total_price | string | 总价（万） | "500" |
| house_unix_price | string | 单价（元/平米） | "4788" |
| house_type | string | 户型 | "3室2厅" |
| house_square | string | 面积（平米，纯数字） | "146.8" |
| house_towards | string | 朝向 | "南向" |
| house_floors | string | 楼层（纯数字） | "24" |
| house_community | string | 小区名称 | "家天下" |
| house_area | string | 所在区域 | "文峰塔 家天下" |
| last_update | datetime | 最后更新时间 | 2026-06-22T10:00:00 |
| price_history | array | 价格变动历史 | [{house_total_price: "500", date: "2026-06-22"}] |

## 快速开始

### 环境要求

- Python 3.10+
- MongoDB 6.0+
- pip 包：scrapy, pymongo, apscheduler, requests, lxml

### 安装

```bash
# 克隆项目
git clone https://github.com/yourname/fangtx_scrapy.git
cd fangtx_scrapy

# 安装依赖
pip install scrapy pymongo apscheduler requests lxml
```

### 配置

1. **启动 MongoDB**

```bash
# 本地 MongoDB 默认端口
mongod --dbpath /data/db
```

2. **配置 Cookie（重要）**

先用浏览器正常访问 `https://sz.esf.fang.com/house/`，F12 → Network → 复制请求头中的 Cookie，填入 `settings.py`：

```python
DEFAULT_REQUEST_HEADERS = {
    'Cookie': '你从浏览器复制的Cookie',
}
```

3. **配置邮件通知（可选）**

```python
# settings.py
REPORT_SENDER = "your_email@qq.com"
REPORT_PASSWORD = "SMTP授权码"       # 不是登录密码
REPORT_RECEIVER = "receiver@qq.com"
REPORT_SMTP_SERVER = "smtp.qq.com"
REPORT_SMTP_PORT = 465
```

### 运行

```bash
# 单次采集
cd fangtx_scrapy
scrapy crawl fangtx_spider

# 定时采集（每天10:00自动运行）
python scheduler.py
```

### 增量采集说明

- **第一次运行**：全量采集，所有房源数据入库
- **后续运行**：只采集新增房源或价格变动的房源，已存在且价格未变的自动跳过
- 查看日志中 `item_scraped_count` 对比两次运行的采集量，增量运行明显少于首次

## 数据查询示例

```javascript
// 查看深圳所有房源
db.fangtx.find({house_area: /深圳/})

// 查看价格变动过的房源（price_history有多条记录）
db.fangtx.find({"price_history.1": {$exists: true}})

// 查看总价低于100万的房源
db.fangtx.find({house_total_price: {$lt: "100"}})

// 查看某个小区的历史价格
db.fangtx.find({house_community: "家天下"}, {price_history: 1})
```

## 注意事项

- 房天下详情页有滑块验证码，本项目仅采集列表页数据
- Cookie 会过期，采集失败时需重新从浏览器复制 Cookie
- 建议设置 `DOWNLOAD_DELAY = 3` 以上，避免触发反爬
- `CONCURRENT_REQUESTS` 建议设为 1-3，并发过高容易被 302 拦截

## 已知问题

- [ ] UA 轮换中间件尚未生效（代码已编写但未激活）
- [ ] settings.py 中 EXTENSIONS 路径引用错误（GitTrending_scrapy → fangtx_scrapy）
- [ ] spider 中 house_area 缺失时使用了 return（应为 continue）
- [ ] Cookie 硬编码在 settings.py 中（应改为环境变量读取）


