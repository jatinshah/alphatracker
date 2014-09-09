/*jslint browser: true*/
/*global $, jQuery, alert*/
function getCookie(name) {
    "use strict";
    var cookieValue, cookies;
    cookieValue = null;
    if (document.cookie && document.cookie != '') {
        cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).ready(function() {
    "use strict";
    // Counter for editing Bio in user profile
    if ($('#counter').length) {
        $("#counter").append($("#bio").val().length + "/160");
    }
    $("#bio").keyup(function() {
        if ($(this).val().length > 160) {
            $(this).val($(this).val().substr(0, 160));
        }
        var text_length = $(this).val().length;
        $("#counter").html(text_length + "/160");
        if (text_length > 150) {
            $("#counter").css("color", "red");
        } else {
            $("#counter").css("color", "black");
        }
    });

    // Voting up & down
    function toggleVote(this_elem, other_elem) {
        this_elem.toggleClass('text-muted');
        this_elem.toggleClass('text-primary');

        if (other_elem.hasClass('text-primary')) {
            other_elem.toggleClass('text-primary');
            other_elem.toggleClass('text-muted');
        }
    }
    function updateScore(this_elem, other_elem, score, vote) {
        if (this_elem.hasClass('text-primary')) {
            score = score - vote;
        } else if (other_elem.hasClass('text-primary')) {
            score = score + 2 * vote;
        } else if (other_elem.hasClass('text-muted')) {
            score = score + vote;
        }
        return score;
    }

    $("[class*='p-vote-']").click(function(evt) {
        var _this, _other, _score, score_count, slug, vote;
        evt.preventDefault();
        _this = $(this);
        _score = $(this).closest('.voting-block').find('.score');
        score_count = Number(_score.text());
        slug = $(this).closest('.post-item').find('.post-slug').text().trim();

        if ($(evt.target).hasClass('p-vote-up')) {
            _other = $(this).closest('.voting-block').find('.p-vote-down');
            score_count = updateScore($(this), _other, score_count, 1);
            vote = '1';
        } else {
            _other = $(this).closest('.voting-block').find('.p-vote-up');
            score_count = updateScore($(this), _other, score_count, -1);
            vote = '-1';
        }
        $.post('/c/vote/', {vote: vote, slug: slug},
               function(data){ if(data['success']) {
                                    _score.html(score_count.toString());
                                    toggleVote(_this, _other);
                                }
                }
              )
    });
});

// Stock Symbol typeahead in Submit form
var stocks = new Bloodhound({
    datumTokenizer: function (data) {
        "use strict";
        var stock_name, stock_symbol;
        stock_name = Bloodhound.tokenizers.whitespace(data.name);
        stock_symbol = Bloodhound.tokenizers.whitespace(data.symbol);
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
    }
);