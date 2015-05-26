# from configuracoes.models import OrdemModelos, Parametrizacao
# from django.apps import apps
# get_model = apps.get_model

# #ordem_modelos = OrdemModelos()
# lista_models = [('compra', 'Compra'), ('venda', 'Venda'), ('movimento', 'Produtos'), ('caixa', 'Caixa'), ('caixa', 'MovimentosCaixa'),]
# for item_lista in lista_models:
# 	model = get_model(item_lista[0], item_lista[1])
# 	campos = model._meta.local_fields
# 	campos = [c.name for c in campos]
# 	classe = model.__name__
# 	for campo in campos:
# 		OrdemModelos(campo=campo, classe=classe, parametrizacao=Parametrizacao.objects.get()).save()


# # OrdemModelos.objects.all().delete()		