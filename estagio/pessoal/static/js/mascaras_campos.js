//$('#id_telefone').mask("(00) 00009-0000");

$(document).ready(function(){
    $('#id_data_nasc').mask('00/00/0000');
    //$('.time').mask('00:00:00');
    //$('.date_time').mask('00/00/0000 00:00:00');
    $('#id_cep').mask('00000-000');
    //$('.phone').mask('0000-0000');
    $('#id_telefone').mask('(00) 00009-0000');
    $('#id_celular').mask('(00) 00009-0000');
    //$('.mixed').mask('AAA 000-S0S');
    //$('#id_cpf').mask('000.000.000-00', {reverse: true});
    //$('.money').mask('000.000.000.000.000,00', {reverse: true});


/*  
    // Outro código para criar a máscara do telefone 
    var masks = ['(00) 00000-0000', '(00) 0000-00009'],
        maskBehavior = function(val, e, field, options) {
        return val.length > 14 ? masks[0] : masks[1];
    };

    $('#id_telefone').mask(maskBehavior, {onKeyPress: 
       function(val, e, field, options) {
           field.mask(maskBehavior(val, e, field, options), options);
       }
    });

*/
/*
    // Outro código para criar a máscara do telefone 
    var masks = ['(00) 00000-0000', '(00) 0000-00009'];
    $('#id_telefone').mask(masks[1], {onKeyPress: 
       function(val, e, field, options) {
           field.mask(val.length > 14 ? masks[0] : masks[1], options) ;
       }
    });

*/
});