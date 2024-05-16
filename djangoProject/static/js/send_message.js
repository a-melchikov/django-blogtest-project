$(document).ready(function() {
    var recipient = getUrlParameter('recipient');
    $('#recipient').val(recipient);
});

function getUrlParameter(name) {
    name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
    var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
    var results = regex.exec(location.search);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
}

$(document).ready(function() {
    var suggestions = [];

    $('#recipient').on('input', function() {
        var input = $(this).val();
        if (input.length > 0) {
            $.ajax({
                url: '/get_user_suggestions/',
                type: 'GET',
                data: { 'input_text': input },
                success: function(response) {
                    suggestions = response;
                    displaySuggestions(response);
                },
                error: function(xhr, errmsg, err) {
                    console.log(xhr.status + ": " + xhr.responseText);
                }
            });
        } else {
            $('#recipient-suggestions').hide();
        }
    });

    $('#recipient').focus(function() {
        var input = $(this).val();
        if (input.length > 0) {
            $('#recipient-suggestions').show();
        }
    });

    $('#recipient').blur(function() {
        $('#recipient-suggestions').hide();
    });

    $(document).on('click', '#recipient-suggestions li', function() {
        var selectedName = $(this).text();
        $('#recipient').val(selectedName);
        $('#recipient-suggestions').hide();
    });

    $('form').submit(function(event) {
        var enteredName = $('#recipient').val();
        if (suggestions.indexOf(enteredName) === -1) {
            event.preventDefault();
            alert('Введите существующее имя из списка подсказок.');
        }
    });

    function displaySuggestions(suggestions) {
        $('#recipient-suggestions').empty();
        if (suggestions.length > 0) {
            var list = $('<ul></ul>');
            $.each(suggestions, function(index, suggestion) {
                list.append($('<li></li>').text(suggestion));
            });
            $('#recipient-suggestions').append(list);
            $('#recipient-suggestions').show();
        } else {
            $('#recipient-suggestions').hide();
        }
    }
});