import os

from scrapy.http.request import Request
import scrapy

#! scrapy crawl ticketsList -o ../resources/station.json(已获取,无需再次执行)


class stationsList(scrapy.Spider):
    name = 'stationsList'
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

    station_url = 'https://www.12306.cn/index/script/core/common/station_name_v10037.js'

    def __init__(self, name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        if os.path.exists('../resources/station.json'):
            os.remove('../resources/station.json')

    def start_requests(self):
        return [Request(
            self.station_url,
            callback=self.search_station,
            # & 获取火车站字典列表(resources/station.json)
            meta={
                'dont_redirect': True,
                'handle_httpstatus_list': [301, 302]
            },
            dont_filter=True,
            cookies=self.cookie,
            errback=self.error
        ),
        ]

    def error(self, response):
        print('fail')

    def search_station(self, response):
        # 得到的数据为：火车站名的首字母，火车站名，火车站id
        # 从12306获取的数据中，通过正则匹配过滤数据
        station_names_data = {}

        stations = response.text.split('@')[1:]
        for station in stations:
            station_info = station.split("|")
            station_names_data[station_info[1]] = station_info[2]

        return station_names_data
