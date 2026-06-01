# 数据清洗工具函数 - 链家二手房专用
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta

# ------------------- 1. 总价清洗：150万 → 1500000 -------------------
def clean_total_price(price_str):
    """
    清洗总价字段，返回单位为元的整数
    示例："150" → 1500000，"235.5" → 2355000
    """
    if not price_str:  # 空值处理
        return 0
    # 去掉所有非数字、非小数点的字符
    cleaned = re.sub(r'[^\d.]', '', str(price_str))
    if not cleaned:  # 清洗后为空，返回0
        return 0
    try:
        # 转成浮点数，乘以10000（万转元），再转整数
        return int(float(cleaned) * 10000)
    except:
        return 0

# ------------------- 2. 面积清洗：89平米 → 89 -------------------
def clean_area(area_str):
    """
    清洗面积字段，返回浮点数（单位：㎡）
    示例："89平米" → 89.0，"120.5㎡" → 120.5
    """
    if not area_str:
        return 0.0
    # 去掉所有非数字、非小数点的字符
    cleaned = re.sub(r'[^\d.]', '', str(area_str))
    if not cleaned:
        return 0.0
    try:
        return float(cleaned)
    except:
        return 0.0


# ------------------- 3. 单价清洗：11,194元/平 → 11194 -------------------
def clean_unit_price(price_str):
    """
    清洗单价字段，返回单位为元/㎡的整数
    示例："11,194元/平" → 11194，"35000元/㎡" → 35000
    """
    if not price_str:
        return 0
    # 先去掉千分位逗号
    price_str = str(price_str).replace(",", "")
    # 去掉所有非数字字符
    cleaned = re.sub(r'[^\d]', '', price_str)
    if not cleaned:
        return 0
    try:
        return int(cleaned)
    except:
        return 0

# ------------------- 4.楼层清洗:高楼层(共20层) -> 20  -------------------
def clean_floor(floor_str):
    if not floor_str:
        return 0
    floor_str = str(floor_str)
    # 核心正则:匹配到任意位置的“数字+层”，提取数字
    match = re.search(r'(\d+)层',floor_str)

    if match:
        return int(match.group(1))
    else:
        return 0 

# ------------------- 5.关注人数：1人关注 -> 1  -------------------
def clean_star_num(star_num_str):
    if not star_num_str:
        return 0
    cleaned = re.sub(r'[^\d]','',str(star_num_str))
    if not cleaned:
        return 0 
    try: 
        return int(cleaned)
    except:
        return 0
    
# ------------------- 6.发布时间：一年前发布 -> 20xx.xx  -------------------
def clean_publish_time(publish_time_str):
    """
    链家发布时间清洗：适配所有格式，避免返回NULL
    匹配失败/空值默认返回当前日期，方便后续数据分析
    """
    # 1. 空值/None处理（兜底，避免返回NULL）
    if not publish_time_str or publish_time_str.strip() == '':
        return datetime.now().date()
    
    publish_time_str = publish_time_str.strip()
    
    # 2. 正则匹配：覆盖数字+所有中文数字，带/不带"以"
    pattern = r'(\d+|一|二|三|四|五|六|七|八|九|十)个?(月|天|年)(前|以前)'
    match = re.search(pattern, publish_time_str)
    
    # 3. 提取数量和单位，中文数字转阿拉伯数字
    num_str = match.group(1)
    unit = match.group(2)
    
    num_map = {"一":1, "二":2, "三":3, "四":4, "五":5, "六":6, "七":7, "八":8, "九":9, "十":10}
    num = num_map.get(num_str, None)
    if num is None:
        num = int(num_str)
    
    # 4. 计算目标日期
    today = datetime.now().date()
    if unit == "年":
        return today - relativedelta(years=num)
    elif unit == "月":
        return today - relativedelta(months=num)
    elif unit == "天":
        return today - relativedelta(days=num)
    else:
        return today