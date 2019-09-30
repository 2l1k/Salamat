$(document).ready(function() {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", $($("[name='csrfmiddlewaretoken']")[0]).val());
        }
    });

    $(window).load(function() {
        $(".eapps-widget").next().remove();
    });
    $("[href='#categories']").click(function(e) {
        e.preventDefault();
        $(this).toggleClass("active");
        $("#categories").slideToggle();
    });
    $("[href='#catalog']").click(function(e) {
        e.preventDefault();
        $("#catalog").slideToggle();
        $("#catalog li:has(ul:has(ul))").removeClass("open");
    });
    $(".slider").slick({
        dots: false,
        arrows: true,
        infinite: true
    });
    $(".carousel").slick({
        dots: false,
        arrows: true,
        infinite: true,
        slidesToShow: 5,
        slidesToScroll: 1,
        responsive: [
            {
                breakpoint: 1080,
                settings: {
                    slidesToShow: 3
                }
            }
        ]
    });
    $(".slider-2").slick({
        dots: true,
        arrows: false,
        infinite: true
    });
    $(".carousel-2").slick({
        dots: false,
        arrows: true,
        infinite: true,
        slidesToShow: 4,
        slidesToScroll: 1,
        responsive: [
            {
                breakpoint: 1080,
                settings: {
                    slidesToShow: 1
                }
            }
        ]
    });
     $('.filter_select').on('change', function () {
          var url = $(this).val(); // get selected value
          if (url) { // require a URL
              url = '?category=' + url
              window.location = url; // redirect
          }
          return false;
      });

    $("#categories label").click(function() {
        var name = $(this).find("span").html();
        $(".categories-btn span").html(name);
    });
    $(document).click(function(e) {
        if ($(e.target).closest(".categories-btn").length) return;
        $("#categories").slideUp();
        e.stopPropagation();
        $("[href='#categories']").removeClass("active");
    });
    $(document).click(function(e) {
        if ($(e.target).closest(".catalog-btn").length) return;
        else if ($(e.target).closest("#catalog").length) return;
        $("#catalog").slideUp();
        $("#catalog li:has(ul:has(ul))").removeClass("open");
        e.stopPropagation();
    });
    $(document).delegate(".rent .slick-arrow", "click", function() {
        setTimeout(function() {
            var subject = $(".rent .slick-current h3").text();
            $(".rent [name='subject']").val(subject);
        }, 500);
    });
    $("[name='show_phone']").change(function() {
        var phone = $(".show_phone").attr("data-value");
        var customer = $(".show_phone").attr("data-customer");
        var data = {customer: customer}
        if ($(this).is(":checked")) {
            $(".show_phone").html(phone);
            $.post('/ru/show_phone/', data);
        } else {
            $(".show_phone").html("+77*********");
        }
    });
    $(".tabs a").click(function(e) {
        e.preventDefault();
        var id = $(this).attr("href");
        $(".tabs a").removeClass("active");
        $(this).addClass("active");
        $(".tab").removeClass("active");
        $(id).addClass("active");
        $(id).find(".levels .level:nth-child(2)").trigger("click");
    });
    $(".level").click(function(e) {
        e.preventDefault();
        var id = $(this).attr("href");
        $(".level").removeClass("active");
        $(this).addClass("active");
        $(".level-plan").removeClass("active");
        $(id).addClass("active");
    });
    $(".tabs-2 a").click(function(e) {
        e.preventDefault();
        var id = $(this).attr("href");
        $(".tabs-2 a").removeClass("active");
        $(this).addClass("active");
        $(".tab-2").removeClass("active");
        $(id).addClass("active");
    });
    $(".rent-item .open-form").click(function() {
        $(this).parent().parent().parent().find("form").slideToggle();
    });
    $(".product-page .images .image").click(function(e) {
        e.preventDefault();
        var src = $(this).attr("href");
        $("#image").attr("src", src);
        $(".product-page .images .image").removeClass("active");
        $(this).addClass("active");
    });
    $(".burger").click(function() {
        $("#menu").slideToggle();
    });
    if ($(window).width() < 1024) {
        $(document).click(function(e) {
            if ($(e.target).closest(".burger").length) return;
            $("#menu").slideUp();
            e.stopPropagation();
        });
    }
    $(".youtube").magnificPopup({
        type: 'iframe',
        mainClass: 'mfp-fade',
        removalDelay: 160,
        preloader: false,
        fixedContentPos: false
    });

    $("[name='all']").click(function() {
        var c = this.checked;
        $("[type='checkbox'").prop("checked", c);
    });
    $("[popup]").magnificPopup({
        type: 'inline'
    });
    $("#catalog li:has(ul:has(ul))").hover(function() {
        $("#catalog li:has(ul:has(ul))").removeClass("open");
        $(this).addClass("open");
    });
    //страница - План зданий
    $.urlParam = function(name) {
        var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
        if (results==null) {
            return null;
        } else {
            //return decodeURI(results[1]) || 0;
            return results ? decodeURIComponent(results[1].replace(/\+/g, '%20')) : null;
        }
    }

    function url() {
        for (var index in boutiques) {
            if (boutiques[index].boutique_number == $.urlParam('boutique') && boutiques[index].build == $.urlParam('build') && boutiques[index].floor == $.urlParam('floor')) {
                $(".boutique #name").html(boutiques[index].name);
                $(".boutique #link").attr("href", boutiques[index].link);
            }
        }

        $(".boutique #location").html($.urlParam('build') + ", Этаж " + $.urlParam('floor') + ", Салон " + $.urlParam('boutique'));
    }

    if ($.urlParam('build') == "Саламат 1") {
        url();
        $(".boutique").fadeIn();
        $("[href='#tab-1']").trigger("click");
        if ($.urlParam('floor') == "1") {
            $("[href='#level-1-1']").trigger("click");
        }
        if ($.urlParam('floor') == "2") {
            $("[href='#level-1-2']").trigger("click");
        }
        if ($.urlParam('floor') == "3") {
            $("[href='#level-1-3']").trigger("click");
        }
        if ($.urlParam('floor') == "4") {
            $("[href='#level-1-4']").trigger("click");
        }
    }
    if ($.urlParam('build') == "Саламат 2") {
        url();
        $(".boutique").fadeIn();
        $("[href='#tab-2']").trigger("click");
        if ($.urlParam('floor') == "1") {
            $("[href='#level-2-1']").trigger("click");
        }
        if ($.urlParam('floor') == "2") {
            $("[href='#level-2-2']").trigger("click");
        }
    }
    if ($.urlParam('build') == "Саламат 3") {
        url();
        $(".boutique").fadeIn();
        $("[href='#tab-3']").trigger("click");
        if ($.urlParam('floor') == "0") {
            $("[href='#level-3-0']").trigger("click");
        }
        if ($.urlParam('floor') == "1") {
            $("[href='#level-3-2']").trigger("click");
        }
        if ($.urlParam('floor') == "2") {
            $("[href='#level-3-0']").trigger("click");
        }
        if ($.urlParam('floor') == "3") {
            $("[href='#level-3-3']").trigger("click");
        }
    }
    if ($.urlParam('build') == "Саламат 4") {
        url();
        $(".boutique").fadeIn();
        $("[href='#tab-4']").trigger("click");
        if ($.urlParam('floor') == "1") {
            $("[href='#level-4-1']").trigger("click");
        }
        if ($.urlParam('floor') == "2") {
            $("[href='#level-4-2']").trigger("click");
        }
    }
    if ($.urlParam('build') == "Саламат 5") {
        url();
        $(".boutique").fadeIn();
        $("[href='#tab-5']").trigger("click");
        if ($.urlParam('floor') == "0") {
            $("[href='#level-5-0']").trigger("click");
        }
        if ($.urlParam('floor') == "1") {
            $("[href='#level-5-2']").trigger("click");
        }
        if ($.urlParam('floor') == "2") {
            $("[href='#level-5-0']").trigger("click");
        }
        if ($.urlParam('floor') == "3") {
            $("[href='#level-5-3']").trigger("click");
        }
    }

    $("g:not(.empty)").click(function() {
        var build = $(this).attr("data-build");
        var floor = $(this).attr("data-floor");
        var boutique = $(this).attr("data-boutique");

        for (var index in boutiques) {
            if (build == boutiques[index].build && floor == boutiques[index].floor && boutique == boutiques[index].boutique_number) salon = boutiques[index];
        }

        $(".boutique #name").html(salon.name);
        $(".boutique #link").attr("href", salon.link);
        $(".boutique #location").html(build + ", Этаж " + floor + ", Салон " + boutique);
        $(".boutique").fadeIn();
    });
    $("g.empty").click(function() {
        var build = $(this).attr("data-build");
        var floor = $(this).attr("data-floor");
        var boutique = $(this).attr("data-boutique");
        $(".boutiques .empty #location-2").html(build + ", Этаж " + floor + ", Салон " + boutique);
        $(".boutiques .empty [name='boutique']").val(build + ", Этаж " + floor + ", Салон " + boutique);
        $(".boutiques .empty").fadeIn();
    });
    $(".boutique .close, .empty .close").click(function(e) {
        $(".boutique, div.empty").fadeOut();
    });

    //Cat select
    $(".input_cat_btn").click(function() {
        $(".input_cat").slideToggle();
    });
    $(".cat_plus").click(function() {
        $(this).toggleClass("open");
        $(this).next().next().slideToggle();
    });
    /*$(".main-cat").click(function() {
        var c = this.checked;
        $(this).parent().parent().next().find(".sub-cat").prop("checked", c);
    });
    $(".sub-cat").click(function() {
        var c = this.checked;
        $(this).parent().parent().next().find(".sub_sub-cat").prop("checked", c);
    });*/

    $("[name='phone']").inputmask("+7(999)999-99-99");
    $("[name='whatsapp']").inputmask("79999999999");

    $("[name='discount']").change(function() {
        var old_price = parseInt($("#old_price").html());
        var discount = parseInt($(this).val());
        var minus = $("[name='discount_percent']").val();
        if (minus == 1) {
            var new_price = old_price - (old_price / 100 * discount);
        } else {
            var new_price = old_price - discount;
        }
        $("#new_price").html(new_price);
    });
    $("[name='discount_percent']").change(function() {
        var old_price = parseInt($("#old_price").html());
        var discount = parseInt($("[name='discount']").val());
        var minus = $("[name='discount_percent']").val();
        if (minus == 1) {
            var new_price = old_price - (old_price / 100 * discount);
        } else {
            var new_price = old_price - discount;
        }
        $("#new_price").html(new_price);
    });
    $("#present [type='checkbox'], #related [type='checkbox']").change(function() {
        if ($(this).is(":checked")) {
            $(this).next().html("Вернуть");
        } else {
            $(this).next().html("Удалить");
        }
    });
    $(".search input").click(function() {
        if ($(this).is(":focus")) {
            $(".dropdown-products").slideDown();
        } else {
            $(".dropdown-products").slideUp();
        }
    });

    $(".fs-file [type='checkbox']").change(function() {
      if(this.checked) {
        $($(this).closest('.control-group').find('.control-label')).css('background-image', "url('/static/img/icon-select-down.png')")
      }
      else {
        $($(this).closest('.control-group').find('.control-label')).css('background-image', "url(/static/img/btn-3.png)")
      }
  });
});