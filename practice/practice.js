// practice.js: the JavaScript exercises from Aryeh's course notebook.
//
// Lines that start with // are COMMENTS. The browser skips them;
// they are notes for people reading the code.
//
// To see console.log messages: open index.html in a browser,
// press F12 (or right-click -> Inspect), and click the "Console" tab.


// ---------------------------------------------------------------
// EXERCISE 1: variables (notebook page 12)
// ---------------------------------------------------------------
// A variable is a labelled box that holds a value.
// "var" makes a new box. The name comes next, then "=", then the value.

var myNumber = 3; // a number (written exactly like in the notebook)

// The notebook stops at "var myString =". A string is TEXT,
// and text always goes inside quote marks:
var myString = "Hello, world"; // a string (text). Change it and reload!

// console.log(...) writes a message in the browser's console.
console.log("myNumber is", myNumber);
console.log("myString is", myString);

// "typeof" tells you what KIND of value is in the box.
console.log("typeof myNumber:", typeof myNumber); // "number"
console.log("typeof myString:", typeof myString); // "string"

// Numbers can do maths. Strings can be joined together with +.
console.log("myNumber + 2 =", myNumber + 2);           // 5
console.log(myString + ", from Jerusalem");           // joins two strings

// Show the same results on the page, so you can see them without the console.
// document.getElementById("...") finds the HTML element with that id.
var variablesBox = document.getElementById("variables-output");
// textContent replaces the text inside the element.
// "\n" means "new line" (the CSS keeps the line breaks).
variablesBox.textContent =
  "myNumber = " + myNumber + "  (typeof: " + typeof myNumber + ")\n" +
  "myString = \"" + myString + "\"  (typeof: " + typeof myString + ")\n" +
  "myNumber + 2 = " + (myNumber + 2);


// ---------------------------------------------------------------
// EXERCISE 2: a button that changes text (notebook page 13, "JS - change")
// ---------------------------------------------------------------
// Step 1: find the two elements on the page by their id.
var message = document.getElementById("message");
var button = document.getElementById("change-button");

// Step 2: keep a counter, so we know how many times it was clicked.
var clicks = 0;

// Step 3: write a FUNCTION: a set of steps with a name, to run later.
function changeText() {
  clicks = clicks + 1; // add one to the counter

  // if / else: do one thing or the other, depending on a test.
  // "%" is the remainder after dividing: clicks % 2 is 1 for odd clicks, 0 for even.
  if (clicks % 2 === 1) {
    message.textContent = "The text changed! (clicks: " + clicks + ")";
  } else {
    message.textContent = "Changed back. (clicks: " + clicks + ")";
  }

  console.log("Button clicked", clicks, "time(s)");
}

// Step 4: tell the button to run changeText every time it is clicked.
// Note: we write changeText WITHOUT () here: we hand over the function,
// we don't run it yet. The browser runs it on each click.
button.addEventListener("click", changeText);
