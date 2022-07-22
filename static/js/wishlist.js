$(document).ready(function () {
          // отслеживаем событие отправки формы
          $('.add-to-wishlist').click(function () {




              if ($(this).hasClass('fa-heart-o')) {
                var url = $(this).data('add')
              }
              else {
                var url = $(this).data('del')
              };

              // создаем AJAX-вызов

              $.ajax({
                  data: $(this).serialize(), // получаяем данные формы

                  url: url,
                  // если успешно, то
                  success: function (response) {
                    $(this).removeClass('fa-heart-o');
                    $(this).addClass('fa-heart');
                    $('#wishlist-qty').text(response.wishlist_qty);

                  },
                  // если ошибка, то
                  error: function (response) {
                      // предупредим об ошибке
                      console.log(response.responseJSON.errors)
                  }
              });

              if ($(this).hasClass('fa-heart-o')) {
                $(this).removeClass('fa-heart-o');
                $(this).addClass('fa-heart');
                $(this).attr('data-url', del);
              }
              else {
                $(this).addClass('fa-heart-o');
                $(this).removeClass('fa-heart');
                $(this).attr('data-url', add)
              };


          });
      })