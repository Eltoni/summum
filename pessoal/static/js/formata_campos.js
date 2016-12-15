$(document).ready(function(){

    //****************************************************************************************************************************************
    // Monta a paginação da inline
    //****************************************************************************************************************************************

    /* Conta */
    var contas = $( "div[id^='contaspagar_set-group'], div[id^='contasreceber_set-group']" ).find( ".table" );
    // acerta formatação original
    $(contas).find( "tbody tr" ).each(function(i) {
        $(this).find("td:first p").css({ display: "inline" });
    });
    // Insere trechos html no documento
    $(contas).attr({"data-page-size": "10", "id": "registro_contas"});
    $(contas).append(" <tfoot><tr><td colspan='6'><div class='pagination pagination-centered hide-if-no-paging'></div></td></tr></tfoot>");


    // Script de definição da paginação
    $(function () {
      $('#registro_contas').footable();

        $('#change-page-size').change(function (e) {
          e.preventDefault();
          var pageSize = $(this).val();
          $('.footable').data('page-size', pageSize);
          $('.footable').trigger('footable_initialized');
        });

        $('#change-nav-size').change(function (e) {
          e.preventDefault();
          var navSize = $(this).val();
          $('.footable').data('limit-navigation', navSize);
          $('.footable').trigger('footable_initialized');
        });
      });

    // Esconde registros vazios na inline
    ultimo_registro = $(contas).find( "tbody tr:last" ).remove(); 
});