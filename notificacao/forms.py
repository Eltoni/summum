#-*- coding: UTF-8 -*-
from django.forms import ModelForm, TextInput, ValidationError
from django.forms.models import BaseInlineFormSet
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html
from suit_redactor.widgets import RedactorWidget
from suit.widgets import SuitSplitDateTimeWidget, AutosizedTextarea

from notificacao.funcoes import converte_bytes


class MensagemForm(ModelForm):

    class Media(object):
        js = (
            '/static/js/suit_redactor/pt_br.js',
        )

    class Meta(object):
        widgets = {
            'texto': RedactorWidget(editor_options={
                'lang': 'pt_br',
                # https://imperavi.com/redactor/docs/settings/
                # 'buttons': ['html', '|', 'formatting', '|', 'bold', 'italic'],
                # 'buttonsHide': ['horizontalrule',]
                }),
            'assunto': TextInput(attrs={'class': 'input-xxlarge'}),
            'data_envio': SuitSplitDateTimeWidget(),
            'destinatario': AutosizedTextarea(attrs={'rows': 2, 'class': 'input-xxlarge', 'placeholder': '...'}),
        }



class AnexoFormSet(BaseInlineFormSet):
    
    def clean(self):
        tamanho_max = settings.FILE_UPLOAD_MAX_MEMORY_SIZE
        tamanho = 0
        for form in self.forms:
            if form.cleaned_data:
                if not form.cleaned_data.get('DELETE'):
                    tamanho += form.instance.arquivo_anexo.size

        if tamanho > tamanho_max:
            msg1 = _(u'Tamanho dos arquivos em anexo supera a capacidade máxima suportada no envio de emails.')
            msg2 = _(u'Tamanho total de todos os arquivos anexos: %s.') % converte_bytes(tamanho)
            msg3 = _(u'Tamanho máximo de anexos suportado: %s.') % converte_bytes(tamanho_max)
            raise ValidationError(format_html('{}<br>{}<br>{}', msg1, msg2, msg3))

