$(document).ready(function(){


wrapped();

$(window).resize(function() {
   width = $(window).width();
    if (width >= 268) {
        wrapped();

    }
});

function wrapped() {
    var offset_top_prev;
    $('.flex-item').each(function() {

       var offset_top = $(this).offset().top;
      if (offset_top > 16) {

            if($(this).hasClass('wrapped')){

             } else {
                $(this).addClass('wrapped');
                $(".drop-menu").css("display","block");
                $(".drop-menu").css("position","absolute");
                $(".drop-menu").css("top","18px");
                $(".drop-menu").css("left",$('.menu').children("li").not('.wrapped').last().offset().left + $('.menu').children("li").not('.wrapped').last().width()+10);
                $(this).clone().appendTo(".drop-menu-touch:last");
            }

      } else if (offset_top == 16) {
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
}

//
// $(function() {
//   $('.drop-menu span').click(function() {
//     $('ul.drop-menu-touch').css("visibility","visible");
//   });
// });

    });