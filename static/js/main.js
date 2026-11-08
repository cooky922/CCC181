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

// Clean the name fields when the user leaves something like: "  maria   DELA cruz " -> "Maria Dela Cruz".
// The server does the same again, so this is only a preview for the user.
document.querySelectorAll("[data-clean-name]").forEach((input) => {
  input.addEventListener("blur", () => {
    input.value = input.value
      .trim()
      .replace(/\s+/g, " ")
      .toLowerCase()
      .replace(/(^|[^\p{L}])(\p{L})/gu, (_, before, letter) => before + letter.toUpperCase());
  });
});