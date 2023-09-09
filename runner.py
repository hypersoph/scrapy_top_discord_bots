import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from top_gg.spiders.top_bots import TopBotsSpider

process = CrawlerProcess(settings = get_project_settings())
process.crawl(TopBotsSpider)
process.start()