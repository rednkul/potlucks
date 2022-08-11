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
                                            '<div class="row order-card blocks-wrapper">' +
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

                                                '<p>Всего за заказ: ' + values.total_cost  + ' р</p>' +
                                                '</div>' +
                                            '</div>' +

                                        '<div class="col-lg-1">' +
                                            '<label>Подтвержден</label>' +
                                            '<div' +
                                                ' data-confirm="' + '/ajax/order_confirm/' + order + '/"' +
                                                ' data-disconfirm="' + '/ajax/order_disconfirm/' + order + '/"' +
                                                ' data-num="' + order + '"' +
                                                ' class="col-lg-1 switch-btn confirmed_switch"' +
                                                ' id="confirmed_switch-'+ order + '">' +


                                            '</div>'+
                                        '</div>' +
                                        '</div>'
                                        );

                   if (values.confirmed == true) {
                        $('#confirmed_switch-'+ order).addClass('switch-on');
                        console.log('#confirmed_switch-'+ order);
                   }
                   $.each(values.items, function(item, item_values){
                        $('#order-items-' + order).prepend( '<p>Товар: ' + item_values.product + ' ' + item_values.quantity  + ' шт ' +
                                                item_values.price + ' р/шт ' + item_values.item_cost + ' р </p>');
                   });
                console.log('перед уборкой');
                if (Object.keys(response.orders).length <= response.paginate_by) {
                    $('#pagination').attr('style', 'display:none');
                    console.log('убрано');
                } else {
                    $('#pagination').attr('style', '');
                    console.log('не убрано');;
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