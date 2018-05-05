import datetime

def get_today():
    return datetime.date.today()

def add_days(input_date, add_days):
    return input_date + datetime.timedelta(days = add_days)

def date_format(date_):
    return "%d/%d" % (date_.month, date_.day)


if __name__ == '__main__':

    today = get_today()
    today_str = date_format(today)
    print(today_str)

    tomorrow = add_days(today, 1)
    tomorrow_str = date_format(tomorrow)
    print(tomorrow_str)

    print(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
