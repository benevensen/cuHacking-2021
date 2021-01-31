function handleButtonClicks() {
    $(".category-button").click(function() {
        $(this ).css('background', 'tomato');
        $(this).siblings().css('background', 'rgba(19, 19, 19, 0.76)')
    });
}

function handleSubmissions() {
    $("main").on("submit", "form", function( event ){
        event.preventDefault();
    });
}


$(function() {
    handleButtonClicks();
    handleSubmissions();
});