// You can access the DOM in your JavaScript code by creating a script inside your HTML document
// Look in at the bottom of the body in your about.html file for <script src="../js/contact.js"></script>
// By using the script tag to connect to your JS file, you can immediately begin accessing the DOM and modifying HTML elements
// -- The document is an object that represents the HTML document as loaded in the browser
// -- It serves as an entry point for JavaScript into the web page's content
// -- It provides global functionality, like accessing the page's URL or adding new elements, through its built-in methods
// -- Pay special attention to the built-in data type named document
// console.log(document); // --> what do you see in the console?!
// console.log(window.location.pathname);
// -- An example using document's built-in method for getting an HTML element by its id attribute:
// As you learned in the variables lesson, once you access an HTML element, you can save it as a variable and access its attributes
// Here are examples:
// -- Get an existing HTML element and read its attributes
// const title = document.getElementById("title");
// const submitButton = document.getElementById("submitButton");
// console.log(title);
// console.log(submitButton);

// Element objects also have properties and methods

// Commonly used properties for elements include:
// -- id
// -- classList
// -- textContent
// -- You will see online the use of innerText and innerHTML instead of textContent and you should know the differences

// -- Get an element's text
// console.log("title before", title.textContent);
// console.log("title", title.innerHTML);
// console.log("title", title.innerText);

// console.log("submit", submitButton.textContent);
// console.log("submit", submitButton.innerHTML);
// console.log("submit", submitButton.innerText);

// -- Change an element's text
// title.textContent = "Email me";
// console.log("title after", title.textContent);
// title.innerHTML = "Email me";
// console.log("title after", title.innerHTML);
// // title.textText = "Email me";
// // console.log("title after",title.innerText);

// submitButton.textContent = "Go";
// console.log(submitButton.textContent);
// submitButton.innerHTML = "Go";
// console.log(submitButton.innerHTML);
// submitButton.innerText = "Go";
// console.log(submitButton.innerText);

// -- Get an element's CSS class list
// console.log(title.classList);
// console.log(submitButton.classList);

// -- Change an element's CSS class list
// submitButton.classList.add("submit-button");
// console.log("after add", submitButton.classList);
// submitButton.classList.remove("enabled-button");
// console.log("after remove", submitButton.classList[0]);

// -- Get an input's disabled property
// console.log("before change disabled", submitButton.disabled); // false becuase that's the default
// console.log("should say undefined", title.disabled); // undefined because h1 does not have disabled attribute

// -- Change a button's disabled property
// submitButton.disabled = true;
// console.log("after change disabled", submitButton.disabled);
// submitButton.disabled = false;

// A commonly used method for element is: addEventListener

// Use it to turn a DOM object into a listener, access it getElementById and then call the
// addEventListener method;

// const sendForm = () => {
//   // const title = document.getElementById("title");
//   // title.textContent = "My Contact Information";
//   console.log("First Name: ", firstName.value);
//   console.log("Last Name: ", lastName.value);
// };

// submitButton.addEventListener("click", sendForm);

// When calling the addEventListener method, you need to pass to it two arguments:
// -- The name of the type of event to listen for
// -- A function that will be triggered when the event happens
// When passing the function in as an argument, it's good practice to pass in the name of the function instead of the entire function definition
// -- Example: submitButton.addEventListener('click', sendForm)
// -- Note: Don't use HTML attributes to listen for events <div onClick="...">Submit</div>

// Inside the listener's function, you can access the event object
// The event object makes available to you the details of the event,
// You will commonly use the event object to get and modify the attributes of an HTML element
// The event object is automatically passed to event handlers and is the first argument in your function definition
// In examples online, you will see the event object represented in code usually as event, e, or evt
// const sendFormWithEvent = (e) => {
//   console.log("Form sent event:", e);
//   console.log(e.target);
//   console.log(e.target.value);
//   console.log(e.target.textContent);
//   console.log(e.target.id);
//   console.log(e.target.classList);
// };
// submitButton.addEventListener("click", sendFormWithEvent);

// Live Coding Tasks
const firstName = document.getElementById("firstName");
const lastName = document.getElementById("lastName");
const file = document.getElementById("file");
const radio = document.getElementById("radio");
const submitButton = document.getElementById("submitButton");
const formWrapper = document.getElementById("form");
submitButton.disabled = true; // disables button on page load

const sendForm = () => {
  // This is one approach . . .
  // if (
  //   firstName.value === "" ||
  //   lastName.value === "" ||
  //   file.value === "" ||
  //   radio.checked === false
  // ) {
  //   console.log("Your form is incomplete");
  // } else {
  //   console.log("Your form is COMPLETE!");
  //   console.log("First Name: ", firstName.value);
  //   console.log("Last Name: ", lastName.value);
  //   console.log("File: ", file.value);
  //   console.log("Radio: ", radio.checked);
  // }
  // This is another approach . . .
  if (firstName.value && lastName.value && file.value && radio.checked) {
    // Make form look completed
    formWrapper.classList.add("form-completed");
    formWrapper.classList.remove("form");

    // Prints form values to console
    console.log("Your form is COMPLETE!");
    console.log("First Name: ", firstName.value);
    console.log("Last Name: ", lastName.value);
    console.log("File: ", file.value);
    console.log("Radio: ", radio.checked);
  } else if (firstName.value || lastName.value || file.value || radio.checked) {
    // code goes below
    console.log("Something is missing, but off to a good start.");
  } else {
    console.log("Your form is totally incomplete.");
  }
};

submitButton.addEventListener("click", sendForm);

const formInput = () => {
  console.log("typing...");
  // Checks if form is complete
  if (firstName.value && lastName.value && file.value && radio.checked) {
    // Enable submit button
    submitButton.disabled = false;
    // Can also add and remove items from the submitButton classList
  } else {
    // Disable submit button
    submitButton.disabled = true;
    // Can also add and remove items from the submitButton classList
  }
  // console.log(submitButton.disabled);
  // if (submitButton.disabled === false) {
  //   // alert("Whoa buddy, it's false");
  //   const title = document.getElementById("title");
  //   title.textContent = "Jeremy, for the win.";
  //   submitButton.disabled = true;
  // } else if (submitButton.disabled === true) {
  //   // alert("Zecharia, for the win.");
  //   console.log(firstName.value + " " + lastName.value);
  //   submitButton.disabled = false;
  // }
  // console.log("First Name: ", firstName.value);
  // console.log("Last Name: ", lastName.value);
};

firstName.addEventListener("input", formInput);
lastName.addEventListener("input", formInput);
file.addEventListener("input", formInput);
radio.addEventListener("input", formInput);
