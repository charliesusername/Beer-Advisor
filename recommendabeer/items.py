# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RecommendabeerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    # Beer Stats
    beer_name = scrapy.Field()
    brewery = scrapy.Field()
    BAscore = scrapy.Field()
    abv = scrapy.Field()
    num_reviews = scrapy.Field()
    ranking = scrapy.Field()
    beer_img = scrapy.Field()
    desc = scrapy.Field()
    family_style = scrapy.Field()
    style_desc = scrapy.Field()
  

    # Review Stats
    #user = scrapy.Field()
    #posted = scrapy.Field()
    #rating = scrapy.Field()

    #review = scrapy.Field()
    #style = scrapy.Field()

