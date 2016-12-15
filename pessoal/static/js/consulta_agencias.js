$(document).ready(function(){

    function newParameters(query) {
        query.banco = $('#id_banco_1').val();
    }
    $('#id_agencia_0').djselectable('option', 'prepareQuery', newParameters);

    $("#id_banco_1").change(function(){
        $("#id_agencia_0, #id_agencia_1").val("");     
    });
});