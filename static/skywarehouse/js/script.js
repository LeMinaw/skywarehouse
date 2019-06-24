$(document).ready(function() {
    $('select').formSelect();

    $('.parallax').parallax();

    $('.collapsible').collapsible();
    
    $('.tooltipped').tooltip({delay: 50});

    $('.materialboxed').materialbox();

    $('#sort_form select').on("change", function() {
        $('#sort_form').submit();
    });
});

$(window).on('load', function() {
    $('ul.tabs').tabs({ swipeable: true, onShow: resizeTab });
    
    sticky($('#navbar'), $('#placeholder'));
});

function resizeTab() {
    $('.tabs-content').css('height', $('.carousel-item.active .row').height() + 'px');
}

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
