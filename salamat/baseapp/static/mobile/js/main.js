$(".search .open").click(function() {
	$(".search").addClass("active");
});
$(".search .close").click(function() {
	$(".search").removeClass("active");
});

$(".menu").click(function() {
	$("#menu").addClass("active");
});

$("#menu .close").click(function(e) {
	e.preventDefault();
	$("#menu").removeClass("active");
	$("#menu li span").html("+");
});

$(".totop").click(function(e) {
	e.preventDefault();
	$("body, html").animate({scrollTop: 0}, 1000);
});

$(document).ready(function() {
    // var $messages = $('#messages .message');
    //
    // if($messages.length){
    //     $messages.each(function(){
    //         var $message = $(this);
    //          setTimeout(function( ) {
    //             if ($message.hasClass('success')){
    //                 toastr.success($message.text(), 'Успех!');
    //             }
    //             if ($message.hasClass('error')){
    //                 toastr.error($message.text(), 'Ошибка!');
    //             }
    //
    //         }, 1300);
    //     });
    // }
	$(".slick-slider").slick({
		dots: false,
        infinite: true,
		prevArrow: $("#prev"),
		nextArrow: $("#next")
	});
	$(".category-slick-slider-1").slick({
		arrows: false,
		dots: true,
		appendDots: $(".cat-1 .dots"),
        infinite: true
	});
	$(".category-slick-slider-2").slick({
		arrows: false,
		dots: true,
		appendDots: $(".cat-2 .dots"),
        infinite: true
	});
	$(".category-slick-slider-3").slick({
		arrows: false,
		dots: true,
		appendDots: $(".cat-3 .dots"),
        infinite: true
	});
	$(".product-slick-slider-1").slick({
		arrows: false,
		dots: true,
		appendDots: $(".dots-1"),
        infinite: true
	});
	$(".product-slick-slider-2").slick({
		arrows: false,
		dots: true,
		appendDots: $(".dots-2"),
        infinite: true
	});
	$(".product-slick-slider-3").slick({
		arrows: false,
		dots: true,
		appendDots: $(".dots-3"),
        infinite: true
	});
	$(".product-slick-slider-4").slick({
		arrows: false,
		dots: true,
		appendDots: $(".dots-4"),
        infinite: true
	});
	$(".product-slick-slider-5").slick({
		arrows: false,
		dots: true,
		appendDots: $(".dots-5"),
        infinite: true
	});
	$(".projects-slider").slick({
		arrows: false,
		dots: true,
        infinite: true
	});
	$(".project-slider").slick({
		arrows: false,
		dots: true,
		appendDots: $(".projects .dots"),
        infinite: true
	});
    $(".clients-slick-slider").slick({
		arrows: true,
		dots: false,
        infinite: true,
        slidesToShow: 1
    });
	$(".partners-slider").slick({
		arrows: true,
		dots: false,
        infinite: true,
        slidesToShow: 1
	});
	$(".sertificates-slider").slick({
		arrows: false,
		infinite: true,
		slidesToShow: 1,
		dots: true,
		appendDots: $(".dots-ser")
	});
	$(".v-product-slick-slider-1").slick({
		arrows: false,
		dots: true,
		appendDots: $(".dots"),
        infinite: true
	});
	$(".commerce-slick-slider-1").slick({
		arrows: false,
		dots: true,
		appendDots: $(".dots-1"),
        infinite: true
	});
	$(".commerce-slick-slider-2").slick({
		arrows: false,
		dots: true,
		appendDots: $(".dots-2"),
        infinite: true
	});
	$(".commerce-slick-slider-3").slick({
		arrows: false,
		dots: true,
		appendDots: $(".dots-3"),
        infinite: true
	});
	$(".commerce-slick-slider-4").slick({
		arrows: false,
		dots: true,
		appendDots: $(".dots-4"),
        infinite: true
	});
	$(".commerce-slick-slider-5").slick({
		arrows: false,
		dots: true,
		appendDots: $(".dots-5"),
        infinite: true
	});
	$(".commerce-slick-slider-6").slick({
		arrows: false,
		dots: true,
		appendDots: $(".dots-6"),
        infinite: true
	});
	$(".commerce-slick-slider-7").slick({
		arrows: false,
		dots: true,
		appendDots: $(".dots-7"),
        infinite: true
	});
	$(".commerce-slick-slider-8").slick({
		arrows: false,
		dots: true,
		appendDots: $(".dots-8"),
        infinite: true
	});
	$(".commerce-slick-slider-9").slick({
		arrows: false,
		dots: true,
		appendDots: $(".dots-9"),
        infinite: true
	});
	$(".financial-slick-slider-1").slick({
		arrows: false,
		dots: true,
		appendDots: $(".dots-1"),
        infinite: true
	});
	$(".financial-slick-slider-2").slick({
		arrows: false,
		dots: true,
		appendDots: $(".dots-2"),
        infinite: true
	});
	$(".financial-slick-slider-3").slick({
		arrows: false,
		dots: true,
		appendDots: $(".dots-3"),
        infinite: true
	});
	$(".financial-slick-slider-4").slick({
		arrows: false,
		dots: true,
		appendDots: $(".dots-4"),
        infinite: true
	});
	$(".financial-slick-slider-5").slick({
		arrows: false,
		dots: true,
		appendDots: $(".dots-5"),
        infinite: true
	});
	$(".financial-slick-slider-6").slick({
		arrows: false,
		dots: true,
		appendDots: $(".dots-6"),
        infinite: true
	});
	$(".city-slick-slider-1").slick({
		arrows: false,
		dots: true,
		appendDots: $(".dots-1"),
        infinite: true
	});
	$(".city-slick-slider-2").slick({
		arrows: false,
		dots: true,
		appendDots: $(".dots-2"),
        infinite: true
	});
	$(".city-slick-slider-3").slick({
		arrows: false,
		dots: true,
		appendDots: $(".dots-3"),
        infinite: true
	});
	$(".city-slick-slider-4").slick({
		arrows: false,
		dots: true,
		appendDots: $(".dots-4"),
        infinite: true
	});
	$(".city-slick-slider-5").slick({
		arrows: false,
		dots: true,
		appendDots: $(".dots-5"),
        infinite: true
	});
	$(".city-slick-slider-6").slick({
		arrows: false,
		dots: true,
		appendDots: $(".dots-6"),
        infinite: true
	});
	$(".hotel-slick-slider-1").slick({
		arrows: false,
		dots: true,
		appendDots: $(".dots-1"),
        infinite: true
	});
	$(".alarm-slick-slider-1").slick({
		arrows: false,
		dots: true,
		appendDots: $(".dots-1"),
        infinite: true
	});
	$(".production-slick-slider").slick({
		arrows: true,
		dots: false,
        infinite: true
	});
	$(".domofon-slick-slider-1").slick({
		arrows: false,
		dots: true,
		appendDots: $(".dots-1"),
        infinite: true
	});
	$(".domofon-slick-slider-2").slick({
		arrows: false,
		dots: true,
		appendDots: $(".dots-2"),
        infinite: true
	});
	$(".drones-slick-slider-1").slick({
		arrows: false,
		dots: true,
		appendDots: $(".dots-1"),
        infinite: true
	});
	$(".drones-slick-slider-2").slick({
		arrows: false,
		dots: true,
		appendDots: $(".dots-2"),
        infinite: true
	});
	$(".lift-slick-slider-1").slick({
		arrows: false,
		dots: true,
		appendDots: $(".dots-1"),
        infinite: true
	});
	$(".slick-slider .caption").css({height: $(".main-slider").height()});
	$(".our-projects .slick-dots").css({width: $(".our-projects").width()});
	$(".our-projects .slick-dots button").css({width: $(".our-projects").width() / $(".our-projects .slick-dots li").length});
	$("#project .slick-dots").css({width: $("#project").width()});
	$("#project .slick-dots button").css({width: $("#project").width() / $("#project .slick-dots li").length});
	$("#serificates .slick-dots").css({width: $("#serificates").width()});
	$("#serificates .slick-dots button").css({width: $("#serificates").width() / $("#serificates .slick-dots li").length});
	$(".aboutus .projects .slick-dots").css({width: $(".aboutus .projects").width()});
	$(".aboutus .projects .slick-dots button").css({width: $(".aboutus .projects").width() / $(".aboutus .projects .slick-dots li").length});
});

$(window).scroll(function() {
	var top = $(window).scrollTop();
	var block = $(".block:first-child").height();
	if (top > block) {
		$(".totop").addClass("active");
	} else {
		$(".totop").removeClass("active");
	}
});

$("#menu li span").click(function() {
	$(this).parent().toggleClass("active");
	$("#menu li span").not(this).parent().removeClass("active");
	$(this).html("-");
	$("#menu li span").not(this).html("+");
	if (!$(this).parent().hasClass("active")) {
		$(this).html("+");
	}
});

/*$(document).ready(function() {
	var click_check_1 = true;
	var click_check_2 = true;
	$("#menu li span", "click", function() {
		if (click_check_1) {
			$("#menu li").removeClass("active");
			$(this).parent().addClass("active");
			$(this).html("-");
			$("#menu li span").not(this).html("+");
		} else {
			$("#menu li").removeClass("active");
			$("#menu li span").html("+");
		}
		click_check_1 = !click_check_1;
	});
});*/