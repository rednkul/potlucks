$(document).ready(function () {
          // отслеживаем событие отправки формы
          $('.availability').click(function () {

          var url = $(this).data('url')

          // создаем AJAX-вызов
         $.ajax({
                  data: $(this).serialize(), // получаяем данные формы

                  url: url,
                  // если успешно, то
                  success: function (response) {

                  },
                  // если ошибка, то
                  error: function (response) {
                      // предупредим об ошибке
                      console.log(response.responseJSON.errors)
                  }
              });

              if ($(this).hasClass('fa-times')) {
                $(this).removeClass('fa-times');
                $(this).addClass('fa-check');
                $(this).attr('data-url', "{% url 'ajax:product_make_available' product.id %}");
              }
              else {
                $(this).addClass('fa-times');
                $(this).removeClass('fa-check');
                $(this).attr('data-url', "{% url 'ajax:product_make_unavailable' product.id %}");

              };


          });
      })