$(document).ready(function(){


    var A = $('.menu-category > li');

   A.mouseenter(function(){
        $(".menu-category-sub").children('li').css("flex-basis", 0);
        // $(".menu-category-sub").css("width",$(".menu-category").width()-60);

       // A.each(function () {

         var max = 0, i=0, t=0, r=0, z=0, pad=0;


         $(this).children('ul').children('li').each(function (index) {

             if ($(this).outerWidth(true) > max) {
                max = $(this).width();


           }

                i=i+1;
         });



          t= ~~(($(".menu-category-sub").width()-60)/ max);
          r= Math.ceil(i/t);

          console.log("max");
          console.log(t);
          console.log(r);
          pad =(t*r-i);
          // console.log(r);
          // pad = ($(this).children('ul').children('li').outerWidth(true) - $(this).children('ul').children('li').width());

           if(t>i){
              // $(this).children('ul').children('li').css("flex-basis",   r / i - pad-5);
          }
          else {
              $(this).children('ul').children('li').css("flex-basis",  max);
                $(this).children('ul').append("<li class=\"hidden\"><span>  </span></li>");
          }


// });






});












wrapped();

$(window).resize(function() {
   width = $(window).width();
    if (width >= 268) {
        wrapped();

    }
});

function wrapped() {

    //-------------------------------------------------------------------
    var max = 0;
    var A = $('.menu-category > li');



    // console.log($(".menu-category-sub").width())
    // console.log($(elem).width())

    $(".header-top-menu").css("overflow","visible");

    //-------------------------------------------------------------------


   $(".menu-category-sub").children('li').css("flex-basis", 2);

    //-------------------------------------------------------------------


    var offset_top_prev, padm=0;
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
       // console.log(($('.menu-category').offset().left + $('.menu-category').width()));



    $(".menu-category-sub").css("left",$(".menu-category").children('li').first().offset().left);
    $(".menu-category-sub").css("width",$(".menu-category").width()-60);

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