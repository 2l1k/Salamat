$(document).ready(function () {

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $('#csrftoken_').val());
        }
    });

    $("[name='show_phone']").change(function() {
        var customer = $(".show_phone").attr("data-customer");
        var data = {customer: customer}
        $.ajax({
            type: 'POST',
            data:data,
            url: '/show_phone/',
        });
    });
});