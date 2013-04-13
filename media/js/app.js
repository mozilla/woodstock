$(document).ready(function() {
    $("#mozillians").tablesorter();
    $('#shortcuts').tooltip();

    if ($('input[value="-1"]').is(':checked')) {
        $('#button-no').addClass('disabled');
    } else if ($('input[value="0"]').is(':checked')) {
        $('#button-skip').addClass('disabled');
    } else if ($('input[value="1"]').is(':checked')) {
        $('#button-probably').addClass('disabled');
    } else if ($('input[value="2"]').is(':checked')) {
        $('#button-definitely').addClass('disabled');
    }

    $('#button-no').click(function() {
        $('input[value="-1"]').attr('checked', true);
        $('#voting_form').submit();
    });
    $('#button-skip').click(function() {
        $('input[value="0"]').attr('checked', true);
        $('#voting_form').submit();
    });
    $('#button-probably').click(function() {
        $('input[value="1"]').attr('checked', true);
        $('#voting_form').submit();
    });
    $('#button-definitely').click(function() {
        $('input[value="2"]').attr('checked', true);
        $('#voting_form').submit();
    });

    $(document).keydown( function(event) {
        if (event.which == 88){
            $('input[value="-1"]').attr('checked', true);
            $('#voting_form').submit();
        } else if (event.which == 48){
            $('input[value="0"]').attr('checked', true);
            $('#voting_form').submit();
        } else if (event.which == 49){
            $('input[value="1"]').attr('checked', true);
            $('#voting_form').submit();
        } else if (event.which == 50){
            $('input[value="2"]').attr('checked', true);
            $('#voting_form').submit();
        }
    });
});
