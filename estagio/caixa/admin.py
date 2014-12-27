#-*- coding: UTF-8 -*-
from django.contrib import admin
from models import *
from django.core.mail import send_mail


class CaixaAdmin(admin.ModelAdmin):
    model = Caixa
    list_display = ('id', 'data_abertura', 'data_fechamento', 'diferenca', 'status')


    def get_form(self, request, obj=None, **kwargs):
        self.suit_form_tabs = [('geral', 'Geral'),]
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
            texto = u'Há um novo Caixa criado no sistema, aberto por: %s %s. Com Valor inicial de R$ %s.' % (request.user.first_name, request.user.last_name, obj.valor_inicial)
            send_mail(
                'Notificação (Estágio)',    # subject
                texto,                      # message
                'gustavo.sdo@gmail.com',    # from
                ['gustavo.sdo@gmail.com'],  # to
                fail_silently=False
            )
        obj.save()
        super(CaixaAdmin, self).save_model(request, obj, form, change)



class MovimentosCaixaAdmin(admin.ModelAdmin):
    model = MovimentosCaixa
    list_display = ('id', 'caixa', 'pagamento_associado', 'recebimento_associado', 'tipo_mov', 'valor')
    readonly_fields = ('descricao', 'valor', 'data', 'tipo_mov', 'caixa', 'pagamento_associado', 'recebimento_associado')
    fields = ('descricao', 'valor', 'data', 'tipo_mov', 'caixa', 'pagamento_associado', 'recebimento_associado')

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(Caixa, CaixaAdmin)
admin.site.register(MovimentosCaixa, MovimentosCaixaAdmin)