#-*- coding: UTF-8 -*-
from django import forms
from localflavor.br.forms import BRStateChoiceField


class CidadeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CidadeForm, self).__init__(*args, **kwargs)
        self.fields['estado'] = BRStateChoiceField(initial="PR")



# class CalendarWidget(forms.TextInput):
# """ Exemplo de utilização de css e javascript no Django  """
#     class Media:
#         css = {
#             'all': ('pretty.css',)
#         }
#         js = ('animations.js', 'actions.js')
