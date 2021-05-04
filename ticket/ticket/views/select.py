import tkinter
from tkinter import scrolledtext
import json
import datetime
import os


class select():
    status = 0

    # default
    param = {
        'leftTicketDTO.train_date': '2021-05-10',  # 时间
        'leftTicketDTO.from_station': 'BJP',  # 出发地
        'leftTicketDTO.to_station': 'TJP',  # 目的地
        'purpose_codes': 'ADULT',   # 成人票
    }

    def main(self):
        print("")

        with open('../resources/station.json', 'r', encoding='utf8') as fp:
            stations = json.load(fp)[0]

        params = tkinter.Tk()
        params.title('12306')  # 定义窗体标题
        params.geometry('500x600+0+0')

        L1 = tkinter.Label(params, text="输入火车票信息", font=(
            '华文新魏', '18')).grid(row=0, column=1)
        L2 = tkinter.Label(params, text="出发时间:", font='song -20').grid(row=1)
        L3 = tkinter.Label(params, text="出发地:", font='song -20').grid(row=2)
        L4 = tkinter.Label(params, text="目的地:", font='song -20').grid(row=3)

        date_year = tkinter.StringVar()
        date_month = tkinter.StringVar()
        date_day = tkinter.StringVar()
        start_str = tkinter.StringVar()
        arrive_str = tkinter.StringVar()

        # 设置三个输入文本框
        date_year = tkinter.Entry(
            params, textvariable=date_year, width=10, font='song-20')
        date_month = tkinter.Entry(
            params, textvariable=date_month, width=5, font='song-20')
        date_day = tkinter.Entry(
            params, textvariable=date_day, width=5, font='song-20')
        start_entry = tkinter.Entry(
            params, textvariable=start_str, width=20, font='song-20')
        arrive_entry = tkinter.Entry(
            params, textvariable=arrive_str, width=20, font='song-20')

        date_year.grid(row=1, column=1)
        date_month.grid(row=1, column=2)
        date_day.grid(row=1, column=3)
        start_entry.grid(row=2, column=1)
        arrive_entry.grid(row=3, column=1)

        def re_input1():
            date_year.delete(0, len(date_year.get()))
            date_month.delete(0, len(date_month.get()))
            date_day.delete(0, len(date_day.get()))

        def re_input2():
            start_entry.delete(0, len(start_str.get()))

        def re_input3():
            arrive_entry.delete(0, len(arrive_str.get()))

        def select():
            year = date_year.get()
            month = date_month.get()
            day = date_day.get()
            start = start_str.get()
            arrive = arrive_str.get()

            try:
                # 日期字符串
                date_str = "{:0>4s}-{:0>2s}-{:0>2s}".format(year, month, day)
                date = datetime.datetime.strptime(
                    date_str, '%Y-%m-%d')     # 格式化为datetime格式

            except Exception:
                print('日期输入不符合格式')

            today = datetime.datetime.today()
            last_day = today + datetime.timedelta(days=14)
            if today - datetime.timedelta(days=1) < date < last_day:
                pass
            else:
                print("该日期内未开放抢票")
                re_input1()
                return

            if(start not in stations.keys()):
                print("出发地点不存在")
                re_input2()
                return

            if(arrive not in stations.keys()):
                print("目的地不存在")
                re_input3()
                return

            self.param['leftTicketDTO.train_date'] = date_str
            self.param['leftTicketDTO.from_station'] = stations[start]
            self.param['leftTicketDTO.to_station'] = stations[arrive]
            self.status = 1

            params.destroy()

        btn1 = tkinter.Button(params, text='清空', command=re_input1, font=(
            '宋体', '16')).grid(row=1, column=4)
        btn2 = tkinter.Button(params, text='清空', command=re_input2, font=(
            '宋体', '16')).grid(row=2, column=2)
        btn3 = tkinter.Button(params, text='清空', command=re_input3, font=(
            '宋体', '16')).grid(row=3, column=2)
        btn4 = tkinter.Button(params, text='预定', command=select, font=(
            '宋体', '16')).grid(row=4, column=1)
        params.mainloop()
