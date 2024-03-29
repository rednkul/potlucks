$(document).ready(function () {
          // отслеживаем событие отправки формы
          $('.add-to-wishlist').click(function () {




              var url = $(this).data('url')

              // создаем AJAX-вызов

              $.ajax({
                  data: $(this).serialize(), // получаяем данные формы

                  url: url,
                  // если успешно, то
                  success: function (response) {

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
                $(this).attr('data-url', "{% url 'ajax:delete_product_from_wishlist' product.id %}");

              }
              else {
                $(this).addClass('fa-heart-o');
                $(this).removeClass('fa-heart');
                $(this).attr('data-url', "{% url 'ajax:add_product_to_wishlist' product.id %}");

              };


          });
      })