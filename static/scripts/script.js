 function viewport() {
    var e = window, a = 'inner';
    if (!('innerWidth' in window )) {
        a = 'client';
        e = document.documentElement || document.body;
    }
    return { width : e[ a+'Width' ] , height : e[ a+'Height' ] };
}

if (viewport().width >= 801) {
    // console.log('1');
    $('.menu-category').ready(function () {
        sub_menu();
        wrapped_submenu();

    });

    $('.header-top-menu').ready(function () {
        wrapped();
    });
}

$(document).ready(function(){

$(window).resize(function() {
   // width = $(window).width();
    if (viewport().width >= 801) {
        // $(".drop-menu").css("display","block");
        // $(".drop-menu-category").css("display","flex");
        wrapped();
        sub_menu();
        wrapped_submenu();
      }
    else{
        $('.menu-category').css("height",'auto');
        $(".menu-category-sub").children('li').css("flex-basis", 'auto');
        $(".menu-category-sub").css("width",'auto');
        $(".menu-category-sub").css("left",'auto');
        $(".drop-menu").css("display","none");
        $(".drop-menu-category").css("display","none");

    }
    // if (width <= 801) {
    //     $('.flex-item').each(function() {
    //         $(this).removeClass('wrapped');
    //     });
    //
    //   }

});


    });

function wrapped() {

    var offset_top_prev= $('.header-top-menu').first('li').offset().top;
    $('.flex-item').each(function() {


       var offset_top = $(this).offset().top;

      if (offset_top > offset_top_prev) {
             if($(this).hasClass('wrapped')){
                $(".drop-menu").css("display","block");
             } else {
                $(this).addClass('wrapped');
                $(".drop-menu").css("display","block");
                // console.log('hello');
                $(".drop-menu").css("position","absolute");
                $(".drop-menu").css("top", offset_top_prev);
                $(".drop-menu").css("left",$('.menu').children("li").not('.wrapped').last().offset().left + $('.menu').children("li").not('.wrapped').last().outerWidth(true)+10);
                $(this).clone().appendTo(".drop-menu-touch:last");
            }

      } else if (offset_top == offset_top_prev) {
          if ($(this).hasClass('wrapped')) {
              $(this).removeClass('wrapped');
              $(".drop-menu-touch li:last").remove();
              $(".drop-menu").css("top","18px");
              $(".drop-menu").css("left", $(this).offset().left+$(this).outerWidth(true)+10);
              if ($(".drop-menu-touch").find('li').length == 0) {
                  // console.log('hello');
                  $(".drop-menu").css("display", "none");
              }

          }
      }
   });

     $(".header-top").css("visibility","visible");
}

function wrapped_submenu() {

    var A = $('.menu-category > li');
    var offset_top_prev= A.first('li').offset().top;
   A.each(function() {
       var offset_top = $(this).offset().top;
       if (offset_top > offset_top_prev) {
             $('.menu-category').css("height",A.first().height());

            if($(this).hasClass('wrapped_submenu')){
                $(".drop-menu-category").css("display","flex");
             } else {
                $(this).addClass('wrapped_submenu');
                $(".drop-menu-category").css("display","flex");
                $(this).clone().appendTo(".drop-menu-touch-category:last");
               }

      } else if (offset_top == offset_top_prev) {
          if ($(this).hasClass('wrapped_submenu')) {
              $(this).removeClass('wrapped_submenu');
              $(".drop-menu-touch-category > li").last().remove();
              if ($(".drop-menu-touch-category").find('li').length == 0) {
                  $(".drop-menu-category").css("display", "none");
                  $('.menu-category').css("height",'auto');
              }

          }
      }
   });
    $(".drop-menu-touch-category ").css("top",A.first('li').height());
    $(".header-category").css("visibility","visible");

}

function sub_menu() {
    var A = $('.menu-category > li');
    $(".menu-category-sub").children('li').css("flex-basis", 0);
    $(".menu-category-sub").css("left",$(".menu-category").children('li').first().offset().left);
    $(".menu-category-sub").css("width",$(".header-category").width()-($('.menu-category-sub').outerWidth(true) - $('.menu-category-sub').width()));
       A.each(function () {
       $(this).children('ul').children(".hidden").remove();
        var max = 0, max_real = 0, i = 0, t = 0, r = 0, z = 0, pad = 0;


        $(this).children('ul').children('li').each(function (index) {

            if ($(this).outerWidth(true) > max) {
                max = $(this).outerWidth(true) + $(this).outerWidth(true) - $(this).width();
                max_real = $(this).outerWidth(true);

            }

            i = i + 1;
        });
        t = ~~($(".menu-category-sub").width()/ max);
        r = Math.ceil(i / t);
        pad = (t * r - i);
        if (t > i) {
            } else {
            for (i = 0; i < pad; i++) {
                $(this).children('ul').append("<li class=\"hidden\"><span>  </span></li>");
            }
            $(this).children('ul').children('li').css("flex-basis", max_real);

        }
    });

}