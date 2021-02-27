
$('.menu-category').ready(function(){
wrapped_submenu();
});

$('.header-top-menu').ready(function(){
wrapped();
});






$(document).ready(function(){

sub_menu();


$(window).resize(function() {
   width = $(window).width();
    if (width >= 268) {
        wrapped();
        wrapped_submenu();
        // wrapped_submenu();

    }
});



function sub_menu() {
    var A = $('.menu-category > li');

    A.mouseleave(function () {
        $(this).children('ul').children(".hidden").remove();
        $(".menu-category-sub").children('li').css("flex-basis", 0);


    });

    A.mouseenter(function () {

        // $(".menu-category-sub").css("width",$(".menu-category").width()-60);

        // A.each(function () {

        var max = 0, max_real = 0, i = 0, t = 0, r = 0, z = 0, pad = 0;


        $(this).children('ul').children('li').each(function (index) {

            if ($(this).outerWidth(true) > max) {
                max = $(this).outerWidth(true) + $(this).outerWidth(true) - $(this).width();
                max_real = $(this).outerWidth(true);

            }

            i = i + 1;
        });


        t = ~~($(".menu-category-sub").width() / max);
        r = Math.ceil(i / t);
        //   console.log(max);
        //  console.log($(".menu-category-sub").width());
        // console.log(t);
        //  console.log(r);

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
    });



function wrapped() {

    //-------------------------------------------------------------------

    var offset_top_prev= $('.header-top-menu').first('li').offset().top;


    //-------------------------------------------------------------------

    // $(".header-top-menu").css("overflow","visible");


    //-------------------------------------------------------------------_________________-----------------------



    $('.flex-item').each(function() {

       var offset_top = $(this).offset().top;
      if (offset_top > offset_top_prev) {

            if($(this).hasClass('wrapped')){

             } else {
                $(this).addClass('wrapped');
                $(".drop-menu").css("display","block");
                $(".drop-menu").css("position","absolute");
                $(".drop-menu").css("top","18px");
                $(".drop-menu").css("left",$('.menu').children("li").not('.wrapped').last().offset().left + $('.menu').children("li").not('.wrapped').last().width()+10);
                $(this).clone().appendTo(".drop-menu-touch:last");
            }

      } else if (offset_top == offset_top_prev) {
          if ($(this).hasClass('wrapped')) {
              $(this).removeClass('wrapped');
              $(".drop-menu-touch li:last").remove();
              $(".drop-menu").css("top","18px");
              $(".drop-menu").css("left", $(this).offset().left+$(this).width() + 10);
              if ($(".drop-menu-touch").find('li').length == 0) {
                  $(".drop-menu").css("display", "none");
              }

          }
      }
   });

     $(".header-top").css("visibility","visible");

}





function wrapped_submenu() {

    //-------------------------------------------------------------------
    var max = 0;
    var A = $('.menu-category > li');
    var offset_top_prev= A.first('li').offset().top;

    //
    //-------------------------------------------------------------------_________________-----------------------




   A.each(function() {

       var offset_top = $(this).offset().top;
       console.log(+ $(".drop-menu-category").height());
       // $(".drop-menu-touch-category ").css("top",$(".drop-menu-category").offset().top);
      if (offset_top > offset_top_prev) {

            if($(this).hasClass('wrapped_submenu')){

             } else {
                $(this).addClass('wrapped_submenu');
                $(".drop-menu-category").css("display","flex");

                // $(".drop-menu").css("position","absolute");
                // $(".drop-menu").css("top","18px");
                // $(".drop-menu").css("left",$('.menu').children("li").not('.wrapped').last().offset().left + $('.menu').children("li").not('.wrapped').last().width()+10);
                $(this).clone().appendTo(".drop-menu-touch-category:last");
                // $(this).css("visibility","hidden");
            }

      } else if (offset_top == offset_top_prev) {
          if ($(this).hasClass('wrapped_submenu')) {
              $(this).removeClass('wrapped_submenu');
              // console.log($(this).children('a').text());
              $(".drop-menu-touch-category > li").last().remove();


              // $(this).css("visibility","visible");

              // $(".drop-menu").css("left", $(this).offset().left+$(this).width() + 10);
              if ($(".drop-menu-touch-category").find('li').length == 0) {
                  $(".drop-menu-category").css("display", "none");
                  $('.menu-category').css("height",'auto');
              }

          }
      }
   });
    $(".drop-menu-touch-category ").css("top",A.first('li').height());
    // $(".drop-menu-touch-category ").css("right",0);
    $('.menu-category').css("height",A.first('li').height());
    $(".header-category").css("visibility","visible");
    //-------------------------------------------------------------------_________________-----------------------
     $(".menu-category-sub").css("left",$(".menu-category").children('li').first().offset().left);
    $(".menu-category-sub").css("width",$(".header-category").width()-($('.menu-category-sub').outerWidth(true) - $('.menu-category-sub').width()));
      //-------------------------------------------------------------------_________________-----------------------

}

function sub_menu() {
    var A = $('.menu-category > li');

    A.mouseleave(function () {
        $(this).children('ul').children(".hidden").remove();
        $(".menu-category-sub").children('li').css("flex-basis", 0);


    });

    A.mouseenter(function () {

        // $(".menu-category-sub").css("width",$(".menu-category").width()-60);

        // A.each(function () {

        var max = 0, max_real = 0, i = 0, t = 0, r = 0, z = 0, pad = 0;


        $(this).children('ul').children('li').each(function (index) {

            if ($(this).outerWidth(true) > max) {
                max = $(this).outerWidth(true) + $(this).outerWidth(true) - $(this).width();
                max_real = $(this).outerWidth(true);

            }

            i = i + 1;
        });


        t = ~~($(".menu-category-sub").width() / max);
        r = Math.ceil(i / t);
        //   console.log(max);
        //  console.log($(".menu-category-sub").width());
        // console.log(t);
        //  console.log(r);

        pad = (t * r - i);


        if (t > i) {

        } else {
            for (i = 0; i < pad; i++) {
                $(this).children('ul').append("<li class=\"hidden\"><span>  </span></li>");
            }

            $(this).children('ul').children('li').css("flex-basis", max_real);

        }


// });


    });
}