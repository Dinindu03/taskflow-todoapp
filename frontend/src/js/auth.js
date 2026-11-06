const form = document.querySelector("#auth-form");
const nameField = document.querySelector("#name-field");
const nameInput = document.querySelector("#name");
const emailInput = document.querySelector("#email");
const passwordInput = document.querySelector("#password");
const passwordToggle = document.querySelector("#password-toggle");
const modeToggle = document.querySelector("#mode-toggle");
const submitButton = document.querySelector("#submit-button");
const submitLabel = document.querySelector("#submit-label");
const submitSpinner = document.querySelector("#submit-spinner");
const message = document.querySelector("#form-message");
const title = document.querySelector("#form-title");
const eyebrow = document.querySelector("#form-eyebrow");
const description = document.querySelector("#form-description");
const switchCopy = document.querySelector("#switch-copy");

let isSignup = false;

function showMessage(text, type) {
  message.textContent = text;
  message.className = `mb-6 rounded-xl border px-4 py-3 text-sm ${
    type === "success"
      ? "border-emerald-200 bg-emerald-50 text-emerald-700"
      : "border-red-200 bg-red-50 text-red-700"
  }`;
}

function clearMessage() {
  message.textContent = "";
  message.className = "mb-6 hidden rounded-xl border px-4 py-3 text-sm";
}

function setFieldError(field, text) {
  const error = document.querySelector(`#${field}-error`);
  error.textContent = text;
  error.classList.toggle("hidden", !text);
}

function clearFieldErrors() {
  ["name", "email", "password"].forEach((field) => setFieldError(field, ""));
}

function validateForm() {
  clearFieldErrors();
  let valid = true;
  const email = emailInput.value.trim();
  const password = passwordInput.value;

  if (isSignup && !nameInput.value.trim()) {
    setFieldError("name", "Please enter your name.");
    valid = false;
  }
  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    setFieldError("email", "Enter a valid email address.");
    valid = false;
  }
  if (password.length < 8) {
    setFieldError("password", "Password must be at least 8 characters.");
    valid = false;
  }
  return valid;
}

function setMode(signup) {
  isSignup = signup;
  nameField.classList.toggle("hidden", !signup);
  nameInput.required = signup;
  passwordInput.autocomplete = signup ? "new-password" : "current-password";
  eyebrow.textContent = signup ? "Get started" : "Welcome back";
  title.textContent = signup ? "Create your account" : "Sign in to your account";
  description.textContent = signup ? "Start organizing your work today." : "Continue where you left off.";
  submitLabel.textContent = signup ? "Create account" : "Sign in";
  switchCopy.textContent = signup ? "Already have an account?" : "Don't have an account?";
  modeToggle.textContent = signup ? "Sign in" : "Create one";
  document.title = `TaskFlow | ${signup ? "Sign up" : "Sign in"}`;
  clearFieldErrors();
  clearMessage();
}

function setLoading(loading) {
  submitButton.disabled = loading;
  submitSpinner.classList.toggle("hidden", !loading);
  submitLabel.textContent = loading ? (isSignup ? "Creating account..." : "Signing in...") : (isSignup ? "Create account" : "Sign in");
}

async function readError(response) {
  try {
    const body = await response.json();
    if (body.error?.message) return body.error.message;
    if (typeof body.detail === "string") return body.detail;
    if (Array.isArray(body.detail)) return "Please check the highlighted fields.";
  } catch {
    // Fall through to the generic message when the server does not return JSON.
  }
  return "Something went wrong. Please try again.";
}

async function submitAuth(event) {
  event.preventDefault();
  if (!validateForm()) return;

  setLoading(true);
  clearMessage();
  const payload = {
    email: emailInput.value.trim(),
    password: passwordInput.value,
  };
  if (isSignup) payload.name = nameInput.value.trim();

  try {
    const response = await fetch(`/api/auth/${isSignup ? "signup" : "signin"}`, {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      showMessage(await readError(response), "error");
      return;
    }

    form.reset();
    if (isSignup) setMode(false);
    if (!isSignup) {
      window.location.href = "/dashboard.html";
      return;
    }
    showMessage("Account created. You can now sign in.", "success");
  } catch {
    showMessage("Unable to reach TaskFlow. Check that the API is running and try again.", "error");
  } finally {
    setLoading(false);
  }
}

passwordToggle.addEventListener("click", () => {
  const visible = passwordInput.type === "text";
  passwordInput.type = visible ? "password" : "text";
  passwordToggle.textContent = visible ? "Show" : "Hide";
  passwordToggle.setAttribute("aria-pressed", String(!visible));
});

modeToggle.addEventListener("click", () => setMode(!isSignup));
form.addEventListener("submit", submitAuth);
setMode(false);
