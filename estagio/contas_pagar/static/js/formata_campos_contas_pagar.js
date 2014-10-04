
$(document).ready(function(){

    // Desabilita o campo checkbox para edição
    $('.status-parcela').each(function(){
        if ( $(this).is(':checked')) {
    		jQuery(this).prop('disabled', true);
        }
    })

    // desafaz o bloqueio do campo checkbox de não-edição para que o elemnto não perca o valor original após o submit da página
    $('button[type="submit"]').click(function(){
        $('input[type="checkbox"]').attr("disabled",false);
    });

});