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