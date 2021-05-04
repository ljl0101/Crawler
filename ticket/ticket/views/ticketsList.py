import tkinter
import json


class ticketsList():
    status = 0

    # default
    ticket_info_list = []
    ticket_info = {
        "date": "2021-05-05",
        "start": "WHN",
        "arrive": "BJP",
        "order": "Z78",
        "start_time": "01:18",
        "arrive_time": "12:15",
        "pass_time": "10:57"
    }
    params = []
    param = {
        'train_no': '7800000Z7804',
        'from_station_no': '07',
        'to_station_no': '11',
        'seat_types': '3411',
        'train_date': '2021-05-05'
    }

    def main(self):
        tickets = []

        with open('../resources/tickets.json', 'r', encoding='utf8') as fp:
            tickets = json.load(fp)

        row = 0
        column = 0

        ticketsList = tkinter.Tk()
        ticketsList.title('12306')  # 定义窗体标题
        ticketsList.geometry('2500x1200+0+0')

        def scheduled(row):
            self.param = self.params[row].copy()
            self.ticket_info = self.ticket_info_list[row].copy()

            self.status = 1

            ticketsList.destroy()

        for ticket in tickets:
            list = []
            for value in ticket.values():
                label = tkinter.Label(ticketsList, text=value)
                label.grid(row=row, column=column)
                column += 1
                list.append(value)
            self.ticket_info['date'] = list[0]
            self.ticket_info['start'] = list[1]
            self.ticket_info['arrive'] = list[2]
            self.ticket_info['order'] = list[3]
            self.ticket_info['start_time'] = list[5]
            self.ticket_info['arrive_time'] = list[6]

            self.ticket_info_list.append(self.ticket_info.copy())

            self.param['train_no'] = list[7]
            self.param['from_station_no'] = list[8]
            self.param['to_station_no'] = list[9]
            self.param['seat_types'] = list[10]
            self.param['train_date'] = list[0]

            self.params.append(self.param.copy())

            # date = tkinter.Label(ticketsList, text = ticket[0])
            # start = tkinter.Label(ticketsList, text = ticket[1])
            # arrive = tkinter.Label(ticketsList, text = ticket[2])
            # order = tkinter.Label(ticketsList, text = ticket[3])
            # start_time = tkinter.Label(ticketsList, text = ticket[4])
            # arrive_time = tkinter.Label(ticketsList, text = ticket[5])
            # pass_time = tkinter.Label(ticketsList, text = ticket[6])
            # train_no = tkinter.Label(ticketsList, text = ticket[7])
            # from_station_no = tkinter.Label(ticketsList, text = ticket[8])
            # to_station_no = tkinter.Label(ticketsList, text = ticket[9])
            # train_data = tkinter.Label(ticketsList, text = ticket[0])

            btn = tkinter.Button(ticketsList, text='预定' +
                                 "{:0>2s}".format(str(row)), command=lambda arg=row: scheduled(arg))
            btn.grid(row=row, column=column)
            column = 0

            row += 1

        ticketsList.mainloop()  # 表示事件循环，使窗体一直保持显示状态
