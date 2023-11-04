window.onbeforeunload = function() {
  window.scrollTo(0, 0);
}

jQuery(document).ready(function($) {

  $(window).load(function() {
    $('.loading').delay(2000).fadeOut('slow', function() {
      $(this).remove();
    });
    setTimeout(function() {
      $('.landing').addClass('loaded');
    }, 2000);
    setTimeout(function() {
      $('body').addClass('loaded');
    }, 2000);

  });

});