// const foodArray = ["egg", "", "egg", "tomato", "lemon"];
// const otherArray = ["apple"];
// index of last item in array is: foodArray.length - 1 (here it's 4)
// length of array is how many items are in the array

// for (let i = 0; i < foodArray.length; i++) {
//   if (foodArray[i] === "egg") {
//     console.log("hi", i, foodArray[i]);
//   } else if (foodArray[i] === "") {
//     console.log("your handful is empty");
//   } else if (foodArray[i] === "") {
//     console.log("your handful is empty");
//   } else if (foodArray[i] === "") {
//     console.log("your handful is empty");
//   } else if (foodArray[i] === "") {
//     console.log("your handful is empty");
//   } else {
//     console.log("bye");
//   }

//   if (foodArray[i] === "egg") {
//     console.log("hi", i, foodArray[i]);
//   }

//   if (foodArray[i] === "lime") {
//     console.log("hi", i, foodArray[i]);
//   }

//   if (foodArray[i] === "soda") {
//     console.log("hi", i, foodArray[i]);
//   }

//   if (foodArray[i] === "egg") {
//     console.log("hi", i, foodArray[i]);
//   } else {
//     console.log("bye");
//   }
// }

// const someFunction = () => {
//   // here is the function code
//   for (let i = 0; i < foodArray.length; i++) {
//     console.log("hi", i, foodArray[i]);
//   }
// };

// someFunction();

// While loop
// x = 22;
// while (x > 10) {
//   x--;
//   console.log(x);
// }

// Comparison examples
// const numberFive = 5;
// const stringFive = "5";
// const otherNumberFive = 5;

// if (numberFive == stringFive) {
//   console.log("five ==");
// }
// if (numberFive === stringFive) {
//   console.log("five ==");
// }

// if (numberFive == otherNumberFive) {
//   console.log("five ==");
// }

// if (numberFive === otherNumberFive) {
//   console.log("five ===");
// }

// Logical examples

// const numberFive = 5;
// const stringFive = "5";
// const otherNumberFive = 5;
// const emptyVariable = "";
// const emptyNumber = 0;
// const emptyArray = [];

// if (!otherNumberFive) {
//   console.log("are we there yet?");
// }

// if (numberFive == stringFive && numberFive == 5) {
//   console.log("five ==");
// }
// if (numberFive === stringFive || numberFive == 5) {
//   console.log("five ==");
// }

// if (numberFive == otherNumberFive) {
//   console.log("five ==");
// }

// if (numberFive === otherNumberFive) {
//   console.log("five ===");
// }

// Example of an arrow function
() => {
  // code goes here
};

// const greetUser = () => {
//   // console.log("Welcome to ITC, " + username);
//   console.log("You're born on: ", birthday);
// };

const greetUserWithBirthday = (username, birthday) => {
  console.log("Welcome to ITC, " + username);
  console.log("You're born on: ", birthday);
};

greetUserWithBirthday("Karin", "August");

// const callsGreetUser = () => {
//   greetUser("Tzafrir");
// };

// const greetUser = (username = "Jack") => {
//   console.log("Welcome to ITC, " + username);
// };

// callsGreetUser();

// console.log("before", message);
const greetUser = (username = "Jack") => {
  let message = "Welcome to ITC, " + username;

  // console.log("Welcome to ITC, " + username);
  return message;
  // Code below the return statement doesn't run
  const nameLength = username.length;
  console.log("won't see me in the console.", nameLength);
};

// console.log("after", message);

greetUser("Paul"); //"Welcome to ITC, Paul"

const paul_greeting = greetUser("Paul");
const tzafrir_greeting = greetUser("Tzafrir");

// Examples how calling functions that return a value
console.log("p-function return value: ", greetUser("Paul"));
console.log("p-function return value: ", paul_greeting);
console.log("t-function return value: ", tzafrir_greeting);

const sendMessage = () => {
  const message = "Hello World";
  console.log(message);
  return message;
};

const helloMessage2 = sendMessage();
console.log(helloMessage2);

const buildDinnerSentence = (array) => {
  // code goes here
  let intro = "When I'm really hungry, I like to eat ";

  for (let i = 0; i < array.length; i++) {
    if (i !== array.length - 1 && i !== array.length - 2) {
      // If i is NOT the last item in the array,
      //just add the item to the intro
      intro = intro + array[i] + ", ";
    } else if (i === array.length - 2) {
      // Checks for SECOND-TO-LAST ITEM in the array,
      // and doesn't add a comma if true
      intro = intro + array[i] + " ";
    } else {
      // If i is the last item in the array,
      // add the word "or" and then the item to the intro
      intro = intro + "or " + array[i] + ".";
    }
  }
  return intro;
};

const foodArray = ["pasta", "pizza", "salad", "chocolate ice cream"];
const dinnerSentence = buildDinnerSentence(foodArray);
console.log(dinnerSentence);

const breakfastArray = [
  "peanut butter",
  "bananas",
  "orange",
  "chocolate ice cream",
  "yogurt",
];
const breakfastSentence = buildDinnerSentence(breakfastArray);
console.log(breakfastSentence);
