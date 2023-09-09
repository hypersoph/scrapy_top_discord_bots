# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose
from scrapy.selector import Selector
import html2text

def get_tags(tag_str):
    tags = tag_str.split(' ')
    return tags

def get_creator(html):
    selector_obj = Selector(text=html)
    username = selector_obj.xpath("normalize-space(.//text())").get()
    discrim = selector_obj.xpath("normalize-space(.//i/text())").get().replace(' ','')

    return username + discrim

def get_long_desc(html):
    text = html2text.html2text(html)
    return text

def remove_whitespace(input_str):
    return input_str.strip()

class TopGgItem(scrapy.Item):
    bot_name = scrapy.Field(
        output_processor=TakeFirst()
    )
    votes = scrapy.Field(
        output_processor=TakeFirst()
    )
    num_servers = scrapy.Field(
        output_processor=TakeFirst()
    )
    short_description = scrapy.Field(
        output_processor=TakeFirst()
    )
    bot_creator = scrapy.Field(
        input_processor = MapCompose(get_creator)
    )
    bot_prefix = scrapy.Field(
        input_processor=MapCompose(remove_whitespace),
        output_processor=TakeFirst()
    )
    tags = scrapy.Field(
        input_processor = MapCompose(get_tags)
    )
    img_url = scrapy.Field(
        output_processor=TakeFirst()
    )
    bot_website = scrapy.Field(
        output_processor=TakeFirst()
    )
    support_server = scrapy.Field(
        output_processor=TakeFirst()
    )
    invite_link = scrapy.Field(
        output_processor=TakeFirst()
    )
    long_description = scrapy.Field(
        input_processor = MapCompose(get_long_desc),
        output_processor = TakeFirst()
    )

