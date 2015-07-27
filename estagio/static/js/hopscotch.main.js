    var url = window.location.protocol + '//' + window.location.host;

    // Define o tour
    var tour = {
      id: "tour-guiado",
      // showPrevButton: true,
      // showSkip: true,
      steps: [
        {
          title: "Tour Guiado",
          content: "Seja bem-vindo ao tour guiado. Neste tour você será apresentado aos principais recursos do sistema que irá utilizar.",
          target: "#up-tour-link",
          placement: "bottom",
          multipage: true,
          onNext: function() {
            window.location = url
          }
        },
        {
          title: "Menu de navegação",
          content: "This is the header of my page.",
          target: "left-nav",
          placement: "right"
        },
        {
          title: "Fim do Tour",
          content: "Parabéns! Você concluiu o tour guiado. Fique a vontade para explorar as outras telas e recursos, e lembre-se que sempre que precisar de ajuda você será bem-vindo e estaremos a sua disposição.",
          target: document.querySelector("#up-tour-link"),
          placement: "bottom"
        }
      ]
    };

    // Executa automaticamente o tour se a página tiver sido chamada pelo tour da página anterior
    if (hopscotch.getState() === "tour-guiado:1") {
      hopscotch.startTour(tour);
    }

    // Inícia o tour
    $( "#up-tour-link" ).click(function(e) {
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