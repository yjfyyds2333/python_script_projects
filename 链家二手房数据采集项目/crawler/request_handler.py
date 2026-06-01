import time,random
from playwright.sync_api import sync_playwright
from config import LJ_BASE_URL,HEADERS,logger,TIMEOUT,playwright,browser,context,page

# 函数1:初始化浏览器(只运行1次!)
def init_browser():
    global playwright,browser,context,page
    # 启动指挥官
    playwright = sync_playwright().start()
    # 启动浏览器: headless=False显示窗口(方便你验证)
    browser = playwright.chromium.launch(
        headless=False,
        slow_mo=1000, # 放慢操作速度到1秒,更像真人的反应速度
        args=[
            "--disable-blink-features=AutomationControlled", # 隐藏自动化工具的特征
            "--start-maximized" # 最大化窗口,和真人操作一致
        ]
    )
    
    # 创建独立会话(Cookie永久保存,解决你第二页失效的问题)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
        viewport={"width":1920,"height":1080}, # 模拟常见的电脑分辨率
        geolocation={"latitude":22.93,"longitude":113.92}, # 模拟东莞的位置
        permissions=['geolocation'], # 允许位置权限,更符合真实用户行为
        locale="zh-CN" # 语言设置为中文,和真实用户一致
    )

    # 打开标签页
    page = context.new_page()
    logger.info("浏览器启动成功!")



# 函数2:爬取网页
def fetch_page(url):
    global page
    try:
        logger.info(f'正在访问:{url}')
        # 1.打开网页
        page.goto(url,timeout=60000) # 超时设为60s,避免页面加载慢被判定为异常 
        # 2.等待页面加载完成
        page.wait_for_load_state("networkidle",timeout=30000)
        # 3.延时:模拟真人看网页,不触发风控
        time.sleep(random.uniform(2.5,3.5))
        
        # 模拟真人滚动页面,不是直接跳转
        page.mouse.wheel(0,300)
        time.sleep(random.uniform(1,3))
        page.mouse.wheel(0,300)
        time.sleep(random.uniform(1.5,3.5))

        # 处理人机验证(你只需要点1次)
        # 如果页面出现验证,程序暂停,等待你手动点完
        if "CAPTCHA" in page.title():
            logger.warning("⚠ 请手动完成人机验证,完成后程序自动继续!")
            # 等待验证完成,最多等2分钟
            page.wait_for_selector("text=二手房",timeout=120000)
            logger.info('验证通过')
        elif "登录" in page.title():
            logger.warning("⚠ 请手动完成人机验证,完成后程序自动继续!")
            # 等待完成登录，最多等2分钟
            page.wait_for_selector("text=二手房",timeout=120000)
            logger.info("登录成功！")

        # 等待
        page.wait_for_selector("text=二手房",timeout=120000)

        # 4.返回网页源代码(给解析用)
        html = page.content()
        return html

    except Exception as e:
        logger.error(f'访问失败:{e}')
        return None
    

# 函数3:关闭浏览器(程序结束用)
def close_browser():
    context.close()
    browser.close()
    playwright.stop()
    logger.info("浏览器已关闭!")