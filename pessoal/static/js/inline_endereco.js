$(".campo-estado").change(function(){
    var estado = $(this);
    var estado_id = estado.attr( "id" );
    var number = estado_id.substring(estado_id.indexOf('-') +1)[0];
    cidade_0 = $('#id_enderecoentregacliente_set-' + number + '-cidade_0').val("");
    cidade_1 = $('#id_enderecoentregacliente_set-' + number + '-cidade_1').val("");
});


$(document).ready(function(){
    $.getScript( '/static/selectable/js/jquery.dj.selectable.js' );

    $('input[id*="id_enderecoentregacliente_set"]').keyup(function(){
        cidade_id = '#' + $(this).attr( "id" );
        number = cidade_id.substring(cidade_id.indexOf('-') +1)[0];
        estado_id = '#id_enderecoentregacliente_set-' + number + '-estado';
        
        $(cidade_id).djselectable('option', 'prepareQuery', newParameters);
    });

    function newParameters(query) {
        query.estado = $(estado_id).val();
    }
});