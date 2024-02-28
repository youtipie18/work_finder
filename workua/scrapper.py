from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from workua.spiders import spider


def run_spider(job_title: str) -> None:
    settings = get_project_settings()
    settings.setmodule('workua.settings')

    process = CrawlerProcess(settings=settings)

    process.crawl(spider.SpiderSpider, job_title=job_title)

    process.start()
