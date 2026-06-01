# 获取当前文件的绝对路径 → 定位到analysis文件夹 → 再上一级就是项目根目录
import os
import sys
import pandas as pd

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 把根目录插入到搜索路径最前面（优先级最高，避免冲突）
sys.path.insert(0, root_dir)

import streamlit as st
from analysis.charts import avg_unix_price,avg_total_price
from config import CHART_BASE_DIR,df
from analysis.analysis import total_data_count


@st.cache_data
def change_to_st():
    # 标题+数据概览模块
    st.title("东莞市二手房数据分析仪表盘")
    st.subheader("数据概览")
        
    col1,col2 = st.columns(2)
    with col1:
        st.metric(label="房价总价均价",value=f'{avg_total_price}')
    with col2:
        st.metric(label='每平方米房价均价',value=f'{avg_unix_price}')
        
    st.success(f'一共有{total_data_count}条数据')

    # 将已经生成的表格图片上传
    st.subheader("1.东莞链家二手房各个区域的房价对比柱状图")
    st.image(os.path.join(CHART_BASE_DIR,"东莞链家二手房各个区域的房价对比柱状图.png"))

    st.subheader("2.面积分布折线图")
    st.image(os.path.join(CHART_BASE_DIR,"面积分布折线图.png"))

    st.subheader("3.热门区域饼状图")
    st.image(os.path.join(CHART_BASE_DIR,"热门区域饼状图.png"))

    st.subheader("数据预览(前20条)")
    st.dataframe(df.head(20),use_container_width=True)

change_to_st()
