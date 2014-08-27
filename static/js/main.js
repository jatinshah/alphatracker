$(document).ready(function(){
    $("#fieldURL").hide();
    $("#selectArticle").click(function(){
        if($(this).is(':checked')){
            $("#fieldURL").hide();
            $("#fieldText").show();
        }
    });
    $("#selectLink").click(function(){
        if($(this).is(':checked')){
            $("#fieldURL").show();
            $("#fieldText").hide();
        }
    });
})

$("[name='rating-toggle']").bootstrapSwitch();
