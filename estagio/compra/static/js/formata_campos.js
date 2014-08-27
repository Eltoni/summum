
$(document).ready(function(){
    /*-------------------------------------------------------------------------------------------------------------------------------
    Validações dos campos numéricos da aplicação.
    --------------------------------------------------------------------------------------------------------------------------------*/
    $(".quantidade-ic").numeric({ decimal: false, negative: false }, function() { alert("Somente inteiros positivos"); this.value = ""; this.focus(); });
    $(".desconto").numeric();
    $(".valor-total-ic").numeric({ negative: false }, function() { alert("Valores decimais"); this.value = ""; this.focus(); });


});