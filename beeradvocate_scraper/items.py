# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BeerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    # Beer Stats
    beer_id = scrapy.Field()
    beer_name = scrapy.Field()
    brewery = scrapy.Field()
    BAscore = scrapy.Field()
    abv = scrapy.Field()
    num_reviews = scrapy.Field()
    ranking = scrapy.Field()
    beer_img = scrapy.Field()
    desc = scrapy.Field()
    beer_style = scrapy.Field()
    #style_desc = scrapy.Field()
  

    # Review Stats
    #user = scrapy.Field()
    #posted = scrapy.Field()
    #rating = scrapy.Field()

    #review = scrapy.Field()
    #style = scrapy.Field()


class ReviewItem(scrapy.Item):
    
    review_id = scrapy.Field()
    beer_id = scrapy.Field()
    username = scrapy.Field()
    posted = scrapy.Field()
    text = scrapy.Field()
    ratings = scrapy.Field()
    score = scrapy.Field()