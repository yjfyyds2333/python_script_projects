import requests
import os,json
from dotenv import load_dotenv
from datetime import datetime,date
from pymongo import MongoClient
import pandas as pd
import json,re
import logging

dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(dir)
os.makedirs('images',exist_ok=True)
os.makedirs('videos',exist_ok=True)

log_filename = f"run_{date.today()}.log"
logging.basicConfig(
    level=logging.INFO,
    encoding="utf-8",
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(filename=log_filename,encoding='utf-8'),
        logging.StreamHandler()
    ]
)

load_dotenv() # 加载.env文件


headers = {
    'Authorization': os.getenv("PEXELS_KEY"),
}

class Database:
    def __init__(self):
        # 无参构造，先空创建实例
        self.client = None
        self.db = None
        self.collection = None
    
    # 自定义初始化方法
    def connect(self, db_name, collection_name):
        self.client = MongoClient()
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        logging.info("数据库建立成功")

d1 = Database()
d1.connect("Pexels", "Pictures")

d2 = Database()
d2.connect("Pexels", "Videos")



def photos_download_pexels(query,per_page,large,target_page):

    params = {
        'query': 'Sky',
        'per_page': '15',
        'page':'1'
    }

    img_datas = []
    params['query'] = query
    params['per_page'] = per_page
    page = 1
    xh = 1

    if os.path.exists("photos_process.json"):
        with open("photos_process.json","r") as f:
            data = json.load(f)
            page = int(data["page"]) - 1
            logging.info(f"上次程序从第{page}页就断开连接了，现在从当前页开始继续采集")
    else:
        pass
    
    while page <= target_page: 
        params['page'] = page

        response_photo = requests.get('https://api.pexels.com/v1/search', params=params, headers=headers)

        data = response_photo.json()

        total_results = data["total_results"]
        next_page = data["next_page"]
        match = re.search(r'page=(\d+)',next_page)
        process_data_page = match.group(1)

        process_data = {'next_page': next_page,'page':process_data_page}


        # 每调一次 json.dump()，文件里就是最新的内容，之前的自动没了。w 模式的特点就是：打开文件时先清空，再写入。
        with open("photos_process.json","w") as f:
            json.dump(process_data,f)

        if not next_page: break
        if len(img_datas) >= total_results: break

        for photo in data["photos"]:

            img_id = photo["id"]
            img_type = "photo"
            img_alt = photo["alt"]
            img_photographer = photo["photographer"]
            img_width = photo["width"]
            img_height = photo["height"]
            img_avg_color = photo["avg_color"]
            img_url = photo["src"][f"{large}"]
            img_date = datetime.now()

            data_list = {
                'id':img_id,
                'img_query':query,
                'type':img_type,
                'alt':img_alt,
                'photographer':img_photographer,
                'width':img_width,
                'height':img_height,
                'avg_color':img_avg_color,
                'url':img_url,
                'date':img_date
            }

            img_datas.append(data_list)

            d1.collection.update_one(
                {'id':img_id},
                    {
                    '$set':{
                        'img_id':img_id,
                        'img_query':query,
                        'img_type':img_type,
                        'img_alt':img_alt,
                        'img_photographer':img_photographer,
                        'img_width':img_width,
                        'img_height':img_height,
                        'img_avg_color':img_avg_color,
                        'img_url':img_url,
                        'last_update':img_date
                        }
                    },
                upsert=True
            )

            img_resp = requests.get(img_url)
            with open(f'images/{query}_{xh}_{img_id}.jpeg','wb') as f:
                f.write(img_resp.content)

            xh += 1

        logging.info(f'【图片采集】：第{page}页采集完成')
        page += 1
    
    if os.path.exists("photos_process.json"):
        os.remove("photos_process.json")

    return img_datas,query

