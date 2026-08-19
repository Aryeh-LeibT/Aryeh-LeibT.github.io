const firstName = "Joe";
const multiplyByThree = (firstNumber, secondNumber) => {
  return (firstNumber + secondNumber) * 3;
};

multiplyByThree(3, 4);
multiplyByThree(5, 6);

// const product = multiplyByThree(7, 8);
// console.log(product * 2);

// Older Syntax
const multiplyByTwo = function () {
  // Function code runs here
  const product = multiplyByThree(100, 8876);
  return product * 2;
};

// console.log(multiplyByTwo());

// const customSplit = (inputString) => {
//   let newArray = [];
//   for (let i = 0; i < inputString.length; i++) {
//     // Add each item from string to array
//     console.log(i, inputString[i]);
//     newArray.push(inputString[i]);
//   }
//   return newArray;
// };

// const sampleString = "thinking about food";

// const splitString = customSplit(sampleString);
// console.log("ours", splitString);

// console.log("theirs", sampleString.split(""));

// const practicingFunctions = (inputString) => {
//   let newArray = [];
//   for (let i = 0; i < inputString.length; i++) {
//     // Add each item from string to array
//     // console.log(i, inputString[i]);
//     if (inputString[i] !== " ") {
//       if (inputString[i] === "d") {
//         newArray.push(inputString[i].toUpperCase());
//       } else if (inputString[i] === "o" || inputString[i] === "O") {
//         newArray.push("p");
//       } else {
//         newArray.push(inputString[i]);
//       }
//     }
//   }
//   return newArray;
// };

// const sampleString = "thinking about foOd";

// const resultsWithoutSpaces = practicingFunctions(sampleString);
// console.log("ours", resultsWithoutSpaces);

const footer = document.getElementById("footer");

const citiesArray = ["tel aviv", "jerusalem", "haifa", "kansas city", "greece"];
let sentenceIntro = "We are located in ";

for (let i = 0; i <= citiesArray.length - 1; i++) {
  // The console log below is a baby (but important) step
  // for developing (a technique)
  // console.log(i, citiesArray[i]);

  if (i === citiesArray.length - 1) {
    sentenceIntro = sentenceIntro + "and " + citiesArray[i] + ".";
  } else {
    sentenceIntro = sentenceIntro + citiesArray[i] + ", ";
  }
}

console.log(sentenceIntro);
footer.textContent = sentenceIntro;
