$(document).ready(function () {
    var frm = $('#orders-filter');
    frm.submit(function () {
        event.preventDefault();
        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            headers:{'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')},
            data: frm.serialize(),
            success: function (response) {
                $('#orders').html("");
                $.each(response.orders, function( order, values ) {
                   $('#orders').prepend(
                                            '<div class="row order-card">' +
                                            '<div class="col-lg-1">' +
                                                '<h1>' + order + '</h1>' +
                                            '</div>' +
                                            '<div class="col-lg-5">' +
                                                '<p>Заказчик: ' + values.last_name + ' '  + values.first_name + ' ' +
                                                values.patronymic + '</p>' +
                                                '<p>Телефон: ' + values.phone_number + '</p>' +
                                                '<p>Email: ' + values.email + '</p>' +
                                                '<p>Город: ' + values.city + '</p>' +
                                                '<p>Адрес: ' + values.post_index + '</p>' +
                                                '<p>Создан: ' + values.created + '</p>' +
                                                '<p>Примечания: ' + values.notes + '</p>' +
                                            '</div>' +

                                            '<div class="col-lg-5"' +
                                                '<p>В заказе:</p>' +
                                                '<div id="order-items-' + order + '">' +
                                                '<p>Товар: ' + values.product + '</p>' +
                                                '<p>Цена за ед.: ' + values.product_price + ' р</p>' +
                                                '<p>Количество: ' + values.goods_number + ' шт.</p>' +

                                                '<p>Всего за заказ: ' + values.total_cost  + ' р</p>' +
                                                '</div>' +
                                            '</div>' +
                                        // Подтверждение после звонка
                                            '<div class="col-lg-1">' +
                                                '<label>Подтвержден</label>' +
                                            '<div' +
                                                ' data-do="' + '/ajax/order_confirm/potluck/' + order + '/"' +
                                                ' data-undo="' + '/ajax/order_disconfirm/potluck/' + order + '/"' +
                                                ' data-num="' + order + '"' +
                                                ' class="col-lg-1 switch-btn red"' +
                                                ' id="confirmed_switch-'+ order + '">' +


                                            '</div>'+


                                        // Оплата

                                            '<label for="paid_switch-' + order + '">Оплачен</label>' +
                                            '<div' +
                                                ' data-do="' + '/ajax/order_paid/potluck/' + order + '/"' +
                                                ' data-undo="' + '/ajax/order_unpaid/potluck/' + order + '/"' +
                                                ' data-num="' + order + '"' +
                                                ' class="col-lg-1 switch-btn green"' +
                                                ' id="paid_switch-'+ order + '">' +
                                            '</div>'+
                                        '</div>' +
                                        '</div>'
                                        );

                   if (values.confirmed == true) {
                        $('#confirmed_switch-'+ order).addClass('switch-on');

                   }
                   if (values.paid == true) {
                        $('#paid_switch-'+ order).addClass('switch-on');

                   }

                console.log('перед уборкой');
                if (Object.keys(response.orders).length <= response.paginate_by) {
                    $('#pagination').attr('style', 'display:none');

                } else {
                    $('#pagination').attr('style', '');

                }
                $(document).on('change', 'select', function (event) {
                    event.preventDefault()});
                });





            },
            error: function(response) {
                console.log(response.responseJSON.errors)

            }

        });

    });
})