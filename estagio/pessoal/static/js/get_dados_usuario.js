$(document).ready(function(){

    function LimpaCampos(){
        $("input[name=nome], input[name=email]").val("");
    }

    /*-------------------------------------------------------------------------------------------------------------------------------
    Busca os dados de acordo com o usuário informado
    -------------------------------------------------------------------------------------------------------------------------------*/
    var valorUnitario;
    var id;

    $("#id_usuario").change(function(){
        id = $("#id_usuario").val();
        if (id) {
            $.ajax({       
            type: "GET",
            url: "/get_dados_usuario/"+id,
            dataType: "json",
            success: function(retorno){
                $.each(retorno, function(i, usuario){
                    var nome = usuario.fields['first_name'];
                    var sobrenome = usuario.fields['last_name'];
                    var email = usuario.fields['email'];
                    $('input[name="nome"]').val(nome + " " + sobrenome);
                    $('input[name="email"]').val(email);
                    });
                }
            }); 

        } else {
            LimpaCampos();
        };       
    });

});