import os
from ..views import select
import re
from ..items import ticketItem
from .. import settings
from scrapy.http.request import Request

import scrapy

import sys
from scrapy.http.request.form import FormRequest
import json

import time

sys.path.append("..")


# ! scrapy crawl ticketsList -o ../resources/tickets.json(已存在一份默认信息)

# from  ticketInfo, ticketItem, AllTicketsItem
# , AllTicketsItem, ticketItem
# https://kyfw.12306.cn/otn/leftTicket/init?
# linktypeid=dc                 default

# &fs=%E5%8C%97%E4%BA%AC,BJP    北京 出发地
# &ts=%E4%B8%8A%E6%B5%B7,SHH    上海 目的地
# &date=2021-04-20              日期
# &flag=Y,Y,Y                   学生 高铁/动车 default：Y


class ticket(scrapy.Spider):
    name = 'ticketsList'
    allowed_domains = ['www.kyfw.12306.cn']

    JSESSIONID = '7A134DDF98831A43EEE1E54415105F43'

    cookie = {
        'JSESSIONID': '7A134DDF98831A43EEE1E54415105F43',
        'tk': '7Q0g-f4mPZmlXTu0Kak5jdRHhu0wW37CM9ZLEgsdl1l0',
        'BIGipServerotn': '703595018.38945.0000',
        'BIGipServerpool_passport': '149160458.50215.0000',
        'RAIL_EXPIRATION': '1619537962659',
        'RAIL_DEVICEID': 'jiSrzl_X0nDcHgcH33Uxj6rqOZKeMUeLo-LvvXkEL2NI3Sg3CRTIWVf5WLR3B6Agcz2PFpot8k_F8XZYesRmrqhgFU6wU2SpmNXiRuX9ULJ9tqeg5WFQ7BsurDyw-GMap52GUNgC1b0VJtJacPUfjD0n0g1xmELp',
        'route': '495c805987d0f5c8c84b14f60212447d',
        '_jc_save_fromStation': '%u5317%u4EAC%2CBJP',
        '_jc_save_fromDate': '2021-04-24',
        '_jc_save_toDate': '2021-04-24',
        '_jc_save_wfdc_flag': 'dc',
        '_jc_save_toStation': '%u4E0A%u6D77%2CSHH',
        'uKey': '9f01dfaa51e7efc519ec6fa99f9c80aa0af85da3e7f70cec3aed53d10d7efac8'
    }

    # & default 今日日期 武汉至北京 (防止param出错重定向至error.html)
    param = {
        # 时间
        'leftTicketDTO.train_date': time.strftime("%Y-%m-%d", time.localtime(time.time())),
        'leftTicketDTO.from_station': 'WHN',  # 出发地
        'leftTicketDTO.to_station': 'BJP',  # 目的地
        'purpose_codes': 'ADULT'
    }

    # ^ default
    ticketsList_url = 'https://kyfw.12306.cn/otn/leftTicket/query'

    def __init__(self, name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        select_param = select.select()
        select_param.main()

        # ! 如果界面直接关闭，未点击预定，则不会传递param信息,直接使用默认的param信息
        if select_param.status == 1:
            self.param = select_param.param

        self.ticketsList_url += "?"
        # 提取param里的信息添加到ticketsList_url后面
        for key in self.param.keys():
            self.ticketsList_url += key + "=" + self.param[key] + "&"
            print(self.ticketsList_url)
        self.ticketsList_url = self.ticketsList_url[:-1]

        # & 删除ticket.json并重新爬取
        # & scrapy crawl xxx -o file 是追加写入，因此我们在init阶段删除该文件夹并重新创建
        if os.path.exists('../resources/tickets.json'):
            os.remove('../resources/tickets.json')

    def start_requests(self):
        return [Request(
            self.ticketsList_url,
            callback=self.get_info,

            meta={
                'dont_redirect': True,
                'handle_httpstatus_list': [301, 302]
            },
            dont_filter=True,
            cookies=self.cookie,
            errback=self.error
        ),
        ]

    def get_info(self, response):
        print(response)

        tickets = []

        data = response.json()['data']['result']

        # ['xcxzczc', '预订', '240000G1010Q', 'G101', 'VNP', 'AOH', 'VNP', 'AOH', '06:36', '12:40', '06:04',
        #  'Y', '12', '20210430', '3', 'P2', '01', '03', '1', '0', '', '', '', '', '', '', '', '', '', '',
        #   '有', '无', '无', '', 'O0M090', 'OM9', '0', '1', '',
        #   'O052400021M0884000009174800000', '0', '', '', '', '', '1', '#1#0', '']
        for list in data:
            ticket = ticketItem()
            info = list.split("|")
            ticket['date'] = self.param['leftTicketDTO.train_date']
            ticket['start'] = self.param['leftTicketDTO.from_station']
            ticket['arrive'] = self.param['leftTicketDTO.to_station']

            ticket['order'] = info[3]
            ticket['start_time'] = info[8]
            ticket['arrive_time'] = info[9]
            ticket['pass_time'] = info[10]

            ticket['train_no'] = info[2]
            ticket['from_station_no'] = info[16]
            ticket['to_station_no'] = info[17]
            ticket['seat_types'] = info[35]

            tickets.append(ticket)

        return tickets

    def error(self, response):
        print('fail')
