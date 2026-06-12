# 链家二手房数据采集与可视化分析项目
## 项目简介
本项目基于 Python 实现**链家二手房数据爬虫采集、数据清洗、统计分析、可视化绘图**，并使用 **Streamlit** 搭建静态图表展示看板，支持本地运行 + 云端 `share.streamlit.io` 一键部署，无需交互筛选，仅做成品图表静态展示，适合课程作业/个人项目作品集。

## 技术栈
- 编程语言：Python
- 数据处理：`pandas` / `numpy` /`python re 模块(正则表达式,精准捕获)`
- 可视化绘图：`matplotlib`
- Excel 读写：`openpyxl`
- 网页看板部署：`streamlit`

## 项目目录结构
```
链家二手房数据采集项目/
├── analysis/                # 分析 & Streamlit 模块
│   ├── __init__.py          # Python包标识（部署必备）
│   ├── analysis.py          # 二手房数据分析逻辑
│   ├── charts.py            # 生成各类静态图表
│   └── app.py               # Streamlit 入口启动文件
├── config.py                # 全局配置、全局数据df定义
├── result.xlsx              # 爬取清洗后的二手房数据源
├── *.png                    # 预生成好的静态分析图表
├── requirements.txt         # 项目依赖库
└── README.md                # 项目说明文档
```

## 环境依赖
项目所有依赖已写入 `requirements.txt`，包含：
```txt
streamlit
pandas
matplotlib
openpyxl
numpy
```

## 本地运行教程
### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 本地启动 Streamlit 看板
```bash
streamlit run analysis/app.py
```
运行后自动弹出网页，展示所有已生成的静态分析图表 + 数据统计信息。

## 云端部署（share.streamlit.io）
1. 将项目完整上传至 GitHub 仓库
2. 进入 [share.streamlit.io](https://share.streamlit.io/) 关联仓库
3. 配置部署参数：
   - 选择分支：`master`
   - 入口文件路径：`链家二手房数据采集项目/analysis/app.py`
4. 自动读取根目录 `requirements.txt` 安装依赖，一键部署完成

## 项目功能亮点
1. 已提前用 Matplotlib 生成**房价柱状图、区域占比饼图、面积分布图**等静态图表
2. Streamlit 只做**静态图片展示**，无需重复绘图、无需侧边栏筛选，轻量化不报错
3. 统一配置全局路径，**本地 / 云端部署导入模块均正常**，找不到包、路径报错已全部适配
4. 封装 `config.py` 全局数据，各模块可直接导入使用
5. 依赖文件精简齐全，云端部署无需额外加装库

## 注意事项
1. 子文件夹 `analysis` 内必须保留空文件 `__init__.py`，否则云端无法识别模块导入
2. 所有图表为**预生成静态图片**，部署后不会重新计算绘图，加载速度快
3. 不要删除 `result.xlsx` 数据源文件，否则 Streamlit 读取数据会报错
4. 若部署报错，优先检查 `requirements.txt` 文件名是否拼写正确、是否放在项目根目录
