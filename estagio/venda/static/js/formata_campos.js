
$(document).ready(function(){
    /*-------------------------------------------------------------------------------------------------------------------------------
    Validações dos campos numéricos da aplicação.
    --------------------------------------------------------------------------------------------------------------------------------*/
    $(".quantidade-ic").numeric({ decimal: false, negative: false }, function() { alert("Somente inteiros positivos"); this.value = ""; this.focus(); });
    $(".desconto").numeric();
    $(".valor-total-ic").numeric({ negative: false }, function() { alert("Valores decimais"); this.value = ""; this.focus(); });

    var mensagem_motivo = document.getElementsByClassName('errorlist')[0]
    setTimeout(function () { mensagem_motivo.className = 'hidden-message' }, 5000);
    setTimeout(function () { mensagem_motivo.className = 'hidden-element' }, 6500);

    var mensagem_erro = document.getElementsByClassName('alert-error')[0]
    setTimeout(function () { mensagem_erro.className = 'hidden-message' }, 5000);
    setTimeout(function () { mensagem_erro.className = 'hidden-element' }, 6500);
});