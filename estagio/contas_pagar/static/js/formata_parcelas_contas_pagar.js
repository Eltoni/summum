$(document).ready(function(){

    // Formata a cor das parcelas da conta a pagar
    $('.field-link_pagamentos_parcela a').each(function() {
        var cor_parcela = $(this).css("color");
        $(this).closest("tr").css('color', cor_parcela);
    });


    // Modal que abre a janela para pagamentos da conta
    $('.modal-pagamento').click(function(event) {
      event.preventDefault();
      $(this).modal({
          overlay: "#000",        // Overlay color
          opacity: 0.75,          // Overlay opacity
          zIndex: 1,              // Overlay z-index.
          escapeClose: true,      // Allows the user to close the modal by pressing `ESC`
          clickClose: true,       // Allows the user to close the modal by clicking the overlay
          closeText: 'Close',     // Text content for the close <a> tag.
          closeClass: '',         // Add additional class(es) to the close <a> tag.
          showClose: true,        // Shows a (X) icon/link in the top-right corner
          modalClass: "modal",    // CSS class added to the element being displayed in the modal.
          spinnerHtml: null,      // HTML appended to the default spinner during AJAX requests.
          showSpinner: true,      // Enable/disable the default spinner during AJAX requests.
          fadeDuration: 250,     // Number of milliseconds the fade transition takes (null means no transition)
          fadeDelay: 1.50          // Point during the overlay's fade-in that the modal begins to fade in (.5 = 50%, 1.5 = 150%, etc.)
      });
      // $.get(this.href, function(html) {
      //   $(html).appendTo('body').modal();
      // });
    });

});