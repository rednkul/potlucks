$(document).ready(function () {
    var frm = $('#review-form');
    frm.submit(function () {
        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            data: frm.serialize(),
            success: function (response) {
            var stars = '<i class="fa fa-star empty"></i>'
            $('#reviews-ul').append('<li>' +
                                            '<div class="review-heading">' +
                                                '<h5 class="name">' + response.review.customer + '</h5>' +
                                                    '<p class="date">' + response.review.date + '</p>' +
                                                        '<div class="review-rating">' +
                                                            '<i class="fa fa-star empty"></i>'.repeat(response.review.star) +
                                                            '<i class="fa fa-star-o empty"></i>'.repeat(5 - response.review.star) +
                                                        '</div>' +
                                            '</div>' +
                                            '<div class="review-body">' +
                                                '<p class="review-text">' + response.review.text + '</p>' +
                                            '</div>' +
                                        '</li>'
                )
            },
            error: function(response) {
                console.log(response.responseJSON.errors)
            }
        });
        return false;
    });
})


