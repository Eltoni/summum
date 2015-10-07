#-*- coding: UTF-8 -*-
from datetime import timedelta
import datetime
from pytz import timezone
from estagio import settings

def dia_util(data):
    """ Valida dia útil. 
        Caso dia da semana retornado na data enviada no parâmetro seja sábado ou domingo, é retornado a data para o próximo dia útil da semana
    """
    dia_semana = data.isoweekday()
    if dia_semana == 6:
        return data + timedelta(days=2)
    if dia_semana == 7:
        return data + timedelta(days=1)
    else:
        return data


def datetime_settings_timezone(d):
    """
    """
    settings_timezone = timezone(settings.TIME_ZONE)
    data = settings_timezone.normalize(d.astimezone(settings_timezone))
    return data


def date_settings_timezone(d):
    """
    """
    settings_timezone = timezone(settings.TIME_ZONE)
    data = settings_timezone.normalize(d.astimezone(settings_timezone)).date()
    return data


def date_add_months(t, p):
    """
    import os
    os.system('cls') #limpar prompt do windows

    Retorna a data somada a quantidade de meses desejados.

    Parâmetros passados (data, quantidade_de_meses)
    
    >>> date_add_months(datetime.date(2010, 1, 1), 1)
    datetime.date(2010, 2, 1)
    >>> date_add_months(datetime.date(2010, 1, 1), 3)
    datetime.date(2010, 4, 1)
    """
    one_month_later = None
    for i in range(p):
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
        t = one_month_later
    if one_month_later == None:
        return datetime.date.today()
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


def date_add_days(t, p):
    """
    Retorna a data somada a quantidade de dias desejadas.

    Parâmetros passados (data, quantidade_de_dias)
    
    >>> date_add_days(datetime.date(2010, 1, 1), 2)
    datetime.date(2010, 1, 15)
    >>> date_add_days(datetime.date(2014, 1, 10), 2)
    datetime.date(2014, 1, 24)
    """
    data = t
    data = data + datetime.timedelta(days=p)
    return data


if __name__ == '__main__':
    import doctest
    doctest.testmod()