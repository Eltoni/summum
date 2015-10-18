
    function calcula_valor_total() {

        var sum = 0;
        // iteração através de cada campo e adiciona o valor
        $(".valor-total-ic").each(function() {

        // adiciona somente se o valor é número
        if(!isNaN(this.value) && this.value.length!=0) {
            sum += parseFloat(this.value);
        }

        });
        // .toFixed() método de arredondamento da soma final para 2 casas decimais

        var descontoTotal = $('#id_desconto').val();
        var percentualDescontoTotal = (sum * descontoTotal) / 100.00;
        sum = sum - percentualDescontoTotal;

        $('#id_total').val(sum.toFixed(2));
    }

    function calcula_valor_total_inline(inline){
        var row = $(inline).closest('tr');
        var quantidade = row.find('.quantidade-ic').val();
        var valorUnitario = row.find('.valor-unitario-ic').val();
        var valorItemCompra = valorUnitario * quantidade;
        var desconto = row.find('.desconto').val();
        var valorPercentualDesconto = (valorItemCompra * desconto) / 100.00;
        valorItemCompra = valorItemCompra - valorPercentualDesconto; 

        var produto = row.find('.vForeignKeyRawIdAdminField').val();
        if (produto) {
            row.find('.valor-total-ic').val(valorItemCompra.toFixed(2));
        };
    }

    function novo_registro_inline(inline){
        inline.find('.quantidade-ic, .desconto, .valor-total-ic').val("");
    }

    function limpa_campos_inline(inline){
        inline.find('input').val("");
        inline.find(".salmonella_label").empty();

        inline.find('.desconto').attr({"readonly": "readonly"});
        inline.find('.quantidade-ic').attr({"readonly": "readonly"});
        inline.find('.quantidade-ic').removeAttr('required');  
        inline.find('.quantidade-ic').attr({oninvalid: "this.setCustomValidity('')"});                                               
        inline.find('.quantidade-ic').removeAttr('max');
        inline.find('.quantidade-ic').removeAttr('title');
        inline.find('.quantidade-ic').removeAttr('oninput'); 
    }

    function dismissRelatedLookupPopup(win, chosenId) {
        var name = windowname_to_id(win.name);
        var elem = document.getElementById(name);
        elem.value = chosenId;
        django.jQuery(elem).trigger('change');
        win.close();

        var row = $(elem).closest('tr');
        var element = $('#'+name);
        var app = element.next("a").attr("data-app");
        var model = element.next("a").attr("data-model");

        if (app == 'movimento' && model == 'produtos'){
            busca_valor_unitario(elem.value, row);
        }
    }

    function busca_valor_unitario(produto, inline){
      $.ajax({       
        type: "GET",
        url: "/venda/venda/get_valor_unitario/"+produto,
        dataType: "json",
        success: function(retorno){
            $.each(retorno, function(i, produtos){ 
                novo_registro_inline(inline);

                var statusProduto = produtos.fields['status'];
                if (statusProduto == false){
                    limpa_campos_inline(inline);
                }
                else{
                    var valorUnitario = produtos.fields['preco_venda'];
                    var quantidadeProduto = inline.find('.valor-unitario-ic').val(valorUnitario);
                    inline.find('.quantidade-ic').focus();

                    jQuery(inline.find('.quantidade-ic')).attr({"required": "required"});
                    jQuery(inline.find('.quantidade-ic')).removeAttr('readonly');
                    jQuery(inline.find('.desconto')).removeAttr('readonly'); 
                }
            });
        }
      }); 
    }

    function valida_quantidade_produto_estoque(produto, inline){
        if(!isNaN(produto) && produto.length!=0) {
          $.ajax({       
            type: "GET",
            url: "/venda/venda/get_valor_unitario/"+produto,
            dataType: "json",
            success: function(retorno){
                $.each(retorno, function(i, produtos){
                    var quantidadeProduto = produtos.fields['quantidade'];
                    jQuery(inline.find('.quantidade-ic')).attr({
                        "max": quantidadeProduto,
                        "title": "Há somente " + quantidadeProduto + " unidades no estoque.", 
                        oninvalid: "this.setCustomValidity('Quantidade limite ultrapassada.')", 
                        oninput:"this.setCustomValidity('')" 
                    });
                });
            }
          }); 
        }
    }

    $(".quantidade-ic, .desconto, .vForeignKeyRawIdAdminField").blur(function(){
        var inline = $(this).closest('tr');
        var produto = inline.find('.vForeignKeyRawIdAdminField').val();
        valida_quantidade_produto_estoque(produto, inline);
    });

    $(".quantidade-ic, .desconto").keyup(function(){
        var inline = $(this);
        calcula_valor_total_inline(inline);
    });

    $(".vForeignKeyRawIdAdminField").change(function(){
        var inline = $(this);
        var app = inline.next("a").attr("data-app");
        var model = inline.next("a").attr("data-model");
        var valor = inline.val();

        if (app == 'movimento' && model == 'produtos'){
            var row = $(inline).closest('tr');

            if (valor != ""){
                busca_valor_unitario(valor, row);
            }
            else{
                limpa_campos_inline(row);
            }
            calcula_valor_total();
        }
    });

    $(".salmonella-clear-field").click(function(e){
        var $this = $(this);
        var row = $(this).closest('tr');
        limpa_campos_inline(row);
        calcula_valor_total();
    });

    $(".inline-deletelink").click(function(e){
        calcula_valor_total();
    });

    $(".quantidade-ic, .desconto, #id_desconto").each(function() {

      $(this).keyup(function(){
          calcula_valor_total();
      });
    });


    // Corrige os campos do formulário após o reload da página
    $(document).ready(function(){
        $(".field-produto .vForeignKeyRawIdAdminField").each(function() {
            var obj = $(this);
            var row = obj.closest('tr');

            if( obj.val() != "") {
                jQuery(row.find('.quantidade-ic')).attr({"required": "required"});
                jQuery(row.find('.quantidade-ic')).removeAttr('readonly');
                jQuery(row.find('.desconto')).removeAttr('readonly'); 
            }
        });

        // Teste para ignorar a validação do HTML ao clicar no botão "Salvar Pedido"
        // $('button[type=submit][name=_addpedido]').click(function(){
        //     $('form').attr('novalidate','novalidate');
        // });
    });