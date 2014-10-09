
$(document).ready(function(){

    // Desabilita o campo checkbox para edição
    var contaPagar = $('.field-status div .controls img', this).attr('alt');
    $('.status-parcela').each(function(){
        // verifica se checkbox está marcado, ou se a conta está fechada
        if ( $(this).is(':checked') || contaPagar=='True') {
    		jQuery(this).prop('disabled', true);
        }
    })

    // desafaz o bloqueio do campo checkbox de não-edição para que o elemnto não perca o valor original após o submit da página
    $('button[type="submit"]').click(function(){
        $('input[type="checkbox"]').attr("disabled",false);
    });

});