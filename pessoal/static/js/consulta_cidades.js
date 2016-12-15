$(document).ready(function(){

    // $('#enderecoentregacliente_set-group').formset({
    //         added: bindSelectables
    // });

    function newParameters(query) {
        query.estado = $('#id_estado').val();
    }
    $('#id_cidade_0').djselectable('option', 'prepareQuery', newParameters);

    $("#id_estado").change(function(){
        $("#id_cidade_0, #id_cidade_1").val("");     
    });
});