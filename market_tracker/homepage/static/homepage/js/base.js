const initialOffset = 600;
const offsetDecrement = 5;
const p = document.querySelector('.animate');

function animateOffset(offset) {
  offset -= offsetDecrement;
  p.style.strokeDashoffset = offset;
  if (offset >= 0) {
    requestAnimationFrame(() => animateOffset(offset));
  } else {
    p.style.strokeDashoffset = initialOffset;
  }
}


animateOffset(initialOffset);