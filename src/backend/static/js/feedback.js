// src/backend/static/js/feedback.js
(function () {
  const form = document.getElementById("feedbackForm");
  if (!form) return;

  const fields = {
    name: {
      el: document.getElementById("name"),
      err: document.getElementById("nameErr"),
      messages: {
        valueMissing: "Please enter your name.",
        tooShort: "Name must be at least 2 characters.",
        tooLong: "Name must be 120 characters or fewer.",
        patternMismatch: "Use letters, spaces, and periods only."
      }
    },
    phone: {
      el: document.getElementById("phone"),
      err: document.getElementById("phoneErr"),
      messages: {
        valueMissing: "Please enter your phone number.",
        tooShort: "Phone number looks too short.",
        tooLong: "Phone number looks too long.",
        patternMismatch: "Use a valid international format (+880..., +1..., etc)."
      }
    },
    email: {
      el: document.getElementById("email"),
      err: document.getElementById("emailErr"),
      messages: {
        typeMismatch: "That email doesn’t look valid.",
        tooLong: "Email must be 160 characters or fewer."
      }
    },
    message: {
      el: document.getElementById("message"),
      err: document.getElementById("msgErr"),
      messages: {
        tooLong: "Message must be 1000 characters or fewer."
      }
    }
  };

  function showError(field) {
    const { el, err, messages } = field;
    err.textContent = "";
    if (el.validity.valid) return true;

    let msg = "";
    const v = el.validity;
    if (v.valueMissing) msg = messages.valueMissing;
    else if (v.tooShort) msg = messages.tooShort;
    else if (v.tooLong) msg = messages.tooLong;
    else if (v.patternMismatch) msg = messages.patternMismatch;
    else if (v.typeMismatch) msg = messages.typeMismatch;
    else msg = "Please correct this field.";

    err.textContent = msg;
    return false;
  }

  Object.values(fields).forEach(({ el }) => {
    el.addEventListener("input", () => showError(fields[el.id]));
    el.addEventListener("blur", () => showError(fields[el.id]));
  });

  form.addEventListener("submit", (e) => {
    let valid = true;
    Object.values(fields).forEach((f) => {
      if (!showError(f)) valid = false;
    });
    if (!valid) {
      e.preventDefault();
      const firstInvalid = Object.values(fields).find((f) => !f.el.validity.valid);
      if (firstInvalid) firstInvalid.el.focus();
    }
  });
})();