});


$(function ()
{
  $("#qSelect option").hide();
  $("#pSelect").on("change", function ()
  {
    let prova = $("#pSelect").val();
    $("#qSelect option").hide();
    $("#qSelect option[data-course="+ questao.idProva +"]").show();
  });
});


$(document).ready(function(){
    $("button").click(function(){
        $("#select").confirm();

    });
});

$(document).ready(function()
{
	$('select#selectcountries').change(function ()
	{
		var optionSelected = $(this).find("option:selected");
		var valueSelected  = optionSelected.val();
		var prova_nome   = optionSelected.text();
		data = {'pn' : prova_nome };
		ajax('/getdetails',data,function(result)
		{
			console.log(result);
			$("#selectquestoes option").remove();
			for (var i = result.length - 1; i >= 0; i--)
			{
				$("#selectquestoes").append('<option>'+ result[i].textoQuestao +'</option>');
			};
		});
	});
});

$("#id_city").chained("#id_country");

$(function()
{
	var questao = $('select[name=questao]');
	questao.empty();
	questao.prepend('<option value="Not selected" selected disabled>Selecione a questão</option>');
	$('select[name=prova]').change(function(){
	if($("#idProva option:selected").text() != ("Você precisa inserir uma prova")) {
	var prova_id = $('select[name=setor]').val();

	request_url = '/index.html/' + prova_id + '/';
	$.ajax({
	url: request_url,
	type: "GET",
	success: function(data){
	questao.empty();
	$.each(data, function(key, value){
	questao.append('<option value="' + key + '">' + value + '</option>');
                        });
                    }
                })
            }
        })
    });
