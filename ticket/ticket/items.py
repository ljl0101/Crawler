# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ticketItem(scrapy.Item):
    date = scrapy.Field()   # 日期
    start = scrapy.Field()  # 出发地
    arrive = scrapy.Field() # 目的地

    order = scrapy.Field()       # 车次
    start_time = scrapy.Field()  # 出发时间
    arrive_time = scrapy.Field() # 到达时间
    pass_time = scrapy.Field()   # 历经时间

    train_no = scrapy.Field()   # 车次编号
    from_station_no = scrapy.Field()
    to_station_no = scrapy.Field()
    seat_types = scrapy.Field() 