# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SimplonFormationItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    formacodes_name = scrapy.Field()
    formacodes_code = scrapy.Field()
    url = scrapy.Field()
    date_limite_candidature = scrapy.Field()
    alternance = scrapy.Field()
    session_name = scrapy.Field()
    date_debut = scrapy.Field()
    duree = scrapy.Field()
    niveau = scrapy.Field()
    location = scrapy.Field()