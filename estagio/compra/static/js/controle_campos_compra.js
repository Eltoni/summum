
$(document).ready(function(){
    //$(".add-row").hide();
    //$('.add-row').css({"display":"none"});
    //$(".add-row").css("display", "none");

    tem_data = $('.field-data div .controls .readonly').text();     // busca o valor do rótulo da data encontrando o elemento em cascata
    if ( tem_data == '(Nenhum)' ) {                                 // e verifica se data não foi inserida
        $(".field-status, .field-data").each(function(){            // caso não tenha sido inserida, significa que a compra não foi registrada no banco
            $(this).hide();                                         // e então esconde os campos no contexto
            }  
        );
    }


});