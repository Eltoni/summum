$(document).ready(function(){

    // Se valor do campo Data pagto for "-", então mensalidade não foi paga
    // desta forma, é setada a cor vermelha para a linha
    // $('.field-formata_data_pagto:contains("-")').closest( "tr" ).css('color', 'red');

    // Faz uma iteração nos campos de data de vencimento
    // obtém as datas de vencimento e formata retirando os separadores '/'
    // converte a data obtida num formato de data válido
    // obtém a data atual
    // verifica se a data de vencimento é menor que a data atual
    // caso seja, segnifica que o boleto está vencido. Nesse caso, é difinido a cor vermelha para tal registro
    function formatDate(date) {
        var mm = date.getMonth() + 1;
        var dd = date.getDate();
        var yyyy = date.getFullYear();
        mm = (mm < 10) ? '0' + mm : mm;
        return yyyy + "-" + mm + "-" + dd;
    }

    $('.field-formata_data').each(function() {
        var dataVencimento = $(this).text().split("/");
        dataVencimentoConv = new Date(dataVencimento[2], dataVencimento[1] - 1, dataVencimento[0]);
        var dataAtual = new Date();
        if (formatDate(dataVencimentoConv) < formatDate(dataAtual)) {
            $(this).closest("tr").css('color', '#E8262A');
        }
        
    });

    // Se valor do campo Data pagto não for "-", então mensalidade foi paga
    // desta forma, é setada a cor verde para a linha
    // $('.field-valor_pago:not(:contains("0.00"))').closest( "tr" ).css('color', '#2DB218');
    var $tableRows = $("table tbody tr");
    $tableRows.each(function(n) {
        var valorPago = $(this).find('.field-valor_pago').text();
        if (valorPago > 0.00){
            $(this).css('color', '#2DB218');
        }
    });

    var $tableRows = $("table tbody tr");
    $tableRows.each(function(n) {
        var valorTotal = $(this).find('.field-valor_total').text();
        var valorPago = $(this).find('.field-valor_pago').text();
        if (valorTotal > valorPago && valorPago > 0.00){
            $(this).css('color', '#355EED');
        }
    });

});