# extensions.py
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from scrapy import signals

class SpiderReportExtension:
    """Scrapy扩展：爬虫结束后自动发送采集报告邮件"""

    def __init__(self, crawler):
        # 从settings.py读取邮箱配置
        self.sender = crawler.settings.get("REPORT_SENDER")
        self.password = crawler.settings.get("REPORT_PASSWORD")
        self.receiver = crawler.settings.get("REPORT_RECEIVER")
        self.smtp_server = crawler.settings.get("REPORT_SMTP_SERVER", "smtp.qq.com")
        self.smtp_port = crawler.settings.get("REPORT_SMTP_PORT", 465)

    @classmethod
    def from_crawler(cls, crawler):
        # 注册扩展：绑定spider_closed信号
        ext = cls(crawler) # 创建实例，并传入crawler参数
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        return ext

    def spider_closed(self, spider):
        """爬虫关闭时自动触发（核心逻辑）"""
        # 1. 从Scrapy内置stats获取采集数据（不用自己查数据库）
        stats = spider.crawler.stats.get_stats()
        item_count = stats.get("item_scraped_count", 0)  # 成功采集的条目数
        finish_reason = stats.get("finish_reason", "unknown")  # 爬虫结束原因

        # 2. 构建邮件内容
        subject = f"【{spider.name}】采集完成报告"
        body = f"""
        爬虫名称：{spider.name}
        采集时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        采集状态：{'✅ 正常结束' if finish_reason == 'finished' else '❌ 异常终止'}
        成功采集条数：{item_count} 条
        结束原因：{finish_reason}
        """

        # 3. 发送邮件（带异常处理，失败不影响爬虫）
        try:
            self.send_email(subject, body)
            spider.logger.info("📧 采集报告邮件发送成功！")
        except Exception as e:
            spider.logger.error(f"❌ 邮件发送失败：{str(e)}")

    def send_email(self, subject, body):
        """发送邮件的核心函数"""
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = self.sender
        msg["To"] = self.receiver

        # 添加邮件正文
        msg.attach(MIMEText(body, "plain", "utf-8"))

        # 连接SMTP服务器并发送
        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
            server.login(self.sender, self.password)
            server.sendmail(self.sender, self.receiver, msg.as_string())