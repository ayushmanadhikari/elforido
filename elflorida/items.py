# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field



class ElfloridaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    categoryName = Field()
    subcategoryName = Field()
    brand =  Field()
    upc = Field()
    Item=  Field()
    URLSKU=  Field()
    Image=  Field()
    Price=  Field()
    SalePrice=  Field()
    SaleFlag=  Field()
    stock=  Field()
    productDescription=  Field()