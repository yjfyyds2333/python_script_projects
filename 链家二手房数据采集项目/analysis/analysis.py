import pandas as pd
from config import logger,df

total_data_count = df['发布时间'].count()

def avg_price(EXCEL_FILE):
    if not EXCEL_FILE:
        logger.error("分析数据时未发现excel表格，无法读取！")
    avg_price = df["单价"].mean().round(0)
    avg_total_price = df["总价"].mean().round(0)
    return avg_price,avg_total_price

def area_price(EXCEL_FILE):
    if not EXCEL_FILE:
        logger.error("分析数据时未发现excel表格，无法读取！")
    try:
        area_price = df.groupby("区域")["单价"].mean().sort_values(ascending=False)
    except Exception as e:
        logger.error(f'出现错误:{e}')
    return area_price

def area_fenbu(EXCEL_FILE):
    if not EXCEL_FILE:
        logger.error("分析数据时未发现excel表格，无法读取！")
    try:  
        df["面积段"] = pd.cut(df["面积"],bins=[0,50,80,100,120,150,200],labels=["0-50","50-80","80-100","100-120","120-150","150+"])
        area_distribution = df["面积段"].value_counts().sort_index()
    except Exception as e:
        logger.error(f'出现错误:{e}')
    return area_distribution

def remen_area(EXCEL_FILE):
    if not EXCEL_FILE:
        logger.error("分析数据时未发现excel表格，无法读取！")
    try:
        remen_area_num = df["区域"].value_counts()
    except Exception as e:
        logger.error(f'出现错误:{e}')
    return remen_area_num

