 $('#selProva').click(function(e) { 

        e.preventDefault();
        cep = $('#listarProvas').val();
        $.ajax({
            type:'POST',
            url: "{% url 'detalhes' %}",
            dataType: "json",
            data: {
                data:cep,
                csrfmiddlewaretoken:'{{csrf_token}}',
            },        
            success: function(retorno){
                $.each(retorno, function(i, item) {
                console.log(i);
                console.log(item);
                console.log("TEST");
                alert("TEST");
                $("#exibeProva").append(i, item);
                });                
            },
            error: function(jqXHR, textStatus, errorThrown){
                //alert("FALHOU");
                console.log('Error');
                console.log(jqXHR);
                console.log(textStatus);
                console.log(errorThrown);
            },
        });

});