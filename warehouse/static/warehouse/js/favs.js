$(".fav").click(function(event) {
    event.preventDefault();

    var elem = $(this);
    var url = elem.attr('href');

    $.ajax({
        url: url,
        dataType: 'json',
        success: function(data) {
            if (data.now_fav) {
                elem.html('<i class="material-icons">favorite</i>');
            } else {
                elem.html('<i class="material-icons">favorite_border</i>');
            }
        }
    });

});


