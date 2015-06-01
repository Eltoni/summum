#-*- coding: UTF-8 -*-
from django.contrib import admin
from caixa.models import *
from django.core.mail import EmailMultiAlternatives
from django.utils.translation import ugettext_lazy as _
from import_export.admin import ExportMixin
from caixa.export import CaixaResource, MovimentosCaixaResource
from decimal import Decimal
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from django.db.models import Q
from daterange_filter.filter import DateRangeFilter
from utilitarios.funcoes_email import TextosEmail
from configuracoes.models import Parametrizacao


class CaixaAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = CaixaResource
    model = Caixa
    list_display = ('id', 'data_abertura', 'formata_data_fechamento', 'diferenca', 'status')
    list_filter = (('data_fechamento', DateRangeFilter),)
    date_hierarchy = 'data_abertura'
    

    def has_add_permission(self, request, obj=None):
        """Remove a permissão para adicionar novo caixa, caso já exista um aberto"""

        caixa_aberto = Caixa.objects.filter(status=True).exists()
        if caixa_aberto:
            return False
        else:
            return True


    def get_form(self, request, obj=None, **kwargs):
        self.suit_form_tabs = [('geral', _(u"Geral")),]
        self.fieldsets = (
            (None, {
                'classes': ('suit-tab suit-tab-geral',),
                'fields' : ('data_abertura', 'data_fechamento', 'valor_entrada', 'valor_saida', 'valor_total', 'valor_inicial', 'valor_fechamento', 'diferenca',)
            }),
        )

        if obj is None:
            self.fieldsets[0][1]['fields'] = ('valor_inicial',)

        else:
            if not obj.data_fechamento:
                self.fieldsets[0][1]['fields'] = ('status',) + self.fieldsets[0][1]['fields']
                self.fieldsets[0][1]['fields'] = tuple(x for x in self.fieldsets[0][1]['fields'] if (x!='data_fechamento' and x!='diferenca' and x!='valor_total'))
                # self.fieldsets[0][1]['fields'] = tuple(x for x in self.fieldsets[0][1]['fields'] if x!='data_fechamento')
                # self.fieldsets[0][1]['fields'] = tuple(x for x in self.fieldsets[0][1]['fields'] if x!='diferenca')
                # self.fieldsets[0][1]['fields'] = tuple(x for x in self.fieldsets[0][1]['fields'] if x!='valor_total')

        return super(CaixaAdmin, self).get_form(request, obj, **kwargs)


    def get_readonly_fields(self, request, obj=None):
        """ Define somente alguns campos do cadastro do caixa como somente leitura caso o registro seja salvo no BD """
        
        readonly_fields = ['data_abertura', 'data_fechamento', 'valor_entrada', 'valor_saida', 'valor_total', 'diferenca',]

        if obj:
            readonly_fields.append('valor_inicial')
            if obj.data_fechamento:
                readonly_fields.append('valor_fechamento')
            
            return readonly_fields
        else:
            readonly_fields.append('valor_fechamento')
            return readonly_fields


    def save_model(self, request, obj, form, change):
        if not change:
            obj.save()

            # Envia email somente para usuários com permissão para receber
            perm = Permission.objects.get(codename='recebe_notificacoes_caixa')
            usuarios_perm = User.objects.filter(Q(groups__permissions=perm) | Q(user_permissions=perm) | Q(is_superuser=True)).values_list('email')
            usuarios_perm_notificacao = ', '.join([str(i[0]) for i in usuarios_perm])
            #to = 'gustavo.sdo@gmail.com'
            mensagem_customizada = Parametrizacao.objects.get().email_abertura_caixa

            assunto = u'Notificação (Abertura de Caixa)'
            from_email = 'gustavo.sdo@gmail.com'
            text_content = u'Essa é uma mensagem importante.'
            html_content = u'%(header)s \
                             <p>Há um novo Caixa criado no sistema, aberto por: %(nome)s %(sobrenome)s.</p> \
                             <br> \
                             <a href="http://%(url)s/%(caixa)s" target="_blank">Caixa %(caixa)s</a>\
                             <p>Valor inicial de <strong>R$%(valor_inicial)s</strong>.</p> \
                             <p>Data de abertura <strong>%(data_abertura)s</strong>.</p> \
                             <br>%(texto_customizado)s \
                             %(footer)s'\
                             % {'nome': request.user.first_name, 
                                'sobrenome': request.user.last_name, 
                                'valor_inicial': Decimal(obj.valor_inicial).quantize(Decimal("0.00")),
                                'url': request.META['HTTP_HOST'] + '/' + obj._meta.app_label + '/' + obj._meta.model_name,
                                'caixa': obj.pk,
                                'data_abertura': obj.data_abertura.strftime('%d/%m/%Y às %H:%M:%S'),
                                'header': TextosEmail.headerEmailInterno,
                                'footer': TextosEmail.footerEmailInterno,
                                'texto_customizado': mensagem_customizada
                                }

            mensagem = EmailMultiAlternatives(assunto, text_content, from_email, [usuarios_perm_notificacao])
            mensagem.attach_alternative(html_content, "text/html")
            mensagem.send()
        obj.save()
        super(CaixaAdmin, self).save_model(request, obj, form, change)



class MovimentosCaixaAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = MovimentosCaixaResource
    model = MovimentosCaixa
    list_display = ('id', 'caixa', 'pagamento_associado', 'recebimento_associado', 'tipo_mov', 'valor')
    list_filter = (('data', DateRangeFilter), 'tipo_mov')
    date_hierarchy = 'data'
    readonly_fields = ('descricao', 'valor', 'data', 'tipo_mov', 'caixa', 'pagamento_associado', 'recebimento_associado')
    fields = ('descricao', 'valor', 'data', 'tipo_mov', 'caixa', 'pagamento_associado', 'recebimento_associado')

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(Caixa, CaixaAdmin)
admin.site.register(MovimentosCaixa, MovimentosCaixaAdmin)