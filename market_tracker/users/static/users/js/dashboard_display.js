document.addEventListener('DOMContentLoaded', function() {
    var header = document.querySelector('header');
    var background_image = document.querySelector('.landing');
    if (header) {
        header.style.display = 'none';
    }
    if (background_image) {
        background_image.style.backgroundImage = 'none';
    }
});