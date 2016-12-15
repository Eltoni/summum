
$(document).ready(function(){

    //$(".geoposition-search").css("margin-right", "15px");
    //$('.geoposition-search').attr('style', 'margin-right: 15px !important');

    $(".endereco-entrega-field").change(function(){
        endereco = $(this).val();
        if( endereco.length > 0 ) {
            $.ajax({       
                type: "GET",
                url: "/venda/venda/get_endereco_entrega_cliente/"+endereco,
                dataType: "json",
                success: function(retorno){
                    $.each(retorno, function(i, enderecos){ 

                        var endereco_entrega = enderecos.fields['endereco'];
                        var cidade_entrega = enderecos.fields['cidade'];
                        var estado_entrega = enderecos.fields['estado'];
                        var endereco_entrega_cliente = endereco_entrega + ", " + cidade_entrega + " - " + estado_entrega;
                        $('.geoposition-search input[type="search"]').val(endereco_entrega_cliente);
                    });
                }
            }); 
        } else {
            valor_select = ""
            $('.geoposition-search input[type="search"]').val(valor_select);
        }

        // value = $(this).find('option:selected').val();
        // if( value.length > 0 ) {
        //     valor_select = $(this).find('option:selected').text();
        // } else {
        //     valor_select = ""
        // }

        // $('.geoposition-search input[type="search"]').val(valor_select);       
    });
   
});
