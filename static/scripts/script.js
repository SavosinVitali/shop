$(document).ready(function(){


wrapped();

$(window).resize(function() {
   width = $(window).width();
    if (width >= 768) {
        wrapped();

    }
});

function wrapped() {
    var offset_top_prev;
    $('.flex-item').each(function() {

       var offset_top = $(this).offset().top;
       console.log($(this).offset().top)
      if (offset_top > 16) {

            if($(this).hasClass('wrapped')){

             }else{

                $(this).addClass('wrapped');
                $(".drop-menu").css("display","block");
                $(this).clone().appendTo(".drop-menu-touch:last");

            }



      } else if (offset_top <= 16) {
          if($(this).hasClass('wrapped'))
          {
              $(this).removeClass('wrapped');
              $(".drop-menu-touch li:last").remove();
          }
          if ($(".drop-menu-touch").find('li').length == 0){
              $(".drop-menu").css("display","none");
          }
          // $(".drop-menu").css("display","none");

      }

   offset_top_prev = offset_top;
   });
}

//
// $(function() {
//   $('.drop-menu span').click(function() {
//     $('ul.drop-menu-touch').css("visibility","visible");
//   });
// });

    });