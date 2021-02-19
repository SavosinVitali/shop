$(document).ready(function(){



$('img[src$=".svg"]').each(function() {
        var $img = jQuery(this);
        var imgURL = $img.attr('src');
        var attributes = $img.prop("attributes");

        $.get(imgURL, function(data) {
            // Get the SVG tag, ignore the rest
            var $svg = jQuery(data).find('svg');

            // Remove any invalid XML tags
            $svg = $svg.removeAttr('xmlns:a');

            // Loop through IMG attributes and apply on SVG
            $.each(attributes, function() {
                $svg.attr(this.name, this.value);
            });

            // Replace IMG with SVG
            $svg.attr('height', 25);
            $svg.attr('width', 25);
            $img.replaceWith($svg);
        }, 'xml');
    });









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