$(document).ready(function () {
          // отслеживаем событие отправки формы
          $('#number').keyup(function () {

              // создаем AJAX-вызов

              $.ajax({
                  data: $(this).serialize(), // получаяем данные формы

                  url: "{% url 'ajax:validate_goods_number' order.id %}",
                  // если успешно, то
                  success: function (response) {
                      if (response.is_integer == false) {
                          $('#not-available').remove();
                          $('#join').after('<p style="color:red" id="not-available">Введите целое положительное число</p>');
                          $("#join").prop("disabled",true);
                      }
                      else {

                          if (response.is_available == false) {
                              $('#not-available').remove();
                              $('#join').after('<p style="color:red" id="not-available">Нельзя выбрать больше {{ available }}</p>');
                              $("#join").prop("disabled",true);
                          }
                          else {

                              $('#not-available').remove();
                              $("#join").prop("disabled",false);

                          }
                      }

                  },
                  // если ошибка, то
                  error: function (response) {
                      // предупредим об ошибке
                      console.log(response.responseJSON.errors)
                  }
              });
              return false;
          });
      })

return false;

$(document).ready(function(){
        //Скрыть PopUp при загрузке страницы
        $("#popup1").hide();
        $('.cancel').click(function () {
            $("#popup1").show();
        });
        $('#no_cancel').click(function () {
            $("#popup1").hide();
        });
    })


// ajax удаления заказа пользователя

        $(document).ready(function () {
          // отслеживаем событие отправки формы
          $('.cancel_order').click(function () {
              var modalId = this.getAttribute('data-modal'),

              // создаем AJAX-вызов

              $.ajax({
                  data: $(this).serialize(), // получаяем данные формы

                  url: "{% url 'ajax:cancel_customer_order' 5 %}",
                  // если успешно, то

                  // если ошибка, то
                  error: function (response) {
                      // предупредим об ошибке
                      console.log(response.responseJSON.errors)
                  }
              });




          });
      })
