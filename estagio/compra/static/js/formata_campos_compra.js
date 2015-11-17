
$(document).ready(function(){

    // Definição de alguns comportamentos específicos das inlines na página de compra.
    $("td.delete input[type=checkbox]").after("<div><a class='inline-deletelink' href='javascript:void(0);'>" + gettext('Remover') + "</a></div>");
    $("td.delete input[type=checkbox]").addClass( "hidden-element" );

    $("td.delete .inline-deletelink").each(function() {
        var obj = $(this);
        var row = obj.closest('tr');
        if (row.find('td.delete input[type=checkbox]').is(':checked')) {
            row.addClass( "hidden-element" );
        }

        $(this).on("click", function(){
            var obj = $(this);
            var row = obj.closest('tr');

            row.addClass("hidden-element");
            row.find('td.delete input[type=checkbox]').prop('checked', true);
            row.find('.quantidade-ic').val(0);
            row.find('.valor-total-ic').val(0.00.toFixed(2));

            // Função alocada no arquivo inline_compra.js
            calcula_valor_total();
        });
    });


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
    

    // Definição das validações do formulário
    jQuery('#id_fornecedor').attr({'required': 'required', 'oninvalid': "this.setCustomValidity('Informe o fornecedor.')", 'oninput': "this.setCustomValidity('')"});
    jQuery('#id_forma_pagamento').attr({'required': 'required', 'oninvalid': "this.setCustomValidity('Informe a forma de pagamento.')", 'oninput': "this.setCustomValidity('')"});
    jQuery('#id_grupo_encargo').attr({'required': 'required', 'oninvalid': "this.setCustomValidity('Informe o grupo de encargo.')", 'oninput': "this.setCustomValidity('')"});

});


document.addEventListener('DOMContentLoaded', function() {
    
    // Verifica se registro está cadastrado
    // Sendo cadastrado e atendendo as validações definidas no forms.py o link para adicionar outra inline é escondido
    $(".hidden-form-row").each(function() { 
        if ( $(this).val() == 1 ) {
            $(".add-row").each(function(){                               
                $(this).addClass( "hidden-element" );                                 
                }  
            );
        }
    });

});