// Anula o navegador de fazer o preenchimento automático dos campos de todo o projeto
$("input, select, textarea").attr("autocomplete", "off");


// Defina o formato padrão de datas
$('.vDateField').mask('00/00/0000');


// defini todos os links apontados para a página inicial do sistema para redirecionar para o dashboard customizado 
$("a").each(function() { 
     var href = $(this).attr('href');

     if (href == "/" && !location.href.match("logout")) {   // checa se a url aponta para a página inicial e se a página não é de logout da conta
         $(this).attr('href', '/dashboard/');               
     }
 });


// Bloqueia entradas de valores diferentes de números, bloqueando também ponto e traço
$(".vForeignKeyRawIdAdminField").numeric({ decimal: false, negative: false });

//
$(".vForeignKeyRawIdAdminField").change(function(){
    var valorID = $(this).val();
    if (valorID == 0 || valorID == ""){
        $(this).parent().find('input').val("");
        $(this).parent().find(".salmonella_label").empty();
    }
});


// Define todos os campos do tipo file com a classe .filestyle, e passa as definições para estes campos
$('input[type=file]').addClass('filestyle');
$(":file").filestyle({input: false, buttonText: "Enviar arquivo"});


// Definições da abertura e comportamento dos modais abertos no sistema.
$('.modal-main-custom').click(function(event) {
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