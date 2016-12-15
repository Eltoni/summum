#-*- coding: UTF-8 -*-
from import_export import resources, fields

from pessoal.models import Cliente, Fornecedor, Funcionario, Cargo
from utilitarios.funcoes import remove_tags

#classes usadas pelo import_export
class ClienteResource(resources.ModelResource):
    status_financeiro = fields.Field()

    class Meta(object):
        model = Cliente
        #exclude = ('nome', 'estado')

    def dehydrate_status(self, cliente):
        if cliente.status:
            return 'Ativo'
        else:
            return 'Inativo'

    def dehydrate_data(self, cliente):
        return '%s' % (cliente.data.strftime('%d/%m/%Y'))

    def dehydrate_data_nasc(self, cliente):
        try:
            return '%s' % (cliente.data_nasc.strftime('%d/%m/%Y'))
        except AttributeError:
            return None

    def dehydrate_status_financeiro(self, cliente):
        return remove_tags(cliente.status_financeiro())

    def dehydrate_cidade(self, cliente):
        return '%s' % (cliente.cidade.nome)


class FornecedorResource(resources.ModelResource):
    status_financeiro = fields.Field()

    class Meta(object):
        model = Fornecedor
        #exclude = ('nome', 'estado')

    def dehydrate_status(self, fornecedor):
        if fornecedor.status:
            return 'Ativo'
        else:
            return 'Inativo'

    def dehydrate_data(self, fornecedor):
        return '%s' % (fornecedor.data.strftime('%d/%m/%Y'))

    def dehydrate_data_nasc(self, fornecedor):
        try:
            return '%s' % (fornecedor.data_nasc.strftime('%d/%m/%Y'))
        except AttributeError:
            return None

    def dehydrate_status_financeiro(self, fornecedor):
        return remove_tags(fornecedor.status_financeiro())

    def dehydrate_cidade(self, fornecedor):
        return '%s' % (fornecedor.cidade.nome)



class FuncionarioResource(resources.ModelResource):

    class Meta(object):
        model = Funcionario
        #exclude = ('nome', 'estado')

    def dehydrate_status(self, funcionario):
        if funcionario.status:
            return 'Ativo'
        else:
            return 'Inativo'

    def dehydrate_data(self, funcionario):
        return '%s' % (funcionario.data.strftime('%d/%m/%Y'))

    def dehydrate_data_nasc(self, funcionario):
        try:
            return '%s' % (funcionario.data_nasc.strftime('%d/%m/%Y'))
        except AttributeError:
            return None
            
    def dehydrate_cargo(self, funcionario):
        # trata os indicados que não tem vinculo com aluno
        try:
            return '%s' % (funcionario.cargo.nome)
        except AttributeError:
            pass

    def dehydrate_cidade(self, funcionario):
        return '%s' % (funcionario.cidade.nome)



class CargoResource(resources.ModelResource):

    class Meta(object):
        model = Cargo
        #exclude = ('nome', 'estado')