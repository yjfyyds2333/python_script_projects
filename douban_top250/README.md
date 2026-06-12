# 豆瓣电影Top250 爬虫项目
一个**工程化、模块化**的豆瓣电影Top250数据爬虫，支持数据爬取、解析、数据库存储、Excel/CSV导出，附带完整日志记录与异常处理。

---

## 📌 项目介绍
本项目基于 Python 实现豆瓣电影 Top250 全站数据爬取，采用模块化开发思想，将**请求、解析、存储、导出**分离，代码易维护、易扩展，适合爬虫新手学习工程化开发。

**爬取数据包含**：电影名称、电影评分、评价人数、电影简介、电影详情链接

## 📁 项目结构
```
douban_top250/
├── config.py           # 全局配置文件（日志、路径、请求头、Cookie）
├── main.py             # 项目主入口（调度全流程）
├── crawler/            # 爬虫核心模块
│   ├── request_handler.py  # 网络请求模块
│   ├── parser.py          # 数据解析模块
│   └── paginator.py        # 分页处理模块
├── database/           # 数据库模块
│   └── mysql_handler.py   # SQLite数据库操作
├── output/             # 数据导出模块
│   └── export_excel.py    # Excel/CSV导出
├── logs/               # 日志自动生成目录
├── douban_movies.db    # SQLite数据库文件（自动生成）
└── requirements.txt    # 项目依赖
```

## ✨ 核心功能
1. **自动化爬取**：支持豆瓣Top250全10页数据自动翻页爬取
2. **稳定请求**：携带请求头+登录Cookie，解决403反爬限制
3. **智能解析**：XPath精准提取数据，空值安全处理，不崩溃
4. **数据存储**：自动创建SQLite数据库，批量存储数据
5. **数据导出**：支持导出为 Excel / CSV 文件
6. **完整日志**：控制台+文件双输出日志，精准定位报错
7. **异常处理**：全流程异常捕获，程序稳定运行

## 🛠️ 技术栈
- 爬虫：`requests` + `lxml`
- 数据库：`SQLite3`（轻量无需安装）\ MySQL
- 数据导出：`pandas` + `openpyxl`
- 日志：Python 内置 `logging` 模块

## 🚀 环境准备
### 1. 安装依赖
在项目根目录打开终端，执行：
```bash
pip install requests lxml pandas openpyxl
```

### 2. 配置登录Cookie（解决403必看）
1. 浏览器登录豆瓣账号，访问 [豆瓣Top250](https://movie.douban.com/top250)
2. 按 `F12` → Network → 复制请求头中的 `Cookie`
3. 打开 `config.py`，将复制的Cookie粘贴到配置中

## 🔧 使用步骤
1. **配置完成**后，在项目根目录执行：
```bash
python main.py
```
2. 程序自动执行：
   - 初始化数据库
   - 逐页爬取数据
   - 解析并存储数据
   - 自动导出Excel文件到 `output/` 目录
3. 查看结果：
   - 数据库：`douban_movies.db`
   - 日志文件：`logs/crawler.log`
   - 导出文件：`output/douban_top250.xlsx`

## 📄 核心文件说明
| 文件 | 作用 |
|------|------|
| `config.py` | 全局配置：日志、请求头、Cookie、数据库路径 |
| `main.py` | 主程序：调度请求→解析→存储→翻页全流程 |
| `request_handler.py` | 发送网络请求，解决403反爬 |
| `parser.py` | XPath解析HTML，提取电影数据 |
| `mysql_handler.py` | 数据库建表、数据插入、连接管理 |
| `export_excel.py` | 数据导出为Excel/CSV |

## ❓ 常见问题
### 1. 403 Forbidden 错误
- 解决方案：在 `config.py` 中配置**登录后的Cookie**

### 2. 数据库列不存在
- 解决方案：删除旧的 `douban_movies.db`，重新运行程序

### 3. 程序报错 module is not callable
- 解决方案：检查函数导入/调用，避免将模块当作函数使用

### 4. 列表索引越界
- 解决方案：已做空值安全处理，XPath提取无数据时自动赋值默认值

## ⚠️ 免责声明
1. 本项目仅用于**Python 爬虫学习与技术交流**，禁止用于商业用途
2. 爬取数据请遵守豆瓣网站 `robots` 协议，合理控制爬取频率
3. 因使用本项目造成的任何法律责任，由使用者自行承担

---

## 🎯 项目亮点
- 纯新手友好，代码注释完整
- 模块化开发，易于二次开发
- 全流程异常处理，稳定性拉满
- 日志+数据库+导出三合一，学习价值极高
