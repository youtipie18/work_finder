# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sys

sys.path.append("..")
from itemadapter import ItemAdapter
import json
from models import Job
from db import Session
from sqlalchemy.exc import IntegrityError

session = Session()


class WorkuaPipeline:
    # def open_spider(self, spider):
    # self.data = []

    # def close_spider(self, spider):
    # with open("data.json", "w", encoding="utf-8") as file:
    #     file.write(json.dumps(self.data, indent=4))

    def process_item(self, item, spider):
        # self.data.append(dict(item))
        urls = [url[0] for url in session.query(Job.url).all()]
        if item["url"] not in urls:
            session.add(Job(**dict(item)))
            session.commit()
        return item
