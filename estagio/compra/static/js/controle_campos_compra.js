
document.addEventListener('DOMContentLoaded', function() {
    
    // Verifica se registro está cadastrado
    // Sendo cadastrado, o link para adicionar outra inline é escondido
    if ( $( ".field-data div .controls .readonly" ).length ) {
        $(".add-row").each(function(){                               
            $(this).addClass( "hidden-element" );                                 
            }  
        );

        // Obtém os valores nos campos e rótulos no formulário, e verifica se o botão "Confirmar Pedido" deve ser exibido
        status_cancelado = $('[name="status"]').is(':checked');
        pedido_confirmado = $('.field-status_pedido div .controls img', this).attr('alt');
        tem_pedido = $('.field-pedido div .controls .readonly').text();

        if ( tem_pedido == 'Sim' && pedido_confirmado == 'False' && !status_cancelado ) {
            (function($) {
                $(document).ready(function($) {
                    $('button[name=_addanother]').after('<button type="submit" name="_addconfirmapedido" class="btn btn-high btn-warning">Confirmar Pedido</button>')
                });
            })(django.jQuery);
        }
    }
    else {

        // função que adiciona o botão "Salvar Pedido" no cadastro da compra
        (function($) {
            $(document).ready(function($) {
                    id = 1;
                    $.ajax({       
                        type: "GET",
                        url: "/checa_pedido_compra_habilitado/"+id,
                        context: document.body,
                        dataType: "json",
                        success: function(retorno){
                            $.each(retorno, function(i, exibe_botao_pedido_compra){
                                var pedido_compra = exibe_botao_pedido_compra.fields['habilita_pedido_compra'];
                                if ( pedido_compra == true ) {
                                    $(".inner-right-column .submit-row").append(
                                        '<button type="submit" name="_addpedido" class="btn btn-high btn-warning">Salvar Pedido</button>'
                                    );
                                }
                                });
                            },
                        error: function() {
                            alert("Erro na requisição Ajax");
                        }
                    }); 
            });
        })(django.jQuery);
    }
});