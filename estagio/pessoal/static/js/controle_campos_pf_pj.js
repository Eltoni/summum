
$(document).ready(function(){
    // Inicia com os campos das classes abaixo escondidos
    $(".field-cnpj, .field-razao_social").hide();
    
    /* PESSOA FÍSICA */
    $('#id_tipo_pessoa_0').each(function(){
        // executa no click do mouse na opção 'Pessoa Física'
        $(this).click(function(){
            // checa se a opção 'Pessoa Física' está selecionado 
            if ( $(this).is(':checked')) {
                $(".field-cnpj, .field-razao_social").each(function(){
                    // esconde os campos no contexto
                    $(this).hide();
                    // e mostra os campos das classes abaixo
                    $(".field-cpf").show();
                });
            }
        });
    })

    /* PESSOA JURÍDICA */
    $('#id_tipo_pessoa_1').each(function(){
        // executa no click do mouse na opção 'Pessoa Jurídica'
        $(this).click(function(){
            // checa se a opção 'Pessoa Jurídica' está selecionado 
            if ( $(this).is(':checked')) {
                $(".field-cpf").each(function(){
                    // esconde os campos no contexto
                    $(this).hide();
                    // e mostra os campos das classes abaixo
                    $(".field-cnpj, .field-razao_social").show();
                });
            }
        });
    })
});