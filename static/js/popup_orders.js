$('#orders').on('click', '#cancel-order', function () {


        var url = $('#cancel_order').data('url');
        console.log('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa');
        console.log(url + 'В po');
        $.ajax({

        url: url,

                  // если успешно, то
                  success: function (response) {
                        console.log(response);

                  },
                  // если ошибка, то
                  error: function (response) {
                      // предупредим об ошибке
                      console.log(response.responseJSON.errors)
                  }
         });
})

