#-*- coding: UTF-8 -*-
import datetime

def add_one_month(t):
    """
    Return a `datetime.date` or `datetime.datetime` (as given) that is
    one month earlier.

    Note that the resultant day of the month might change if the following
    month has fewer days:

    >>> add_one_month(datetime.date(2010, 1, 1))
    datetime.date(2010, 2, 1)
    >>> add_one_month(datetime.date(2010, 1, 31))
    datetime.date(2010, 2, 28)
    >>> add_one_month(datetime.date(2010, 12, 1))
    datetime.date(2011, 1, 1)
    >>> add_one_month(datetime.date(2010, 12, 31))
    datetime.date(2011, 1, 31)
    >>> add_one_month(datetime.date(2011, 3, 31))
    datetime.date(2011, 4, 30)
    """
    one_day = datetime.timedelta(days=1)
    one_month_later = t + one_day
    while one_month_later.month == t.month:  # advance to start of next month
        one_month_later += one_day
    target_month = one_month_later.month
    while one_month_later.day < t.day:  # advance to appropriate day
        one_month_later += one_day
        if one_month_later.month != target_month:  # gone too far
            one_month_later -= one_day
            break
    return one_month_later


def date_add_week(t, p):
    """
    Retorna a data somada a quantidade de semanas desejadas.

    Parâmetros passados (data, quantidade_de_semanas)
    
    >>> date_add_week(datetime.date(2010, 1, 1), 2)
    datetime.date(2010, 1, 15)
    >>> date_add_week(datetime.date(2014, 1, 10), 2)
    datetime.date(2014, 1, 24)
    """
    data = str(t)
    aDate = datetime.datetime.strptime(data, "%Y-%m-%d")
    threeWeeks = datetime.timedelta(weeks=p)
    data = aDate + threeWeeks
    data = data.date()
    return data


if __name__ == '__main__':
    import doctest
    doctest.testmod()