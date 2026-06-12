import os 
from openai import OpenAI
import pymysql,time

dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(dir)

client = OpenAI(
    api_key='sk-2261bfd127d4415bbb19340245a62917',
    base_url="https://api.deepseek.com")

# MySQL配置（和你的爬虫用同一个数据库）
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Yjf15113137810",
    "database": "lj_houses_info"
}


# 3. 从MySQL读未分类的房源数据
def get_unclassified_houses():
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    sql = f"SELECT id,标题,总价,面积 FROM lj_houses LIMIT 200"
    cursor.execute(sql)
    houses = cursor.fetchall()
    conn.close()
    return houses

# 2. 批量分类函数（用你写的逻辑，适配多条数据）
def classify_batch(houses):
    """一次处理多条房源，减少API请求次数"""
    items = "\n".join([f"{i+1}. 房源：{h[1]}，总价{h[2]}万，面积{h[3]}平米" 
                      for i, h in enumerate(houses)])
    prompt = f"""
    对以下{len(houses)}套房源分别判断买家类型（刚需/改善/豪宅），按序号用逗号分隔输出：
    {items}
    示例输出：刚需,改善,豪宅
    """
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50,
            stream=False
        )
        result = response.choices[0].message.content.strip()
        return result.split(",")
    except Exception as e:
        print(f"批量调用失败: {e}")
        return ["未知"] * len(houses)


# 5. 主流程
if __name__ == "__main__":
    batch_size = 5  # 一次处理5条，减少API请求次数
    houses = get_unclassified_houses()
    print(f"找到{len(houses)}条未分类房源")
    
    for i in range(0, len(houses), batch_size):
        batch = houses[i:i+batch_size]
        categories = classify_batch(batch)
        for house, category in zip(batch, categories):
            print(f"房源{house[0]} 分类为: {category}")
        time.sleep(1)  # 控制请求频率