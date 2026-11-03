// Served at /static/js/main.js and linked from templates/base.html.
// =============================================================

const joinForm = document.getElementById("join-form");
if (joinForm) {
  const button = joinForm.querySelector("button[type=submit]");
  const label = button.textContent;

  joinForm.addEventListener("submit", () => {
    button.disabled = true;
    button.textContent = "Getting your ticket…";
  });

  // the browser may restore the page with the button still disabled.
  window.addEventListener("pageshow", (event) => {
    if (event.persisted) {
      button.disabled = false;
      button.textContent = label;
    }
  });
}