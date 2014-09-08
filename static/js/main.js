$(document).ready(function() {
    $("#counter").append($("#bio").val().length + "/160");
    $("#bio").keyup(function(){
        if($(this).val().length > 160){
            $(this).val($(this).val().substr(0,160));
        }
        var text_length = $(this).val().length;
        $("#counter").html(text_length + "/160");
        if(text_length > 150) {
            $("#counter").css("color", "red");
        }
        else {
            $("#counter").css("color", "black");
        }
    });
});

var stocks = new Bloodhound({
    datumTokenizer: function (data) {
        var stock_name = Bloodhound.tokenizers.whitespace(data.name);
        var stock_symbol = Bloodhound.tokenizers.whitespace(data.symbol);
        return stock_symbol.concat(stock_name);
    },
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    prefetch: {
        url: '/r/stocks/'
    },
    limit: 10
});


stocks.initialize();

$('#stock-symbol .typeahead').typeahead(
    {
        hint: true,
        highlight: true,
        minLength: 1
    },
    {
        name: 'stocks',
        displayKey: 'symbol',
        source: stocks.ttAdapter(),
        templates: {
            suggestion: Handlebars.compile('<p>{{symbol}} - {{name}}</p>')
        }
    });