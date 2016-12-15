# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Caixas(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1) # Field name made lowercase.
    data = models.DateField(db_column='DATA') # Field name made lowercase.
    valor_entrada = models.DecimalField(db_column='VALOR_ENTRADA', max_digits=20, decimal_places=2) # Field name made lowercase.
    valor_saida = models.DecimalField(db_column='VALOR_SAIDA', max_digits=20, decimal_places=2) # Field name made lowercase.
    valor_total = models.DecimalField(db_column='VALOR_TOTAL', max_digits=20, decimal_places=2) # Field name made lowercase.
    valor_inicial = models.DecimalField(db_column='VALOR_INICIAL', max_digits=20, decimal_places=2) # Field name made lowercase.
    diferenca = models.DecimalField(db_column='DIFERENCA', max_digits=20, decimal_places=2) # Field name made lowercase.
    valor_fechamento = models.DecimalField(db_column='VALOR_FECHAMENTO', max_digits=20, decimal_places=2) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'caixas'

class Cargo(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    nome = models.CharField(db_column='NOME', max_length=100) # Field name made lowercase.
    descricao = models.TextField(db_column='DESCRICAO', blank=True) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'cargo'

class Cidade(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(db_column='NOME', max_length=255) # Field name made lowercase.
    estado = models.ForeignKey('Estado', db_column='ESTADO_ID') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'cidade'

class Cliente(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    nome = models.CharField(db_column='NOME', max_length=255) # Field name made lowercase.
    cpf = models.CharField(db_column='CPF', max_length=11) # Field name made lowercase.
    rg = models.CharField(db_column='RG', max_length=20, blank=True) # Field name made lowercase.
    data_nasc = models.DateField(db_column='DATA_NASC', blank=True, null=True) # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1) # Field name made lowercase.
    endereco = models.CharField(db_column='ENDERECO', max_length=50) # Field name made lowercase.
    bairro = models.CharField(db_column='BAIRRO', max_length=50) # Field name made lowercase.
    complemento = models.CharField(db_column='COMPLEMENTO', max_length=50, blank=True) # Field name made lowercase.
    numero = models.CharField(db_column='NUMERO', max_length=15) # Field name made lowercase.
    cep = models.CharField(db_column='CEP', max_length=9) # Field name made lowercase.
    telefone = models.CharField(db_column='TELEFONE', max_length=30, blank=True) # Field name made lowercase.
    celular = models.CharField(db_column='CELULAR', max_length=30, blank=True) # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', max_length=100, blank=True) # Field name made lowercase.
    cidade = models.ForeignKey(Cidade, db_column='CIDADE_ID') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'cliente'

class Compras(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    total = models.DecimalField(db_column='TOTAL', max_digits=20, decimal_places=2) # Field name made lowercase.
    data = models.DateField(db_column='DATA') # Field name made lowercase.
    desconto = models.DecimalField(db_column='DESCONTO', max_digits=20, decimal_places=2, blank=True, null=True) # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1) # Field name made lowercase.
    fornecedores = models.ForeignKey('Fornecedor', db_column='FORNECEDORES_ID') # Field name made lowercase.
    forma_pagamento = models.ForeignKey('FormaPagamento', db_column='FORMA_PAGAMENTO_ID') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'compras'

class ContasPagar(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    data = models.DateField(db_column='DATA') # Field name made lowercase.
    valor_total = models.DecimalField(db_column='VALOR_TOTAL', max_digits=20, decimal_places=2) # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=2) # Field name made lowercase.
    descricao = models.TextField(db_column='DESCRICAO', blank=True) # Field name made lowercase.
    compras = models.ForeignKey(Compras, db_column='COMPRAS_ID') # Field name made lowercase.
    fornecedores = models.ForeignKey('Fornecedor', db_column='FORNECEDORES_ID') # Field name made lowercase.
    forma_pagamento = models.ForeignKey('FormaPagamento', db_column='FORMA_PAGAMENTO_ID') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'contas_pagar'

class ContasReceber(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    data = models.DateField(db_column='DATA') # Field name made lowercase.
    total = models.DecimalField(db_column='TOTAL', max_digits=20, decimal_places=2) # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1) # Field name made lowercase.
    descricao = models.TextField(db_column='DESCRICAO', blank=True) # Field name made lowercase.
    cliente = models.ForeignKey(Cliente, db_column='CLIENTE_ID') # Field name made lowercase.
    vendas = models.ForeignKey('Vendas', db_column='VENDAS_ID') # Field name made lowercase.
    forma_pagamento = models.ForeignKey('FormaPagamento', db_column='FORMA_PAGAMENTO_ID') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'contas_receber'

class Estado(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    nome = models.CharField(db_column='NOME', max_length=255) # Field name made lowercase.
    sigla = models.CharField(db_column='SIGLA', max_length=2) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'estado'

class FormaPagamento(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    nome = models.CharField(db_column='NOME', max_length=100) # Field name made lowercase.
    quant_parcelas = models.IntegerField(db_column='QUANT_PARCELAS') # Field name made lowercase.
    prazo_entre_parcelas = models.IntegerField(db_column='PRAZO_ENTRE_PARCELAS') # Field name made lowercase.
    tipo_prazo = models.CharField(db_column='TIPO_PRAZO', max_length=1, blank=True) # Field name made lowercase.
    carencia = models.IntegerField(db_column='CARENCIA') # Field name made lowercase.
    tipo_carencia = models.CharField(db_column='TIPO_CARENCIA', max_length=1, blank=True) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'forma_pagamento'

class Fornecedor(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    nome = models.CharField(db_column='NOME', max_length=45) # Field name made lowercase.
    cnpj = models.CharField(db_column='CNPJ', max_length=14) # Field name made lowercase.
    razao_social = models.CharField(db_column='RAZAO_SOCIAL', max_length=255, blank=True) # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1) # Field name made lowercase.
    endereco = models.CharField(db_column='ENDERECO', max_length=50) # Field name made lowercase.
    numero = models.CharField(db_column='NUMERO', max_length=15) # Field name made lowercase.
    bairro = models.CharField(db_column='BAIRRO', max_length=50) # Field name made lowercase.
    complemento = models.CharField(db_column='COMPLEMENTO', max_length=50, blank=True) # Field name made lowercase.
    cep = models.CharField(db_column='CEP', max_length=9, blank=True) # Field name made lowercase.
    telefone = models.CharField(db_column='TELEFONE', max_length=30) # Field name made lowercase.
    celular = models.CharField(db_column='CELULAR', max_length=30, blank=True) # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', max_length=100, blank=True) # Field name made lowercase.
    cidade = models.ForeignKey(Cidade, db_column='CIDADE_id') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'fornecedor'

class Funcionario(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    nome = models.CharField(db_column='NOME', max_length=255) # Field name made lowercase.
    cpf = models.CharField(db_column='CPF', max_length=11, blank=True) # Field name made lowercase.
    rg = models.CharField(db_column='RG', max_length=20, blank=True) # Field name made lowercase.
    data_nasc = models.DateField(db_column='DATA_NASC', blank=True, null=True) # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1) # Field name made lowercase.
    endereco = models.CharField(db_column='ENDERECO', max_length=50) # Field name made lowercase.
    bairro = models.CharField(db_column='BAIRRO', max_length=50) # Field name made lowercase.
    complemento = models.CharField(db_column='COMPLEMENTO', max_length=50, blank=True) # Field name made lowercase.
    numero = models.CharField(db_column='NUMERO', max_length=15) # Field name made lowercase.
    cep = models.CharField(db_column='CEP', max_length=9, blank=True) # Field name made lowercase.
    telefone = models.CharField(db_column='TELEFONE', max_length=30, blank=True) # Field name made lowercase.
    celular = models.CharField(db_column='CELULAR', max_length=30, blank=True) # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', max_length=100, blank=True) # Field name made lowercase.
    salario = models.DecimalField(db_column='SALARIO', max_digits=20, decimal_places=2, blank=True, null=True) # Field name made lowercase.
    cidade = models.ForeignKey(Cidade, db_column='CIDADE_id') # Field name made lowercase.
    cargo = models.ForeignKey(Cargo, db_column='CARGO_ID') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'funcionario'

class ItensCompra(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    quantidade = models.IntegerField(db_column='QUANTIDADE') # Field name made lowercase.
    valor_unitario = models.DecimalField(db_column='VALOR_UNITARIO', max_digits=20, decimal_places=2) # Field name made lowercase.
    desconto = models.DecimalField(db_column='DESCONTO', max_digits=20, decimal_places=2, blank=True, null=True) # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1) # Field name made lowercase.
    produtos = models.ForeignKey('Produtos', db_column='PRODUTOS_ID') # Field name made lowercase.
    compras = models.ForeignKey(Compras, db_column='COMPRAS_ID') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'itens_compra'

class ItensMovEstoque(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    quantidade = models.IntegerField(db_column='QUANTIDADE') # Field name made lowercase.
    tipo_mov = models.CharField(db_column='TIPO_MOV', max_length=1) # Field name made lowercase.
    motivo = models.CharField(db_column='MOTIVO', max_length=255) # Field name made lowercase.
    produtos = models.ForeignKey('Produtos', db_column='PRODUTOS_ID') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'itens_mov_estoque'

class ItensVenda(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    quantidade = models.IntegerField(db_column='QUANTIDADE') # Field name made lowercase.
    valor_unitario = models.DecimalField(db_column='VALOR_UNITARIO', max_digits=20, decimal_places=2) # Field name made lowercase.
    desconto = models.DecimalField(db_column='DESCONTO', max_digits=20, decimal_places=2, blank=True, null=True) # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1) # Field name made lowercase.
    vendas = models.ForeignKey('Vendas', db_column='VENDAS_ID') # Field name made lowercase.
    produtos = models.ForeignKey('Produtos', db_column='PRODUTOS_ID') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'itens_venda'

class Lotes(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    cod_lote = models.CharField(db_column='COD_LOTE', max_length=255) # Field name made lowercase.
    quantidade = models.IntegerField(db_column='QUANTIDADE') # Field name made lowercase.
    produtos = models.ForeignKey('Produtos', db_column='PRODUTOS_ID') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'lotes'

class MovimentosCaixa(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    descricao = models.CharField(db_column='DESCRICAO', max_length=45) # Field name made lowercase.
    valor = models.CharField(db_column='VALOR', max_length=45) # Field name made lowercase.
    data = models.CharField(db_column='DATA', max_length=45) # Field name made lowercase.
    tipo_mov = models.CharField(db_column='TIPO_MOV', max_length=45) # Field name made lowercase.
    caixa = models.ForeignKey(Caixas, db_column='CAIXA_ID') # Field name made lowercase.
    pagamento = models.ForeignKey('Pagamento', db_column='PAGAMENTO_ID', blank=True, null=True) # Field name made lowercase.
    recebimento = models.ForeignKey('Recebimento', db_column='RECEBIMENTO_ID', blank=True, null=True) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'movimentos_caixa'

class Pagamento(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    data = models.DateField(db_column='DATA') # Field name made lowercase.
    valor = models.DecimalField(db_column='VALOR', max_digits=20, decimal_places=2) # Field name made lowercase.
    juros = models.DecimalField(db_column='JUROS', max_digits=20, decimal_places=2, blank=True, null=True) # Field name made lowercase.
    desconto = models.DecimalField(db_column='DESCONTO', max_digits=20, decimal_places=2, blank=True, null=True) # Field name made lowercase.
    parcelas_contas_pagar = models.ForeignKey('ParcelasContasPagar', db_column='PARCELAS_CONTAS_PAGAR_ID') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'pagamento'

class ParcelasContasPagar(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    vencimento = models.DateField(db_column='VENCIMENTO') # Field name made lowercase.
    valor = models.DecimalField(db_column='VALOR', max_digits=20, decimal_places=2) # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1) # Field name made lowercase.
    num_parcelas = models.IntegerField(db_column='NUM_PARCELAS') # Field name made lowercase.
    contas_pagar = models.ForeignKey(ContasPagar, db_column='CONTAS_PAGAR_ID') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'parcelas_contas_pagar'

class ParcelasContasReceber(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    valor = models.DecimalField(db_column='VALOR', max_digits=20, decimal_places=2) # Field name made lowercase.
    vencimento = models.DateField(db_column='VENCIMENTO') # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1) # Field name made lowercase.
    num_parcelas = models.CharField(db_column='NUM_PARCELAS', max_length=45) # Field name made lowercase.
    contas_receber = models.ForeignKey(ContasReceber, db_column='CONTAS_RECEBER_ID') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'parcelas_contas_receber'

class Produtos(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    nome = models.CharField(db_column='NOME', max_length=255) # Field name made lowercase.
    descricao = models.TextField(db_column='DESCRICAO', blank=True) # Field name made lowercase.
    preco = models.DecimalField(db_column='PRECO', max_digits=20, decimal_places=2) # Field name made lowercase.
    preco_venda = models.DecimalField(db_column='PRECO_VENDA', max_digits=20, decimal_places=2) # Field name made lowercase.
    quantidade = models.IntegerField(db_column='QUANTIDADE') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'produtos'

class Recebimento(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    data = models.DateField(db_column='DATA') # Field name made lowercase.
    valor = models.DecimalField(db_column='VALOR', max_digits=20, decimal_places=2) # Field name made lowercase.
    juros = models.DecimalField(db_column='JUROS', max_digits=20, decimal_places=2, blank=True, null=True) # Field name made lowercase.
    desconto = models.DecimalField(db_column='DESCONTO', max_digits=20, decimal_places=2, blank=True, null=True) # Field name made lowercase.
    parcelas_contas_receber = models.ForeignKey(ParcelasContasReceber, db_column='PARCELAS_CONTAS_RECEBER_ID') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'recebimento'

class Vendas(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    total = models.DecimalField(db_column='TOTAL', max_digits=20, decimal_places=2) # Field name made lowercase.
    data = models.DateField(db_column='DATA') # Field name made lowercase.
    desconto = models.DecimalField(db_column='DESCONTO', max_digits=20, decimal_places=2, blank=True, null=True) # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=1) # Field name made lowercase.
    cliente = models.ForeignKey(Cliente, db_column='CLIENTE_ID') # Field name made lowercase.
    forma_pagamento = models.ForeignKey(FormaPagamento, db_column='FORMA_PAGAMENTO_ID') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'vendas'

