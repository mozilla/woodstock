$(document).ready(function () {
    'use strict';

    $('#blind-info').tooltip();

    function generate_link() {
        var events = [];
        $('input:checkbox:checked').each(function(){
            events.push($(this).val());
        });
        var blind = $('input:radio:checked').val();

        $('#events-submit').attr('href', '/dashboard/?events=' + events + '&blind=' + blind);
        $('#events-submit').removeClass('disabled');

        if ($.isEmptyObject(events)) {
            $('#events-submit').attr('href', '#');
            $('#events-submit').addClass('disabled');
        }
    }

    $('input').change(function() {
        generate_link();
    });

    generate_link();
});
