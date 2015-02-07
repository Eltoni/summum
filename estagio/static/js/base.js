// Anula o navegador de fazer o preenchimento automático dos campos de todo o projeto
$("input, select, textarea").attr("autocomplete", "off");


// defini todos os links apontados para a página inicial do sistema para redirecionar para o dashboard customizado 
$("a").each(function() { 
     var href = $(this).attr('href');

     if (href == "/" && !location.href.match("logout")) {   // checa se a url aponta para a página inicial e se a página não é de logout da conta
         $(this).attr('href', '/dashboard/');               
     }
 });