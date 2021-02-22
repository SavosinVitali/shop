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

    var A = $('.menu-category > li');
    $(".menu-category-sub").css("left",$(".menu-category").offset().left+3);
    $(".menu-category-sub").css("width",$(".menu-category").width()-87);

    A.each(function () {

         var max = 0, i=0, t=0, r=0, z=0;
         // console.log(this);
         $(this).children('ul').children('li').each(function (index) {
               // console.log($(this).offsetWidth);
             // console.log(this.offsetWidth);
             if ($(this).outerWidth(true) > max) {
                max = $(this).outerWidth(true);
                // console.log("max");
                // console.log(this.offsetWidth);
                // console.log($(this).outerWidth(true));
                // console.log("max");
           }

                i=i+1;
         });



          t= ~~(($(".menu-category").width()-87 )/ max);
          r = ($(".menu-category").width()-87 );
          if(t>i){
              $(this).children('ul').children('li').css("width",   r / i - 20);
          }
          else {
              $(this).children('ul').children('li').css("width", r / t - 20);
          }
          // $(this).children('ul').children('li').css("width",max);
          console.log('sleduchiy punkt');
          console.log(max);
          console.log(t);
          //  r = ~~(i / (($(".menu-category").width()-87 )/ max));
          // // console.log($(".menu-category").width()-87);
           console.log(r);
          // z= t-r;
          console.log(r / t);
          // console.log('sleduchiy punkt');
          // console.log($(".menu-category").width()-87);
          // console.log(max);
          //  console.log('sleduchiy punkt');



    // console.log($(this).children('a').text());
    // console.log($(this).children('ul').children('li').children('a').text());
    // console.log($(this).children('ul').children('li').width());
    // if ($(this).children('ul').children('li').offsetWidth > max) {
    //     max = $(this).children('ul').children('li').offsetWidth;
    //     elem = $(this).children('ul').children('li');
    //        }
        // console.log($(this).children('ul').children('li').offsetWidth);
        // console.log(elem);
     // $(A).css("width",this.offsetWidth);
     // $(A).children("li")
     // console.log($(elem).width())
});
    // console.log($(".menu-category-sub").width())
    // console.log($(elem).width())

    // $(".menu-category-sub > li").css("width",$(elem).width());

    //-------------------------------------------------------------------







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