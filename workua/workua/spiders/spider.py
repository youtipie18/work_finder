from typing import Any

import scrapy
from bs4 import BeautifulSoup
from ..items import WorkuaItem


class SpiderSpider(scrapy.Spider):
    name = "spider"
    job_title = "python"
    allowed_domains = ["www.work.ua"]
    start_urls = [f"https://www.work.ua/jobs-{job_title}/?experience=1&student=1&anyword=1&notitle=1"]

    def __init__(self, job_title, **kwargs: Any):
        super().__init__(**kwargs)
        self.job_title = job_title

    def parse(self, response):
        jobs = response.css("#pjax-jobs-list .job-link")

        for job in jobs:
            url = response.urljoin(job.css("h2 a::attr(href)").get())
            yield scrapy.Request(url=url, callback=self.parse_job)

        if response.css(".pagination .add-left-default a"):
            next_page = response.urljoin(response.css(".pagination .add-left-default a::attr(href)").get())
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_job(self, response):
        item = WorkuaItem()
        item["title"] = response.css("#h1-name::text").get()
        item["requirements"] = BeautifulSoup(
            response.css('[title="Умови й вимоги"]').xpath("parent::*").get()).get_text().strip()
        item["description"] = BeautifulSoup(
            response.css("#job-description").get()).get_text().strip()
        item["url"] = response.request.url
        yield item
