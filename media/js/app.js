/*global $, jQuery, document*/

function check_submit(v) {
    "use strict";
    $('input[value=' + v + ']').attr('checked', true);
    $('#voting_form').submit();
}

$(document).ready(function () {
    "use strict";
    $("#mozillians").tablesorter({sortList: [[1, 0], [0, 0]] });
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

    $('#button-no').click(function () {check_submit("-1"); });
    $('#button-skip').click(function () {check_submit("0"); });
    $('#button-probably').click(function () {check_submit("1"); });
    $('#button-definitely').click(function () {check_submit("2"); });

    $(document).keydown(function (event) {
        if (event.which === 88) {
            check_submit("-1");
        } else if (event.which === 48) {
            check_submit("0");
        } else if (event.which === 49) {
            check_submit("1");
        } else if (event.which === 50) {
            check_submit("2");
        }
    });
});
