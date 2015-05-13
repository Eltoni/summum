
$(document).ready(function(){

    // tratamento para bloquear botão para finalização do cadastro enquanto há um campo sendo editado
    $("input, select").focusin(function() {
        $(":submit").attr("disabled", true);
    });

    $("input, select").focusout(function() {
        $(":submit").attr("disabled", false);
    });


    // Validações dos campos numéricos da compra.
    // Bloqueia entrada de valores diferentes de números
    $(".quantidade-ic").numeric({ decimal: false, negative: false });
    $(".desconto").numeric({ decimal: false, negative: false });
    $(".valor-total-ic").numeric({ negative: false });


    // Esconde mensagem de validação do Django após alguns segundos após a exibição da mesma 
    var mensagem_motivo = document.getElementsByClassName('errorlist')[0]
    setTimeout(function () { mensagem_motivo.className = 'hidden-message' }, 5000);
    setTimeout(function () { mensagem_motivo.className = 'hidden-element' }, 6500);

    var mensagem_erro = document.getElementsByClassName('alert-error')[0]
    setTimeout(function () { mensagem_erro.className = 'hidden-message' }, 5000);
    setTimeout(function () { mensagem_erro.className = 'hidden-element' }, 6500);
    

    // Definição das validações do formulário
    jQuery('#id_fornecedor').attr({'required': 'required', 'oninvalid': "this.setCustomValidity('Informe o fornecedor.')", 'oninput': "this.setCustomValidity('')"});
    jQuery('#id_forma_pagamento').attr({'required': 'required', 'oninvalid': "this.setCustomValidity('Informe a forma de pagamento.')", 'oninput': "this.setCustomValidity('')"});
    jQuery('#id_grupo_encargo').attr({'required': 'required', 'oninvalid': "this.setCustomValidity('Informe o grupo de encargo.')", 'oninput': "this.setCustomValidity('')"});

});


document.addEventListener('DOMContentLoaded', function() {
    
    // Verifica se registro está cadastrado
    // Sendo cadastrado, o link para adicionar outra inline é escondido
    if ( $( ".field-data div .controls .readonly" ).length ) {
        $(".add-row").each(function(){                               
            $(this).addClass( "hidden-element" );                                 
            }  
        );
    }
});