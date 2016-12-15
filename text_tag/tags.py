#-*- coding: UTF-8 -*-
from django.template import defaultfilters
from django.utils.translation import ugettext_lazy as _
from datetime import datetime, timedelta

from text_tag.registry import registry


class BaseDateTag(object):
    """
    Esta classe define todos os métodos de retorno e formatação de 
    datas e horārios utilizados no processamento das tags e filtros 
    da aplicação.

    Métodos nomeados com final "_tag" são identificados automaticamente
    como tags. Jå, mêtodos nomeados com final "_filter" são identificados 
    automaticamente como filtros.
    """
    def __init__(self):
        self.current_datetime = datetime.now()

    def datetime_tag(self, days=0, minutes=0, hours=0, weeks=0):
        """ 
        Retorna a data e hora corrente.
        Parâmetros aceitos: days, minutes, hours, weeks
        Uso: {{datetime_tag[0, 0, 0, 0]}}
        """
        datetime = self.current_datetime + timedelta(days=days, minutes=minutes, hours=hours, weeks=weeks)
        return datetime

    def date_tag(self, days=0, weeks=0):
        """ 
        Retorna a data corrente no formato padrão do sistema.
        Parâmetros aceitos: days, weeks
        Uso: {{date_tag[0, 0]}}
        """
        date = self.datetime_tag(days=days, weeks=weeks).date()
        return date

    def time_tag(self, minutes=0, hours=0):
        """ 
        Retorna o horário corrente.
        Parâmetros aceitos: minutes, hours
        Uso: {{time_tag}}
        """
        time = self.datetime_tag(minutes=minutes, hours=hours).time()
        return time

    def dt_d_tag(self, days=0, weeks=0):
        """ 
        Retorna o dia corrente.
        Parâmetros aceitos: days, weeks
        Uso: {{dt_d_tag}}
        """
        dt_d = self.date_tag(days=days, weeks=weeks).day
        return dt_d

    def d_month_tag(self, days=0, weeks=0):
        """ 
        Retorna o mês corrente.
        Parâmetros aceitos: days, weeks
        Uso: {{d_month_tag}}
        """
        d_month = self.date_tag(days=days, weeks=weeks).month
        return d_month

    def d_year_tag(self, days=0, weeks=0):
        """ 
        Retorna o ano corrente.
        Parâmetros aceitos: days, weeks
        Uso: {{d_year_tag}}
        """
        d_year = self.date_tag(days=days, weeks=weeks).year
        return d_year

    def format_datetime_filter(self, p_datetime, format_datetime=None):
        """ 
        Retorna data e hora no formato desejado.
        Padrão: Definido pelo sistema.
        Parâmetros aceitos: format_datetime
        Uso: {{any_tag|format_datetime_filter}}
        """
        if not format_datetime:
            datetime = defaultfilters.date(p_datetime, "SHORT_DATETIME_FORMAT")
        else:
            datetime = p_datetime.strftime(format_datetime)
        return datetime

    def format_date_filter(self, p_date, format_date=None):
        """ 
        Retorna data no formato desejado.
        Padrão: Definido pelo sistema.
        Parâmetros aceitos: format_date
        Uso: {{any_tag|format_date_filter}}
        """
        if not format_date:
            date = defaultfilters.date(p_date, "SHORT_DATE_FORMAT")
        else:
            date = p_date.strftime(format_date)
        return date

    def format_time_filter(self, p_time, format_time=None):
        """ 
        Retorna hora no formato desejado.
        Padrão: Definido pelo sistema.
        Parâmetros aceitos: format_time
        Uso: {{any_tag|format_time_filter}}
        """
        if not format_time:
            time = defaultfilters.date(p_time, "TIME_FORMAT")
        else:
            time = p_time.strftime(format_time)
        return time

registry.register(BaseDateTag)