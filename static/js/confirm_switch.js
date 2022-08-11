$(document).on('click', '.switch-btn', function () {
          // отслеживаем событие отправки формы

          // При добалении кнопки подтверждения заказа после звонка клиенту
          // Возникла сложность - после применения ajax-фильтрации кнопки перестали работать
          // После click на on('click', ...) проблема устранена

            event.preventDefault();
            console.log('НАжал');
            var url
            var num = $(this).data('num')
            $(this).toggleClass('switch-on');
            if ($(this).hasClass('switch-on')) {
               $(this).trigger('on.switch');
               url = $(this).data('do');

            } else {
                $(this).trigger('off.switch');
                url = $(this).data('undo');

            };

          // создаем AJAX-вызов
            $.ajax({

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


});