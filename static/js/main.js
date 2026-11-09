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

// Tidy the name fields when the user leaves them: "  maria   DELA cruz " -> "Maria Dela Cruz".
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


let formToConfirm = null;
document.addEventListener("submit", (event) => {
  const form = event.target.closest("form[data-confirm]");
  if (!form || form.dataset.confirmed === "yes") return;
  event.preventDefault();
  event.stopPropagation();

  const popup = document.getElementById("confirmModal");
  if (!popup || !window.bootstrap) {
    if (confirm(form.dataset.confirm)) { form.dataset.confirmed = "yes"; form.requestSubmit(); delete form.dataset.confirmed; }
    return;
  }
  formToConfirm = form;
  document.getElementById("confirmModalBody").textContent = form.dataset.confirm;
  document.getElementById("confirmModalYes").textContent = form.dataset.confirmLabel || "Delete";
  bootstrap.Modal.getOrCreateInstance(popup).show();
}, true);

const confirmYes = document.getElementById("confirmModalYes");
if (confirmYes) {
  confirmYes.addEventListener("click", () => {
    const form = formToConfirm;
    formToConfirm = null;
    bootstrap.Modal.getInstance(document.getElementById("confirmModal")).hide();
    if (form) {
      form.dataset.confirmed = "yes";
      form.requestSubmit();
      delete form.dataset.confirmed;
    }
  });
}