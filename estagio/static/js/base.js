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