// Anula o navegador de fazer o preenchimento automático dos campos de todo o projeto
$("input, select, textarea").attr("autocomplete", "off");


// Define o formato padrão de datas
$('.vDateField').mask('00/00/0000');
// Define o formato padrão monetário
//$('.field-money').mask('000.000.000,00', {reverse: true});


// defini todos os links apontados para a página inicial do sistema para redirecionar para o dashboard customizado
// checa se a url aponta para a página inicial e se a página não é de logout da conta
$("a").each(function() { 
     var href = $(this).attr('href');

     if (href == "/" && !location.href.match("logout")) {
         $(this).attr('href', '/dashboard/');               
     }
 });


// Esconde mensagem de erro dos campos obrigatórios das inlines.
$('div.help-block').delay(4000).fadeOut(1000, function() {
    var $this = $(this);
    $this.has( "ul.errorlist" ).addClass('hidden-element');
});


// esconde a linha referente ao campo que possui a classe css .hidden-form-row
// utilizado por exemplo para esconder o campo de status_apoio renderizado no formulário de compra.
$(".hidden-form-row").each(function() { 
    $(this).parent( ".controls" ).parent( "div" ).parent( ".form-row" ).addClass( "hidden-element" );
});


// Bloqueia entradas de valores diferentes de números, bloqueando também ponto e traço
$(".vForeignKeyRawIdAdminField").numeric({ decimal: false, negative: false });

//
$(".vForeignKeyRawIdAdminField").change(function(){
    var valorID = $(this).val();
    if (valorID == 0 || valorID == ""){
        $(this).parent().find('.vForeignKeyRawIdAdminField').val("");
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
      fadeDuration: 250,      // Number of milliseconds the fade transition takes (null means no transition)
      fadeDelay: 1.50         // Point during the overlay's fade-in that the modal begins to fade in (.5 = 50%, 1.5 = 150%, etc.)
  });
});

var len = $('script').filter(function () {
    return($(this).attr('src') == '/static/js/jquery.modal.min.js');
}).length;

if (len != 0) {
    function modal_open_event(event, modal) {
      $('body').css('overflow', 'hidden');
    };
    function modal_close_event(event, modal) {
      $('body').css('overflow', 'auto');
    };
    $(document).on($.modal.BLOCK, modal_open_event);
    $(document).on($.modal.CLOSE, modal_close_event);
}