
$(document).ready(function(){

    tem_data = $('.field-data div .controls .readonly').text();     // busca o valor do rótulo da data encontrando o elemento em cascata
    if ( tem_data == '(Nenhum)' ) {                                 // e verifica se data não foi inserida
        $(".field-status, .field-data, .field-pedido, .field-status_pedido").each(function(){            // caso não tenha sido inserida, significa que a compra não foi registrada no banco
            $(this).hide();                                         // e então esconde os campos no contexto
            }  
        );

        // função que adiciona o botão "Salvar Pedido" no cadastro da compra
        (function($) {
            $(document).ready(function($) {
                $(".inner-right-column .submit-row").append(
                    '<button type="submit" name="_addpedido" class="btn btn-high btn-warning">Salvar Pedido</button>'
                );
            });
        })(django.jQuery);
    }

});


document.addEventListener('DOMContentLoaded', function() {
    
    // Verifica se registro está cadastrado
    // Sendo cadastrado, o link para adicionar outra inline é escondido
    tem_data = $('.field-data div .controls .readonly').text();
    if ( tem_data != '(Nenhum)' ) {
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

        // Esconde o status do pedido, caso a compra não seja um pedido
        if ( tem_pedido == 'Não' ) {
            $(".field-status_pedido").each(function(){            
                $(this).hide();                                         
                }  
            );
        }
    }
});