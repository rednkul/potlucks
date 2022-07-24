
$(document).ready(function () {
    var frm = $('#join-form');
    frm.submit(function () {
        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            data: frm.serialize(),
            success: function (response) {
                $('#cart-qty').text(response.cart_qty)
            },
            error: function(data) {
                console.log(response.responseJSON.errors)
            }
        });
        return false;
    });
})