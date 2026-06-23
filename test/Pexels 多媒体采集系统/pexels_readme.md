---
AIGC:
    Label: "1"
    ContentProducer: 001191110102MACQD9K64018705
    ProduceID: 907551919054137_0/project_7650382242090320143-files/学习路线/pexels_readme.md
    ReservedCode1: ""
    ContentPropagator: 001191110102MACQD9K64028705
    PropagateID: 907551919054137#1782200246402
    ReservedCode2: ""
---
# Pexels 多媒体采集系统

基于 Pexels 官方 API 的图片+视频批量采集工具，支持关键词搜索、分页采集、断点续采、元数据存储与导出。

## 功能特性

- **图片采集**：按关键词搜索，支持选择 original/large2x/large/medium/small 等多种尺寸下载
- **视频采集**：按关键词搜索，支持 min/sd1/sd2/hd720/hd1080 五档清晰度选择
- **分页采集**：基于 next_page 自动翻页，支持指定采集页数
- **断点续采**：进度写入 progress.json，程序中断后重启自动从断点继续
- **增量采集**：下载前检测文件是否已存在，跳过已下载资源
- **元数据存储**：MongoDB upsert 去重存储，pandas 导出 Excel
- **异常处理**：请求超时重试（3次）、429限流自动等待、状态码检测
- **日志记录**：按日期生成日志文件，同时输出到控制台

## 技术栈

- Python 3.x
- requests（HTTP 请求 + 流式下载）
- pymongo（MongoDB 存储）
- pandas（数据导出 Excel）
- python-dotenv（环境变量管理）

## 项目结构

```
Pexels 多媒体采集系统/
├── Pexels 多媒体采集系统.py   # 主程序
├── .env                        # API Key 配置（不入库）
├── images/                     # 图片下载目录
├── videos/                     # 视频下载目录
├── photos_process.json         # 图片采集进度（运行时生成）
├── videos_process.json         # 视频采集进度（运行时生成）
├── Picture_{query}_excel_{date}.xlsx  # 图片元数据导出
├── Videos_{query}_excel_{date}.xlsx   # 视频元数据导出
└── run_{date}.log              # 运行日志
```

## 快速开始

### 1. 安装依赖

```bash
pip install requests pymongo pandas python-dotenv
```

### 2. 获取 API Key

前往 [Pexels API](https://www.pexels.com/api/) 注册并获取免费 API Key。

### 3. 配置环境变量

在项目根目录创建 `.env` 文件：

```
PEXELS_KEY=你的API Key
```

### 4. 运行

```python
if __name__ == "__main__":
    # 图片搜索存储
    pic_data, query = photos_download_pexels("happy", 15, "large", 3)
    save_picture(pic_data, query)

    # 视频搜索存储
    videos_data, query = videos_download_pexels("game", 6, "min", 3)
    save_video(videos_data, query)
```

## 参数说明

### photos_download_pexels(query, per_page, large, target_page)

| 参数 | 类型 | 说明 |
|------|------|------|
| query | str | 搜索关键词 |
| per_page | int | 每页数量（最大 80） |
| large | str | 图片尺寸：original / large2x / large / medium / small |
| target_page | int | 采集目标页数 |

### videos_download_pexels(query, per_page, hd_type, target_page)

| 参数 | 类型 | 说明 |
|------|------|------|
| query | str | 搜索关键词 |
| per_page | int | 每页数量（最大 80） |
| hd_type | str | 清晰度：min / sd1 / sd2 / hd720 / hd1080 |
| target_page | int | 采集目标页数 |

## 核心设计

### 断点续采

每页采集前将当前页信息写入 progress.json，程序崩溃重启后读取进度文件，从断点页重新采集。MongoDB 的 upsert 机制保证重复数据不会冲突。

### 异常处理

- 所有请求设置 timeout=10s，避免无限等待
- 失败自动重试 3 次，间隔 2 秒
- 429 限流响应自动读取 Retry-After 头等待重试
- 重试耗尽后跳过当前请求，不中断整个程序

### 增量采集

下载前通过 os.path.exists 检测目标文件是否已存在，已存在则跳过下载。

## 注意事项

- Pexels API 免费版有请求频率限制，大批量采集建议降低 per_page 或增加请求间隔
- .env 文件包含 API Key，务必添加到 .gitignore
- 视频清晰度选择依赖 API 返回的 video_files 数量，少数视频可能不足 5 档

---

> 本内容由 Coze AI 生成，请遵循相关法律法规及《人工智能生成合成内容标识办法》使用与传播。
