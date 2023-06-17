const pass_fields = document.querySelectorAll(".pass-key");
const showBtns = document.querySelectorAll(".show");

showBtns.forEach(function(showBtn, index) {
  showBtn.addEventListener("click", function() {
    const pass_field = pass_fields[index];
    if (pass_field.type === "password") {
      pass_field.type = "text";
      showBtn.textContent = "HIDE";
      showBtn.style.color = "#C38748";
    } else {
      pass_field.type = "password";
      showBtn.textContent = "SHOW";
      showBtn.style.color = "#222";
    }
  });
});