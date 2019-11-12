      $(document).ready(function() {
      let prova = $('#myForm').data('prova')
      let questao = $('#myForm').data('questao')
      let categoria = $('#myForm').data('categoria')
      if (prova) {
        $('#id_prova option[value='+prova+']').attr('selected', 'selected');
      }
      if (questao) {
        $('#id_questao option[value='+questao+']').attr('selected', 'selected');
      }
      if (categoria) {
        $('#id_categoria option[value='+categoria+']').attr('selected', 'selected');
      }
    });
    $("#id_prova,#id_questao,#id_categoria").on('change', function(){
       $('#btnSubmit').click();
    })




  $(document).ready(function() {
  var panels = $('.user-infos');
  var panelsButton = $('.dropdown-user');
  panels.hide();

  //Click dropdown
  panelsButton.click(function() {
    //get data-for attribute
    var dataFor = $(this).attr('data-for');
    var idFor = $(dataFor);

    //current button
    var currentButton = $(this);
    idFor.slideToggle(400, function() {
      //Completed slidetoggle
      if(idFor.is(':visible'))
      {
        currentButton.html('<i class="glyphicon glyphicon-chevron-up text-muted"></i>');
      }
      else
      {
        currentButton.html('<i class="glyphicon glyphicon-chevron-down text-muted"></i>');
      }
    })
  });
 });


  $(document).ready(function(){
   $("#register_form").submit(function(e){
       e.preventDefault();
       $("#nome-warning").hide();
       $("#email-warning").hide();
       $("#password-warning").hide();
       if(document.forms["register_form"]["nome"].value == '')
       {
           $("#nome-warning").show();
           return;
       }
       if(document.forms["register_form"]["email"].value=='')
       {
           $("#email-warning").show();
           return;
       }
       if(document.forms["register_form"]["password"].value=='')
       {
           $("#password-warning").show();
           return;
       }
       $.post("/quiz/create/",
           {
               nome : document.forms["register_form"]["nome"].value,
               email : document.forms["register_form"]["email"].value,
               password : document.forms["register_form"]["password"].value,
               csrfmiddlewaretoken :document.forms["register_form"]["csrfmiddlewaretoken"].value
           },
           function(data,status)
           {
               if (status == "success")
               {
                   $("#modal1").modal('hide');
                   $("#register-success").show();
               }
           }
       );
   });
   $("#login_form").submit(function(e){
      // alert("hello");
       e.preventDefault();
       $.post("/quiz/validate_login/",
           {
               usernome : document.forms["login_form"]["usernome"].value,
               password : document.forms["login_form"]["password"].value,
               csrfmiddlewaretoken : document.forms["login_form"]["csrfmiddlewaretoken"].value
           },
           function(data,status)
           {
                   window.location.href="/quiz/test";
           }
       );
   });
    $(".add_prova").click(function(){
       $(".glyphicon-plus").toggle();
        $(".glyphicon-arrow-down").toggle();
        $("#show-prova-form").slideToggle();
        });
    function add_questoes(prova_id,i)
    {
        $("#lista_questoes").hide();
        $("#add_questoes").show();
        $("#num-questao-btn").click(function(){
           $("#add_questoes").hide();
           $("#read-questoes").show();
            count = $("#questao-no").val();
            //alert(count);
                $("#questao-form").submit(function (e) {
                    e.preventDefault();
                    $("#icon-span").attr("class","glyphicon glyphicon-ok");
                    $.post("/quiz/add_questao/",
                        {
                            questao : document.forms["questao-form"]["IdQuestao"].value,
                            option1 : document.forms["questao-form"]["aOpcao"].value,
                            option2 : document.forms["questao-form"]["bOpcao"].value,
                            option3 : document.forms["questao-form"]["cOpcao"].value,
                            option4 : document.forms["questao-form"]["dOpcao"].value,
                            option5 : document.forms["questao-form"]["eOpcao"].value,
                            resposta : document.forms["questao-form"]["respostaQuestao"].value,
                            prova : prova_idProva,
                            csrfmiddlewaretoken : document.forms["questao-form"]["csrfmiddlewaretoken"].value
                        },
                        function(data,success)
                        {
                            document.forms["questao-form"]["questao"].value = "";
                            document.forms["questao-form"]["option1"].value = "";
                            document.forms["questao-form"]["option2"].value = "";
                            document.forms["questao-form"]["option3"].value = "";
                            document.forms["questao-form"]["option4"].value = "";
                            document.forms["questao-form"]["answer"].value = "";
                            $("#icon-span").attr("class","glyphicon glyphicon-forward");
                        }
                    );
                    i++;
                    if(i>=count) {
                        $("#read-questoes").hide();
                        window.location.reload();
                    }
                });
        });
    }
    $("#prova-form").submit(function(e){
           // alert("helo");
           e.preventDefault();
           $.post("/add_prova/",
               {
                   prova_nome : document.forms["prova-form"]["prova_nome"].value,
                   user : document.forms["prova-form"]["user"].value,
                   csrfmiddlewaretoken :document.forms["prova-form"]["csrfmiddlewaretoken"].value
               },
               function(data,status)
               {
                   //alert(data);
                    $("#lista_questoes").append(template(document.forms["prova-form"]["user"].value,document.forms["prova-form"]["prova_nome"].value));
                   $(".add_prova").click();
                   document.forms["prova-form"]["prova_nome"].value = "";
                   add_questoes(data,0);
               }
           );
    });
    function show_result(count,total)
    {
        $("#count").text(count);
        $("#total").text(total);
        $("#score").slideDown();
    }
    $(".exit-btn").click(function(){
        window.location.reload();
    });
    function test(data,count)
    {
        j = 1;
        $(".select-option").click(function(){
      $(".glyphicon-ok").attr("class","glyphicon glyphicon-unchecked col-sm-offset-1");
      $(this).find(".glyphicon").attr("class","glyphicon glyphicon-ok col-sm-offset-1");
            $("#option-answer").val($(this).find(".option").text());
    });
        $("#verify").click(function(){
           $(".before").hide();
            $(".after").show();
            if($("#option-answer").val() == data[j-1].answer)
            {
                $(".after-ok").show();
            }
            else{
                $(".after-not-ok").show();
            }
        });
        $("#after").click(function(){
            if($("#option-answer").val() == data[j-1].answer)
                count++;
            if(j >= data.length)
            {
                $(".after").hide();
                $(".after-ok").hide();
                $(".after-not-ok").hide();
                $(".glyphicon-ok").attr("class","glyphicon glyphicon-unchecked col-sm-offset-1");
            $   (".before").show();
                $("#questao-display").hide();
                show_result(count,data.length);
                return;
            }
            $(".questao-place").html(data[j].idQuestao);
            $(".option1-place").html(data[j].aOpcao);
            $(".option2-place").html(data[j].bOpcao);
            $(".option3-place").html(data[j].cOpcao);
            $(".option4-place").html(data[j].dOpcao);
            $(".option5-place").html(data[j].eOpcao);
            $(".after").hide();
            $(".after-ok").hide();
            $(".after-not-ok").hide();
            $(".glyphicon-ok").attr("class","glyphicon glyphicon-unchecked col-sm-offset-1");
            $(".before").show();
            j++;
        });
    }
    $("#lista_questoes").on('click','.prova-panel',function(){
            $("#lista_questoes").hide();
            prova_idProva = $(this).find(".prova_template").attr('idProva');
            $.get("/api/questao/",function(data,status){
                var i;
               // alert("hello");
                data2 = [];
               for(i=0;i<data.length;i++)
               {
                   if(data[i].prova == prova_idProva)
                   {
                       //console.log(data[i].prova+' '+prova_id);
                       data2.push(data[i]);
                   }
               }
                i=0;
                //alert(data);
                data = data2;
                //console.log(data.length);
                if (data.length == 0 ) {
                    $("#no-questoes").show();
                    return;
                }
                $("#questao-display").show();
                //alert(questoes);
                $(".questao-place").html(data[i].idQuestao);
                $(".option1-place").html(data[i].aOpcao);
                $(".option2-place").html(data[i].bOpcao);
                $(".option3-place").html(data[i].cOpcao);
                $(".option4-place").html(data[i].dOpcao);
                $(".option4-place").html(data[i].eOpcao);
                test(data,0);
            });
          });
    });


