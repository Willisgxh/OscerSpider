# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class OscerspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Diseases = scrapy.Field()
    Symptoms = scrapy.Field()
    Causes = scrapy.Field()
    Diagnosis = scrapy.Field()
    Treatment = scrapy.Field()