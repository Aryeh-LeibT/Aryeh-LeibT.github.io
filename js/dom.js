console.log(document);

const firstName = document.getElementById("firstName");
// console.log(firstName);
// console.log(firstName.classList);
// console.log(firstName.id);
// console.log(firstName.type);
// console.log(firstName.placeholder);
const lastName = document.getElementById("lastName");
const submitButton = document.getElementById("submitButton");
const checkbox = document.getElementById("checkbox");
const fileInput = document.getElementById("fileInput");

const onInput = () => {
  if (
    firstName.value !== "" &&
    lastName.value !== "" &&
    checkbox.checked === true &&
    fileInput.value !== ""
  ) {
    submitButton.disabled = false;

    // Delete console logs in a real project, but we left them in here
    // to remind you of the dev techniques we use

    // console.log("first: ", firstName.value);
    // console.log("last: ", lastName.value);
    // console.log(submitButton.disabled);
    // console.log(checkbox.checked);
    // console.log(fileInput.value);
  }
};

firstName.addEventListener("input", onInput);
lastName.addEventListener("input", onInput);
checkbox.addEventListener("input", onInput);
fileInput.addEventListener("input", onInput);

const submitForm = () => {
  // Delete console logs in a real project, but we left them in here
  // to remind you of the dev techniques we use
  // console.log("from the form button");
  console.log(submitButton.disabled);
  console.log("First Name: ", firstName.value);
  console.log("Last Name: ", lastName.value);
  console.log("checkbox: ", checkbox.checked);
  console.log("file: ", fileInput.value);
};

submitButton.addEventListener("click", submitForm);

const image = document.getElementById("image");
const previousButton = document.getElementById("previousButton");
const nextButton = document.getElementById("nextButton");
console.log(image);
console.log(previousButton);
console.log(nextButton);

const arrayOfImages = ["fish_icon.png", "turtle.jpg", "cartoon_soccer.png"];
let i = 0;

const moveBackwards = () => {
  nextButton.disabled = false;

  if (i > 0) {
    i--;
    image.src = "../images/" + arrayOfImages[i];
  }

  if (i === 0) {
    previousButton.disabled = true;
  }
};

const moveForwards = () => {
  previousButton.disabled = false;

  if (i < arrayOfImages.length - 1) {
    i++;
    image.src = "../images/" + arrayOfImages[i];
  }

  if (i === arrayOfImages.length - 1) {
    nextButton.disabled = true;
  }
};

previousButton.addEventListener("click", moveBackwards);
nextButton.addEventListener("click", moveForwards);

// const namesArray = ["aryeh", "alla", "baoz", "benny", "yehuda"];

// for (let i = 0; i <= namesArray.length - 1; i++) {
//   console.log(i, namesArray[i].toUpperCase());
// }

// console.log("hi, from line 97");

// for (let i = 0; i < namesArray.length; i++) {
//   // code applied to each item in collection
//   console.log(namesArray[i]);

//   // This is what the browser sees / does
//   // console.log(namesArray[0]);  first time through aryeh
//   // console.log(namesArray[1]);  second time through alla
//   // console.log(namesArray[2]);  third time through boaz
//   // console.log(namesArray[3]);  fourth time through benny
// }

// Same way of writing the above, but different condition (same result)
// for (let i = 0; i <= namesArray.length - 1; i++) {
// }

// const namesObject = {
//   studentOne: "aryeh",
//   studentTwo: "alla",
//   studentThree: "boaz",
// };

// const otherNamesObject = {
//   studentOne: "inbar",
//   studentTwo: "michael",
//   studentThree: "penina",
// };

// const hour = 7;
// let greeting;

// if (hour < 18) {
//   greeting = "Good day";
// } else if (hour === 19) {
//   greeting = "nineteen";
// } else if (hour === 20) {
//   greeting = "twenty";
// } else if (hour === 20) {
//   greeting = "twenty one";
// } else {
//   greeting = "catch all";
// }
// console.log(greeting);

// if (hour === 7) {
//   greeting = "7";
// }
// console.log(greeting);

// if (hour === 7) {
//   greeting = "seven";
// }

// console.log(greeting);

console.log(7 < 9);

const x = 8;
const y = 9;

if (x > y && x === 8) {
  console.log(x > y);
} else {
  const txt1 = "John";
  const txt2 = "Doe";
  // const txt3 = txt1 + txt2;
  const txt3 = `Who is ${txt1} ${txt2}?`;
  console.log(txt3);
}

const citiesArray = [
  "tel aviv",
  "jerusalem",
  "haifa",
  "kansas city",
  "Paradise",
];
let introAlla = "Alla is located in ";
let introAryeh = "Aryeh is located in ";
let introNobody = "Nobody here is located in ";
let introJon = "Jon is located in ";
let introEveryone = "We are all located in";

for (let i = 0; i <= citiesArray.length - 1; i++) {
  // The console log below is a baby (but important) step
  // for developing (a technique)
  // console.log(i, citiesArray[i]);
  // if (citiesArray[i] === "tel aviv") {
  //   // do something
  //   console.log(introAlla + citiesArray[i]);
  // } else if (citiesArray[i] === "jerusalem") {
  //   // do something else
  //   console.log(introAryeh + citiesArray[i]);
  // } else if (citiesArray[i] === "haifa") {
  //   // do something else
  //   console.log(introNobody + citiesArray[i]);
  // } else if (citiesArray[i] === "kansas city") {
  //   // do something else
  //   console.log(introJon + citiesArray[i]);
  // } else if (citiesArray[i] === "tel aviv") {
  //   // do something
  //   console.log(`${introEveryone} ${citiesArray[i]}`);
  // } else {
  //   // do something
  //   console.log(`${introEveryone} ${citiesArray[i]}`);
  // }
  // if (citiesArray[i] === "tel aviv") {
  //   // do something
  //   console.log(introAlla + citiesArray[i]);
  // }
  // if (citiesArray[i] === "jerusalem") {
  //   // do something else
  //   console.log(introAryeh + citiesArray[i]);
  // }
  // if (citiesArray[i] === "haifa") {
  //   // do something else
  //   console.log(introNobody + citiesArray[i]);
  // }
  // if (citiesArray[i] === "kansas city") {
  //   // do something else
  //   console.log(introJon + citiesArray[i]);
  // }
  // if (citiesArray[i] === "Paradise") {
  //   // do something
  //   console.log(`${introEveryone} ${citiesArray[i]}`);
  // }
}

const citiesArrayTwo = [
  "tel aviv",
  "jerusalem",
  "haifa",
  "kansas city",
  "Paradise",
];
let sentenceIntro = "We are all located in ";

for (let i = 0; i <= citiesArrayTwo.length - 1; i++) {
  // The console log below is a baby (but important) step
  // for developing (a technique)
  // console.log(i, citiesArray[i]);

  sentenceIntro = sentenceIntro + citiesArray[i].toUpperCase();
}

console.log(sentenceIntro);
