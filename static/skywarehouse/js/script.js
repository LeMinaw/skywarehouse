$(document).ready(function() {
    $('select').material_select();

    $('.parallax').parallax();

    $('.collapsible').collapsible();
    
    $('.tooltipped').tooltip({delay: 50});
    
    $('#sort_form select').on("change", function() {
        $('#sort_form').submit();
    });
    
});

$(window).on('load', function() {
    $('ul.tabs').tabs({swipeable: true});

    sticky($('#navbar'), $('#placeholder'));
});

function sticky(element, placeholder) {
    let initialPlaceHolder = placeholder.height();
    var initialPos = element.offset().top,
        wasMoved = false;

    $(window).scroll(function() {
        if ($(this).scrollTop() > initialPos) {
            element.addClass('ontop');
            if (!wasMoved) { // preventing refresh of placeholder height
                placeholder.css('height', initialPlaceHolder + element.height() + 20 + 'px'); // TODO: True margin detection
                wasMoved = !wasMoved;
            }
        } else {
            element.removeClass('ontop');
            if (wasMoved) {
                placeholder.css('height', initialPlaceHolder + 'px');
                wasMoved = !wasMoved;
            }
        }
    });
}
