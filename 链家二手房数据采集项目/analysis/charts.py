import matplotlib.pyplot as plt
from analysis.analysis import avg_price,area_price,area_fenbu,remen_area
from config import EXCEL_FILE,CHART_BASE_DIR
import os 

plt.rcParams["font.sans-serif"] =["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

avg_unix_price,avg_total_price = avg_price(EXCEL_FILE)

# 1.柱状图:朝向平均房价对比
def zhu_chart():
    area_avg_price = area_price(EXCEL_FILE)
    plt.figure(figsize=(10,6))
    plt.bar(
        x = area_avg_price.index.astype(str),
        height = area_avg_price.values,
        color = "steelblue"
    )

    plt.title("东莞链家二手房各个朝向的房价对比",fontsize=14)
    plt.xlabel("朝向",fontsize=12)
    plt.ylabel("平均房价",fontsize=12)
    plt.tight_layout()
    plt.xticks(rotation=45)

    plt.savefig(os.path.join(CHART_BASE_DIR,"东莞链家二手房各个朝向的房价对比柱状图.png"),dpi=300)

def zhe_chart():
    area_fenbu_dy = area_fenbu(EXCEL_FILE)
    plt.figure(figsize=(10,6))
    plt.plot(area_fenbu_dy.index, area_fenbu_dy.values,marker="o", color="#ff7f0e", linewidth=2)

    # 美化
    plt.title("东莞链家二手房房源面积段分布", fontsize=14)
    plt.xlabel("面积段（㎡）", fontsize=12)
    plt.ylabel("房源数量", fontsize=12)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(CHART_BASE_DIR,"面积分布折线图.png"),dpi=300)

def bin_chart():
    region_counts= remen_area(EXCEL_FILE)
    # 数据准备（取TOP10热门朝向，避免饼图过乱）
    top10_regions = region_counts.head(10)
    labels = top10_regions.index
    sizes = top10_regions.values

    plt.figure(figsize=(8,8))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90, colors=plt.cm.Paired.colors)

    # 美化
    plt.title("热门朝向二手房房源占比（TOP10）", fontsize=14)
    plt.axis("equal")  # 保持饼图为圆形
    plt.tight_layout()
    plt.savefig(os.path.join(CHART_BASE_DIR,"热门朝向饼状图.png"),dpi=300)
