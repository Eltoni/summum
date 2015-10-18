$(document).ready(function(){
    
    // Formata a cor das parcelas da conta a pagar
    $('.field-cor_valor_pago p').each(function() {
        var cor_parcela = $(this).css("color");
        $(this).closest("tr").css('color', cor_parcela);
    });
    
});