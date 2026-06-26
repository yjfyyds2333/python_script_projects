---
AIGC:
    Label: "1"
    ContentProducer: 001191110102MACQD9K64018705
    ProduceID: 907551919054137_0/project_7650382242090320143-files/学习路线/xueqiu_readme.md
    ReservedCode1: ""
    ContentPropagator: 001191110102MACQD9K64028705
    PropagateID: 907551919054137#1782442071179
    ReservedCode2: ""
---
# 项目6：雪球网股票行情监控系统

## 项目简介
采集雪球网深沪A股行情数据，实现DrissionPage自动过WAF获取cookie + requests采集API数据 + MongoDB增量存储。

## 技术栈
- **Cookie获取**：DrissionPage（自动过阿里云WAF JS挑战）
- **数据采集**：requests
- **数据存储**：MongoDB（增量采集+历史记录）

## 功能清单

| 功能 | 说明 | 状态 |
|------|------|------|
| F1 Cookie自动获取 | DrissionPage打开雪球→等待WAF挑战完成→提取cookie | ✅ |
| F2 WAF挑战绕过 | 阿里云acw_sc__v2加密，通过浏览器自动化绕过 | ✅ |
| F3 股票行情采集 | 深沪A股全量采集（代码/名称/涨跌幅/成交量/市值等） | ✅ |
| F4 MongoDB存储 | update_one+upsert去重，$push记录历史价格走势 | ✅ |
| F5 增量采集 | 每次运行只更新变化数据，历史数据追加到period_history | ✅ |

## 核心知识点

### 1. 雪球WAF反爬机制
雪球使用阿里云WAF，首次请求返回混淆JS（控制流扁平化+多层编码），浏览器执行JS计算acw_sc__v2后设置cookie，第二次请求才能通过。混淆程度极高，纯Python逆向不现实。

### 2. DrissionPage过WAF方案
浏览器自动化天然能执行JS，所以DrissionPage直接就能过WAF。核心逻辑：
```python
page = ChromiumPage(9222)
page.get("https://xueqiu.com")
time.sleep(3)  # 等WAF挑战自动完成
cookies = {c["name"]: c["value"] for c in page.cookies()}
```

### 3. SSR页面 vs JSON API
- 首页/行情页是服务端渲染（SSR），数据嵌在`<script id="initStore">`标签里
- 翻页/交互通过JSON API（`/v5/stock/screener/quote/list.json`）
- 两种方式都需要cookie，API方式更适合批量采集

### 4. Cookie认证链路
```
浏览器请求 / → WAF返回JS挑战 → 浏览器执行JS设置acw_sc__v2 → 再次请求获得xq_a_token
                                                                        ↓
                                                    后续API请求带上xq_a_token → 返回数据
```
- xq_a_token有效期约7天
- 每次API请求必须带Referer头

### 5. MongoDB增量存储策略
```python
collection.update_one(
    {"stock_code": stock_code},    # 按股票代码去重
    {"$set": {最新数据},            # 覆盖更新当前状态
     "$push": {"period_history": {历史快照}}},  # 追加历史记录
    upsert=True                    # 不存在则插入
)
```

## 项目结构
```
xueqiu_stock/
├── 雪花网深沪股票行情监控.py   # 主脚本
└── requirements.txt
```

## 运行方式
1. 确保Chrome浏览器已打开且监听9222端口
2. 运行脚本：`python 雪花网深沪股票行情监控.py`
3. 数据存入MongoDB的stock数据库

## 注意事项
- 单IP每分钟请求不超过20次，建议加延时
- cookie有效期约7天，过期需重新获取
- 采集168页约5000只股票，全量采集注意频率控制

---

> 本内容由 Coze AI 生成，请遵循相关法律法规及《人工智能生成合成内容标识办法》使用与传播。
