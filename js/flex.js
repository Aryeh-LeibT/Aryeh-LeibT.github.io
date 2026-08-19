// // The console.log is a very helpful developer tool for JS
// const connectedMessage = "connected";
// console.log("connectedMessage: ", connectedMessage);

// let welcomeMessage = "Hello, ";
// console.log("welcomeMessage: ", welcomeMessage);
// welcomeMessage = "Welcome to ITC!";
// console.log(" updated welcomeMessage: ", welcomeMessage);

// // The var keyword is the old way, you'll see it in code but you should
// // use the let and const keywords instead
// var goodbyeMessage = "goodbye";
// console.log(goodbyeMessage);

// // do this.
// const contactButton = document.getElementById("contactButton");
// console.log(contactButton);
// console.log(contactButton.textContent);
// console.log(contactButton.id);
// console.log(contactButton.classList);

// // Don't do this, it's too many DOM manipulations than what you need
// const contactButtonText = document.getElementById("contactButton").textContent;
// const contactButtonId = document.getElementById("contactButton").id;

// // Examples of Data Types

// // Strings
// const firstName = "Jonathan";
// console.log("name length", firstName.length);
// console.log("name uppercase", firstName.toUpperCase());

// const text1 = "Hello";
// const text2 = "World";
// const text3 = text1.concat(" ", text2, "!");
// console.log(text3);

// const helloSentence = text1 + " " + text2 + "!";
// console.log(helloSentence);

// const originalSentence = "Please visit Microsoft, Microsoft!";
// const copySentence = originalSentence.replace(/Microsoft/g, "W3Schools");
// console.log("originalSentence", originalSentence);
// console.log("copySentence", copySentence);

// const address = "2207";
// const birthday = "7";
// console.log(address + birthday);

// // Numbers
// const favoriteNumber = 170000000000;
// console.log(9 + 8);
// console.log(6.3 + 3.6);
// console.log(6 + 3.6);
// console.log("9" + 9);

// console.log((6 * 7) / 4 + 9);

// // Booleans

// const isOn = true;
// const isOff = false;

// console.log("Boolean: ", isOn, typeof isOn);
// console.log("String: ", isOn.toString(), typeof isOn.toString());

// // string that looks like Boolean
// const trueString = "true";

// // not a Boolean
// // const capsTrue = True;

// // Arrays
// const emptyArray = [];
// const cars = ["Saab", "Volvo", "BMW"];
// const assortedArray = ["Saab", 6, ["p", "q", "r"], { firstName: "Jon" }];

// console.log(cars.length); // 3
// // last index position of cars is 2
// // THE LAST INDEX POSITION OF AN ARRAY IS ALWAYS array.length -1
// // All the things we did with arrays and index
// // positions, we can do with strings too!

// console.log(cars[0]);
// console.log(cars[2]);
// console.log(cars[cars.length - 1]);
// console.log(cars[cars.length - 2]);

// console.log(cars);
// console.log(cars.toString());

// const sportsTeams = "Chiefs";
// console.log(sportsTeams.length);
// console.log(sportsTeams[2]);
// console.log(sportsTeams[sportsTeams.length - 1]);

// let str = "Please locate where 'locate' occurs!";
// let pos = str.indexOf("locate");
// console.log(pos);

// console.log(cars.sort().reverse());
