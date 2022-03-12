$(document).ready(function(){
    $("#click-to-top").on("click","a", function(event) {
        event.preventDefault();
    var top = $('#to-top').offset().top;

        $('body,html').animate({scrollTop: top}, 800);
    });
});
