#-*- coding: UTF-8 -*-
from models import Cliente, Fornecedor, Funcionario, Cargo
from import_export import resources
from import_export import fields


#classes usadas pelo import_export
class ClienteResource(resources.ModelResource):

    class Meta:
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
        return '%s' % (cliente.data_nasc.strftime('%d/%m/%Y'))



class FornecedorResource(resources.ModelResource):

    class Meta:
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
        return '%s' % (fornecedor.data_nasc.strftime('%d/%m/%Y'))



class FuncionarioResource(resources.ModelResource):

    class Meta:
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
        return '%s' % (funcionario.data_nasc.strftime('%d/%m/%Y'))

    def dehydrate_cargo(self, funcionario):
        # trata os indicados que não tem vinculo com aluno
        try:
            return '%s' % (funcionario.cargo.nome)
        except:
            pass



class CargoResource(resources.ModelResource):

    class Meta:
        model = Cargo
        #exclude = ('nome', 'estado')