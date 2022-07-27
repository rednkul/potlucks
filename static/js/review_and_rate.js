$(document).ready(function () {
    var frm = $('#review-form');
    frm.submit(function () {
        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            data: frm.serialize(),
            success: function (response) {
            var id='review-' + response.review.id;
            if (response.review.created) {
                  $('#reviews-ul').prepend('<li id="'+ id + '">' +
                                            '<div class="review-heading">' +
                                                '<h5 class="name">' + response.review.customer + '</h5>' +
                                                    '<p class="date">' + response.review.date + '</p>' +
                                                        '<div class="review-rating">' +
                                                            ' <i class="fa fa-star empty"></i>' .repeat(response.review.star) +
                                                            ' <i class="fa fa-star-o empty"></i> '.repeat(5 - response.review.star) +
                                                        '</div>' +
                                            '</div>' +
                                            '<div class="review-body">' +
                                                '<p class="review-text">' + response.review.text + '</p>' +
                                            '</div>' +
                                        '</li>');
                } else {
                $("#" + id).html(
                                '<div class="review-heading">' +
                                                '<h5 class="name">' + response.review.customer + '</h5>' +
                                                    '<p class="date">' + response.review.date + '</p>' +
                                                        '<div class="review-rating">' +
                                                            ' <i class="fa fa-star empty"></i>' .repeat(response.review.star) +
                                                            ' <i class="fa fa-star-o empty"></i> '.repeat(5 - response.review.star) +
                                                        '</div>' +
                                            '</div>' +
                                            '<div class="review-body">' +
                                                '<p class="review-text">' + response.review.text + '</p>' +
                                                '<p class="date">Отзыв обновлен' + response.review.updated_at + '</p>' +
                                            '</div>'
                                );
                }
            $('#rating-avg').text(response.product.rating_avg);

            $('#product-rating').html(

                                        ' <i class="fa fa-star empty"></i> '.repeat(Math.round(response.product.rating_avg)) +
                                        ' <i class="fa fa-star-o empty"></i> '.repeat(5 - Math.round(response.product.rating_avg))
            );

            $('#rating-avg-stars').html(

                                        ' <i class="fa fa-star empty"></i> '.repeat(Math.round(response.product.rating_avg)) +
                                        ' <i class="fa fa-star-o empty"></i> '.repeat(5 - Math.round(response.product.rating_avg))
            );

            $('#ones').text(response.product.number_of_ratings.ones);
            $('#twos').text(response.product.number_of_ratings.twos);
            $('#threes').text(response.product.number_of_ratings.threes);
            $('#fours').text(response.product.number_of_ratings.fours);
            $('#fives').text(response.product.number_of_ratings.fives);

            $('#add-or-update-review').text('Дополнить отзыв');


            },
            error: function(response) {
                console.log(response.responseJSON.errors)
            }
        });
        return false;
    });
})


