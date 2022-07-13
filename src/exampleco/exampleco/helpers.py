import datetime


def time_period_to_time_convertor(time_period):
    current_date = datetime.datetime.today()
    if time_period == 'THIS_YEAR':
        current_date = current_date.year
    elif time_period == 'THIS_MONTH':
        current_date = current_date.month
    else:
        current_date = current_date.isocalendar()[1]
    return current_date
