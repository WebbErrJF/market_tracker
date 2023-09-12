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

document.addEventListener('DOMContentLoaded', function() {
  var body = document.querySelector('body');
  body.style.overflow = 'hidden';
});