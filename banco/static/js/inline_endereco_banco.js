// $(".campo-estado").change(function(){
//     var estado = $(this);
//     var estado_id = estado.attr( "id" );
//     var number = estado_id.substring(estado_id.indexOf('-') +1)[0];
//     cidade_0 = $('#id_agencia_set-' + number + '-cidade_0').val("");
//     cidade_1 = $('#id_agencia_set-' + number + '-cidade_1').val("");
// });


$(document).ready(function(){
    $.getScript( '/static/selectable/js/jquery.dj.selectable.js' );

    function filtra_cidade(row){
        estado_id = '#' + row.find('.campo-estado').attr( "id" );
        cidade_id = '#' + row.find('.campo-cidade').attr( "id" );
        
        $(cidade_id).djselectable('option', 'prepareQuery', newParameters);
    }

    function newParameters(query) {
        query.estado = $(estado_id).val();
    }

    $('input[id*="id_agencia_set"]').keyup(function(){
        cidade_id = '#' + $(this).attr( "id" );
        number = cidade_id.substring(cidade_id.indexOf('-') +1)[0];
        estado_id = '#id_agencia_set-' + number + '-estado';
        
        $(cidade_id).djselectable('option', 'prepareQuery', newParameters);
    });

    $("a.ui-combo-button").click(function() {
        row = $(this).closest('tr');
        
        filtra_cidade(row);
    });

    $(".campo-estado").change(function() {
        row = $(this).closest('tr');
        row.find('.campo-cidade').val("");

        filtra_cidade(row);
    });
});