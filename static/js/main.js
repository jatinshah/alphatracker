/*jslint browser: true*/
/*global $, jQuery, alert, console */
function getCookie(name) {
    "use strict";
    var cookieValue, cookies, i, cookie;
    cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        cookies = document.cookie.split(';');
        for (i = 0; i < cookies.length; i++) {
            cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    "use strict";
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    "use strict";
    var host = document.location.host, // host + port
        protocol = document.location.protocol,
        sr_origin = '//' + host,
        origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url === origin || url.slice(0, origin.length + 1) === origin + '/') ||
        (url === sr_origin || url.slice(0, sr_origin.length + 1) === sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        "use strict";
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
        var this_elem, other_elem, score_elem, score_count, slug, vote;
        evt.preventDefault();
        this_elem = $(this);
        score_elem = $(this).closest('.voting-block').find('.score');
        score_count = Number(score_elem.text());
        slug = $(this).closest('.post-item').find('.post-slug').text().trim();

        if ($(evt.target).hasClass('p-vote-up')) {
            other_elem = $(this).closest('.voting-block').find('.p-vote-down');
            score_count = updateScore($(this), other_elem, score_count, 1);
            vote = '1';
        } else {
            other_elem = $(this).closest('.voting-block').find('.p-vote-up');
            score_count = updateScore($(this), other_elem, score_count, -1);
            vote = '-1';
        }
        $.post('/c/vote/', {vote: vote, slug: slug},
               function(data) { if (data.success) {
            score_elem.html(score_count.toString());
            toggleVote(this_elem, other_elem);
        }
                              }
              );
    });

    // Follow/Unfollow implementation
    function toggleFollow(button_elem) {
        var button_text = button_elem.text().trim();
        if(button_text === 'Following') {
            button_elem.html('Unfollow');
            button_elem.toggleClass('btn-primary');
            button_elem.toggleClass('btn-danger');
        } else if (button_text === 'Unfollow') {
            button_elem.html('Following');
            button_elem.toggleClass('btn-danger');
            button_elem.toggleClass('btn-primary');
        }
    }

    var recent_button_click = false;
    $('body').on('mouseenter', '.following', function(){
        if(!recent_button_click) {
            var button_elem = $(this);
            toggleFollow(button_elem);
        }
    });
    $('body').on('mouseleave', '.following', function(){
        if(recent_button_click) {
            recent_button_click = false;
            return;
        }
        var button_elem = $(this);
        toggleFollow(button_elem);
    });

    $('#follow-button').click(function() {
        recent_button_click = true;
        var following_username = $(this).attr('username');
        var button_elem = $(this);
        button_elem.unbind('mouseenter mouseleave');
        $.post('/u/follow/', {following_username: following_username},
               function(data) {
            console.log(data);
            if(data.success) {
                if(data.following) {
                    button_elem.html('Following');
                    button_elem.removeClass();
                    button_elem.addClass('btn btn-primary following');
                }else {
                    button_elem.html('Follow');
                    button_elem.removeClass();
                    button_elem.addClass('btn btn-default');
                }
                // Change button text & button type
                // POST returns current state
            }
        })

    });
});

// Stock Symbol typeahead in Submit form
var stocks = new Bloodhound({
    datumTokenizer: function(data) {
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