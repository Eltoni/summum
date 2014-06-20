from import_export import resources
from models import Cliente, Fornecedor, Funcionario, Cargo

#classes usadas pelo import_export
class ClienteResource(resources.ModelResource):

    class Meta:
        model = Cliente
        #exclude = ('nome', 'estado')



class FornecedorResource(resources.ModelResource):

    class Meta:
        model = Fornecedor
        #exclude = ('nome', 'estado')


class FuncionarioResource(resources.ModelResource):

    class Meta:
        model = Funcionario
        #exclude = ('nome', 'estado')


class CargoResource(resources.ModelResource):

    class Meta:
        model = Cargo
        #exclude = ('nome', 'estado')