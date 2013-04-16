/*global $, jQuery, document*/

$(document).ready(function () {
    "use strict";
    $("#mozillians").tablesorter({sortList: [[1, 0], [0, 0]] });

    $('#filter-voted').click(function () {
        $('#filter-voted').addClass("badge-info");
        $('#filter-not-voted').removeClass("badge-info");
        $('#filter-all').removeClass("badge-info");
        $("tbody tr").each(function(){
            if($(this).find("td").is(":empty"))
                $(this).hide();
        });
        $("tbody tr").each(function(){
            if(!$(this).find("td").is(":empty"))
                $(this).show();
        });
    });

    $('#filter-not-voted').click(function () {
        $('#filter-not-voted').addClass("badge-info");
        $('#filter-voted').removeClass("badge-info");
        $('#filter-all').removeClass("badge-info");
        $("tbody tr").each(function(){
            if($(this).find("td").is(":empty"))
                $(this).show();
        });
        $("tbody tr").each(function(){
            if(!$(this).find("td").is(":empty"))
                $(this).hide();
        });
    });

    $('#filter-all').click(function () {
        $('#filter-all').addClass("badge-info");
        $('#filter-not-voted').removeClass("badge-info");
        $('#filter-voted').removeClass("badge-info");
        $("tbody tr").each(function(){
            $(this).show();
        });
    });
});