def videos_download_pexels(query,per_page,hd_type,target_page):

    params = {
        'query': 'nature',
        'per_page': '1',
        'page':'1'
    }

    page = 1
    xh = 1
    videos_data = []
    params['query'] = query
    params['per_page'] = per_page

    if os.path.exists("videos_process.json"):
        with open("videos_process.json","r") as f:
            data = json.load(f)
            page = int(data["page"]) - 1
            logging.info(f"上次程序从第{page}页就断开连接了，现在从当前页开始继续采集")
    else:
        pass

    while page <= target_page:

        params['page'] = page
        response_video = requests.get('https://api.pexels.com/v1/videos/search', params=params, headers=headers)

        data = response_video.json()

        next_page = data['next_page']
        total_results = data["total_results"]

        match = re.search(r'page=(\d+)',next_page)
        process_data_page = match.group(1)

        process_data = {'next_page': next_page,'page':process_data_page}

        # 每调一次 json.dump()，文件里就是最新的内容，之前的自动没了。w 模式的特点就是：打开文件时先清空，再写入。
        with open("videos_process.json","w") as f:
            json.dump(process_data,f)


        if not next_page:
            logging.info("所有视频结果都被采集完")
            break
        if len(videos_data) >= total_results:
            logging.info("所有视频结果都被采集完")
            break

        videos_list = data.get("videos", [])

        if not isinstance(videos_list, list):
            logging.info("videos不是列表，跳过")
            return

        for videos in videos_list:
        
            video_url_list = videos["video_files"]
            sorted_videos = sorted(video_url_list,key=lambda x:(x["width"],x["height"]))

            # 5个清晰度分别取出
            min = sorted_videos[0]   # 最低清
            sd1 = sorted_videos[1]   # 低标清
            sd2 = sorted_videos[2]   # 中标清
            hd720 = sorted_videos[3] # 720P高清
            hd1080 = sorted_videos[4]# 1080P超清

            level_map = {
                "min": min,
                "sd1": sd1,
                "sd2": sd2,
                "hd720": hd720,
                "hd1080": hd1080
            }

            if hd_type in level_map:
                target_video = level_map[hd_type]
            else:
                logging.info("参数填入错误")
                # 循环内用break，非循环用return/exit终止

            video_id = videos.get("id")
            if video_id is None:
                continue     

            video_type = "video"
            video_during_time = f'{videos["duration"] // 60}分{videos["duration"] % 60}秒'
            video_width = target_video['width']
            video_height = target_video['height']
            video_photographer = videos["user"]["name"]
            video_url = target_video['link']
            video_getdate = datetime.now()
            
            data_list = {
                'video_id':video_id,
                'video_query':query,
                'video_type':video_type,
                'video_during_time':video_during_time,
                'video_width':video_width,
                'video_height':video_height,
                'video_photographer':video_photographer,
                'video_url':video_url,
                'video_date':video_getdate
            }

            videos_data.append(data_list)

            d2.collection.update_one(
                {'id':video_id},
                    {
                    '$set':{
                        'video_id':video_id,
                        'video_query':query,
                        'video_type':video_type,
                        'video_during_time':video_during_time,
                        'video_width':video_width,
                        'video_height':video_height,
                        'video_photographer':video_photographer,
                        'video_url':video_url,
                        'last_update':video_getdate
                        }
                    },
                upsert=True
            )

            video_resp = requests.get(video_url,stream=True)
            with open(f'videos/{query}_{xh}_{video_id}.mp4','wb') as f:
                for chunk in video_resp.iter_content(chunk_size=8192):
                    f.write(chunk)
                    
            xh += 1  

        logging.info(f"【视频采集】:第{page}页采集完成!")
        page += 1  

    if os.path.exists("videos_process.json"):
        os.remove("videos_process.json")

    return videos_data,query

def save_picture(data,query):
    df = pd.DataFrame(data)
    df.to_excel(f"Picture_{query}_excel_{datetime.now().strftime("%Y-%m-%d")}.xlsx",index=False)

def save_video(data,query):
    df = pd.DataFrame(data)
    df.to_excel(f"Videos_{query}_excel_{datetime.now().strftime("%Y-%m-%d")}.xlsx",index=False)

if __name__ == "__main__":
    # 图片搜索存储
    # pic_data,query = photos_download_pexels("happy",15,"large",3)
    # save_picture(pic_data,query)

    # 视频搜索存储
    videos_data,query = videos_download_pexels("game",6,"min",3)
    save_video(videos_data,query)
