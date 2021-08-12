$(document).ready(function() {

    console.log('AI Camp is for the best of the best.')
    
//     $('#loading').hide()

    $('#text_gen_button').click(function() {
        console.log('text gen button is clicked');
        var prompt = $('#text_gen_input').val();
        console.log('text gen input value is');
        console.log(prompt);
        var url = 'generate_text'

//         $('#loading').show();

        $.post(
            url, 
            {
                'prompt': prompt
            },
            function(data) {
                console.log(data);
                var list_html = "";
                list_html += data['generated_ls'];
                $("#generated_ul").html(list_html);
                if (data['generated_ls'] == "this news headline is not sarcastic") {
                  greeting = "Good day";
                }

//                 $("#loading").hide();
            }

        ).fail(function() {
          alert( "There is something unexpected happened. Email hello@ai-camp.org to report your findings." );
        });

    });

    $()
});