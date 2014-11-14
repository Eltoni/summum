
$(document).ready(function(){

    tem_data = $('.field-data div .controls .readonly').text();     // busca o valor do rótulo da data encontrando o elemento em cascata
    if ( tem_data == '(Nenhum)' ) {                                 // e verifica se data não foi inserida
        $(".field-status, .field-data").each(function(){            // caso não tenha sido inserida, significa que a compra não foi registrada no banco
            $(this).hide();                                         // e então esconde os campos no contexto
            }  
        );
    }
});

document.addEventListener('DOMContentLoaded', function() {
    tem_data = $('.field-data div .controls .readonly').text();
    if ( tem_data != '(Nenhum)' ) {
        $(".add-row").each(function(){                               // Verifica se registro está cadastrado
            $(this).addClass( "hidden-element" );                    // Sendo cadastrado, o link para adicionar outra inline é escondido             
            }  
        );
    }
});