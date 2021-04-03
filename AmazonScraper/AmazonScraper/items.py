# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonscraperItem(scrapy.Item):
    # define the fields for your item here like:
    Product = scrapy.Field()
    Price = scrapy.Field()
    Rating = scrapy.Field()
    No_of_Ratings = scrapy.Field()
    ASIN = scrapy.Field()
    URL = scrapy.Field()
    ImageURL = scrapy.Field()

class AsinItem(scrapy.Item):
    Title = scrapy.Field()
    Brand = scrapy.Field()
    Rating = scrapy.Field()
    No_of_Ratings = scrapy.Field()
    Description = scrapy.Field()
    Price = scrapy.Field()
    ASIN = scrapy.Field()
    Colour = scrapy.Field()
    Weight = scrapy.Field()
    Dimensions = scrapy.Field()

class ReviewsItem(scrapy.Item):
    Reviewer = scrapy.Field()
    Rating = scrapy.Field()
    Title = scrapy.Field()
    Date = scrapy.Field()
    Verified = scrapy.Field()
    Review = scrapy.Field()
    Helpful =scrapy.Field()

class BestSellersItem(scrapy.Item):
    Category = scrapy.Field()
    Position = scrapy.Field()
    Price = scrapy.Field()
    Product = scrapy.Field()
    ImageUrl = scrapy.Field()
    URL = scrapy.Field()
    Ratings = scrapy.Field()
    No_of_Ratings = scrapy.Field()
    Parent_Cat = scrapy.Field()

class DealsItem(scrapy.Item):
    Product = scrapy.Field()
    Price = scrapy.Field()
    Pre_Price = scrapy.Field()
    Rating = scrapy.Field()
    No_of_Ratings = scrapy.Field()
    Timer = scrapy.Field()
    Claimed = scrapy.Field()
    URL = scrapy.Field()
    IMG_URL = scrapy.Field()