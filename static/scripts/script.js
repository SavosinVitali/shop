$(document).ready(function(){











wrapped();

$(window).resize(function() {
   width = $(window).width();
    if (width >= 268) {
        wrapped();

    }
});

function wrapped() {

    //-------------------------------------------------------------------

    var A = $('.menu-category-sub  li'), max = 0, elem;

    A.each(function () {

    if (this.offsetWidth > max) {
        max = this.offsetWidth, elem = this;

    }
});

    $(".menu-category-sub > li").css("width",$(elem).width());

    //-------------------------------------------------------------------


    $(".menu-category-sub").css("left",$(".menu-category").offset().left+3);
    $(".menu-category-sub").css("width",$(".menu-category").width()-87);




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
//      $(".menu-category li").hover(
//             function(){
//
//                 // console.log($(".menu-category li:last-child").offset().right)
//                 // console.log($(".menu-category").height())
//                 // $(".menu-category-sub").css("top",$(".menu-category").height()+$(".menu-category").offset().top);
//                 // $(".menu-category-sub").css("left",$(".menu-category").offset().left);
//                 // $(".menu-category-sub").css("width",$(".menu-category").width());
//                     });

    });

  // jQuery('img.svg').each(function(){
  //           var $img = jQuery(this);
  //           var imgID = $img.attr('id');
  //           var imgClass = $img.attr('class');
  //           var imgURL = $img.attr('src');
  //
  //           jQuery.get(imgURL, function(data) {
  //               // Get the SVG tag, ignore the rest
  //               var $svg = jQuery(data).find('svg');
  //
  //               // Add replaced image ID to the new SVG
  //               if(typeof imgID !== 'undefined') {
  //                   $svg = $svg.attr('id', imgID);
  //               }
  //               // Add replaced image classes to the new SVG
  //               if(typeof imgClass !== 'undefined') {
  //                   $svg = $svg.attr('class', imgClass+' replaced-svg');
  //               }
  //
  //               // Remove any invalid XML tags as per http://validator.w3.org
  //               $svg = $svg.removeAttr('xmlns:a');
  //
  //               // Replace image with new SVG
  //               $img.replaceWith($svg);
  //
  //           }, 'xml');
  //
  //              });