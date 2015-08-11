    // $( "#up-tour-1-link" ).click(function(e) {
    //     url_fim = window.location.href;
    // });

    var url = window.location.protocol + '//' + window.location.host;

    // Define o tour
    var tour = {
      id: "tour-guiado",
      // showPrevButton: true,
      // showSkip: true,
      steps: [
        {
          title: "Tour Guiado",
          content: "Seja bem-vindo ao tour guiado. Neste tour você será apresentado às principais características deste sistema.",
          target: "#up-tour-1-link",
          placement: "bottom",
          multipage: true,
          onNext: function() {
            window.location = url
          }
        },
        {
          title: "Menu de navegação",
          content: "Ao lado esquerdo da página, haverá sempre o menu de navegação do sistema. O mesmo exibirá todas as páginas na qual o usuário autenticado possui permissão para acesso.",
          target: "left-nav",
          placement: "right",
          multipage: true,
          onNext: function() {
            window.location = url + '/pessoal/cliente/'
          }
        },
        {
          title: "Listagens",
          content: "Acessando.",
          target: "#suit-center .breadcrumb .active",
          placement: "bottom"
        },
        {
          title: "Filtros",
          content: "Filtros de pesquisa",
          target: "#changelist .xfull",
          placement: "bottom"
        },
        {
          title: "Ordenação dos registros",
          content: "Alterando a ordem dos resultados na listagem (É possível aplicar a ordenação com multiplas campos).",
          target: "#result_list .column-nome a",
          placement: "top"
        },
        {
          title: "Exportar os dados",
          content: "Há possibilidade de exportar pelos dados nas listagens em que o botão 'Exportar' é exibido na página.<br>Os dados a serem exportados poderão ser filtrados como explicado anteriormente. Diante disso, surgirão somente os registros selecionados de acordo com o desejo do usuário.",
          target: "#changelist .object-tools #export-data",
          placement: "left",
          yOffset: -17,
          multipage: true,
          onNext: function() {
            window.location = url + '/pessoal/cliente/export/?'
          }
        },
        {
          title: "Opções de exportação",
          content: "Lista de opções.<br>Por fim, basta clicar no botão 'Enviar', ao lado, para iniciar o download do arquivo.",
          target: "#id_file_format",
          placement: "bottom",
          multipage: true,
          onNext: function() {
            window.location = url + '/pessoal/cliente/'
          }
        },
        {
          title: "Ver/Editar registros",
          content: "De volta a listagem.",
          target: "#changelist-form #result_list tbody tr:nth-child(1) th",
          placement: "right",
          xOffset: -40,
          yOffset: -17,
          multipage: true,
          onNext: function() {
            window.location = document.querySelector("#changelist-form #result_list tbody tr:nth-child(1) th a").href
          }
        },
        {
          title: "Dados obrigatórios",
          content: "Os dados obrigatórios nos formulários do sistema aparecem com o asterisco ao lado do rótulo.",
          target: "#content-main fieldset .control-label .required:nth-child(1)",
          placement: "right",
          xOffset: 10,
          yOffset: -26
        },
        {
          title: "Log de alterações",
          content: "Presente em todos os formulários do sistema.<br>Visualize o histórico de alterações do cadastro. Veja a data de modificação, os dados alterados e o(s) usuário(s) que realizaram tais alterações.",
          target: "ul li .historylink",
          placement: "left",
          yOffset: -15
          // fixedElement: true
        },
        {
          title: "Suporte",
          content: "Para dúvidas, necessidades de mudanças ou melhorias, contate o suporte.",
          target: "#link-suport",
          placement: "top"
        },
        {
          title: "Problemas",
          content: "Encontrou algum erro? Relate a falha para que a correção seja implementada.",
          target: "#link-issue",
          placement: "top"
        },
        {
          title: "Fim do Tour",
          content: "Parabéns! Você concluiu o tour guiado. Fique a vontade para explorar as outras telas e recursos, e lembre-se que sempre que precisar de ajuda você será bem-vindo e estaremos a sua disposição.",
          target: document.querySelector("#up-tour-1-link"),
          placement: "bottom"
        }
      ]
    };

    // Executa automaticamente o tour se a página tiver sido chamada pelo tour da página anterior
    if (hopscotch.getState() === "tour-guiado:1" || hopscotch.getState() === "tour-guiado:2" || hopscotch.getState() === "tour-guiado:6" || hopscotch.getState() === "tour-guiado:7" || hopscotch.getState() === "tour-guiado:8") {
      hopscotch.startTour(tour);
    }

    // Inícia o tour
    $( "#up-tour-1-link" ).click(function(e) {
      e.preventDefault();
      hopscotch.startTour(tour);
    });

    // Configuração do tour
    hopscotch.configure({
      i18n:{
        stepNums: ["1", "2", "3"],
        nextBtn: 'Próximo',
        prevBtn: 'Anterior',
        doneBtn: 'Terminar',
        skipBtn: 'Pular',
        closeTooltip: 'Fechar'
      }
    });