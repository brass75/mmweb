function submitGuess(){
    var url='play.html/' + game_id + '/' +  $("#guess").val()

    var jqxhr = $.getJSON(url, function(response) {
            switch(response.status) {
                case 'win':
                    $("#status").text("CONGRATULATIONS! You won!");
                    break;
                case 'lose':
                    $("#status").text("Sorry! You couldn't guess my number. It was " + response.secret +".");
                    break;
                case 'error':
                    $("#status").text(response.message + " You have " + response.guesses + " remaining.");
                    break;
                default:
                    $("#status").text("You have " + response.guesses + " guesses remaining.");
                    break;
            }
            if (response.status != "error") {
                $('#history > tbody:last-child').append(response.hint);
                if (response.status != "continue") {
                    $("#div_play_game").hide()
                    $("#div_new_game").show()
                }
            }
        })  
        .fail(function() {
            console.log( "Unable to process guess!" );
            $("#status").text(" There appears to be a problem.<br>" + $("#status").text())
        });
}