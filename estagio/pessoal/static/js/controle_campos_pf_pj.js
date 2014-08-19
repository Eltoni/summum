/* --------------------------------------------------------------------------------------
    #id_tipo_pessoa_0   > id opção Pessoa Física
    #id_tipo_pessoa_1   > id opção Pessoa Juridica
    .field-cpf          > classe campo cpf
    .field-cnpj         > classe campo cnpj
    .field-razao_social > classe campo razao social
 -------------------------------------------------------------------------------------- */

$(document).ready(function(){
    // Em tempo de execução, esconde os campos que não pertencem a opção do combobox selecionado
    if ( $('#id_tipo_pessoa_0').attr('checked')) {
        $(".field-cnpj, .field-razao_social").hide();
    } else {
        $(".field-cpf").hide();
    }


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

                    // checa se campo cnpj tem valor
                    if ( $("#id_cnpj").val()!='') {
                        // se tem, o campo cpf fica vazio
                        $('#id_cpf').val(""); 
                    }  
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

                    // checa se campo cpf foi digitado
                    if ( $("#id_cpf").val()!='') {
                        // se foi digitado, os campos cnpj e razão social ficam vazios  
                        $('#id_cnpj, #id_razao_social').val(""); 
                    }   
                });
            }
        });
    })
});