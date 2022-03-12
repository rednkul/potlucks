$(function() {
 let header = $('.header');
 let headerHeight = header.height(); // вычисляем высоту шапки
 let id_header = $('#header');
 let top_header = $('#top-header');


 $(window).scroll(function() {
   if($(this).scrollTop() > 100) {
    id_header.css({
      'padding': '0',

      'transition': '.3s'
    });
    top_header.css({
      'padding': '0',

      'transition': '.3s'
    });
   } else {
    id_header.css({
      'padding': '15px 0',

      'transition': '.3s'
    });
    top_header.css({
      'padding': '5px 0',

      'transition': '.3s'
    });
   };
   if($(this).scrollTop() > 1) {
    header.addClass('header_fixed');
    $('body').css({
       'paddingTop': headerHeight+'px' // делаем отступ у body, равный высоте шапки
    });
   } else {
    header.removeClass('header_fixed');
    $('body').css({
     'paddingTop': 0 // удаляю отступ у body, равный высоте шапки
    })
   }
 });
});

if($(this).scrollTop() > 300) {
    header.css({
      'padding': '0',

      'transition': '.3s'
    });
} else {
    header.css({
      'padding': '15px 0',

      'transition': '.3s'
    });
}