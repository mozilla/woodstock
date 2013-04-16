/*global $, jQuery, document*/

$(document).ready(function () {
    "use strict";
    $('.bar').tooltip();
    $("#mozillians").tablesorter({sortList: [[1, 0], [0, 0]] });

    $('#filter-voted').click(function () {
        $('#filter-voted').addClass("badge-info");
        $('#filter-not-voted').removeClass("badge-info");
        $('#filter-all').removeClass("badge-info");
        $("tbody tr").each(function () {
            if ($(this).find("td").is(":empty")) {
                $(this).hide();
            }
        });
        $("tbody tr").each(function () {
            if (!$(this).find("td").is(":empty")) {
                $(this).show();
            }
        });
    });

    $('#filter-not-voted').click(function () {
        $('#filter-not-voted').addClass("badge-info");
        $('#filter-voted').removeClass("badge-info");
        $('#filter-all').removeClass("badge-info");
        $("tbody tr").each(function () {
            if ($(this).find("td").is(":empty")) {
                $(this).show();
            }
        });
        $("tbody tr").each(function () {
            if (!$(this).find("td").is(":empty")) {
                $(this).hide();
            }
        });
    });

    $('#filter-all').click(function () {
        $('#filter-all').addClass("badge-info");
        $('#filter-not-voted').removeClass("badge-info");
        $('#filter-voted').removeClass("badge-info");
        $("tbody tr").each(function () {
            $(this).show();
        });
    });

    if ($('#status-total').html() < 10) {
        $('#status-msg').append('it will be quick, we promise!');
    } else if ($('#status-total').html() < 50) {
        $('#status-msg').append('you are doing great! Grab a coffee.');
    } else if ($('#status-total').html() < 70) {
        $('#status-msg').append('you have less than half left!');
    } else if ($('#status-total').html() < 90) {
        $('#status-msg').append('you are doing great!');
    } else if ($('#status-total').html() < 100) {
        $('#status-msg').append('you are almost there!');
    } else if ($('#status-total').html() == 100) {
        $('#status-msg').append('you are done! Awesome!');
    }
});
