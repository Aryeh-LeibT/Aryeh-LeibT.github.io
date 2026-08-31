const footerMessage = "this page was built using:";
console.log(footerMessage);

const languageArray = ["HTML", "CSS", "JavaScript"];
console.log(languageArray);

const GITHUB_URL = "https://api.github.com/users/";
const GITHUB_USERNAME = "Aryeh-LeibT";
console.log(GITHUB_URL + GITHUB_USERNAME);

const firstName = document.getElementById("firstName");
const lastName = document.getElementById("lastName");
const email = document.getElementById("email");
const comment = document.getElementById("comment");
const submitButton = document.getElementById("submitButton");
const file = document.getElementById("file");
const radio = document.getElementById("radio");

const sendForm = () => {
  console.log("submit", {
    firstName: firstName && firstName.value,
    lastName: lastName && lastName.value,
    email: email && email.value,
    comment: comment && comment.value,
  });
};

const formInput = () => {
  if (!submitButton) return;
  const ready =
    firstName &&
    firstName.value &&
    lastName &&
    lastName.value &&
    email &&
    email.value &&
    comment &&
    comment.value &&
    radio &&
    radio.checked;
  submitButton.disabled = !ready;
};

if (submitButton) {
  submitButton.disabled = true;
  submitButton.addEventListener("click", sendForm);
  [firstName, lastName, email, comment, file, radio].forEach((el) => {
    if (el) el.addEventListener("input", formInput);
    if (el) el.addEventListener("change", formInput);
  });
}
