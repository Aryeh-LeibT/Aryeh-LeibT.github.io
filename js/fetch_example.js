// const URL = "https://dog.ceo/api/breeds/image/random";

// Fetch function returns a promise
// console.log(fetch(URL));

// Template for basic fetch function
// fetch(URL)
//   .then((response) => response.json())
//   .then((data) => console.log(data));

// Example of the timing of the fetch function
// console.log("Starting"); // first
// const URL = "https://dog.ceo/api/breeds/image/random";

// fetch(URL)
//   .then((response) => {
//     console.log("Got the HTTP response)"); // third
//     return response.json();
//   })
//   .then((data) => {
//     console.log("Got the data: ", data); // fourth
//   })
//   .catch((error) => {
//     console.log(
//       "There has been a problem with your fetch operation: " + error.message
//     );
//   });

// console.log("All done!"); // second

// Example of object
// const responseObject = {
//   message: "https://images.dog.ceo/breeds/dachshund/dachshund-1018409_640.jpg",
//   status: "success",
// };

// // console.log(responseObject.message);
// // console.log(responseObject["message"]);

// console.log(responseObject.status);
// console.log(responseObject["status"], responseObject["message"]);

// Compare syntax for arrays to objects
// const newArray = ["sprite", "pepsi", "coco-cola"];
// newArray[0];

const catURL = "https://api.thecatapi.com/v1/images/search";

let smallPhotoTitle = document.getElementById("smallPhotoTitle");
smallPhotoTitle.textContent = "Checking for cat photo . . .";

fetch(catURL)
  .then((response) => response.json())
  .then((data) => {
    const catPhoto = document.getElementById("catPhoto");
    // console.log(catPhoto.src);
    // console.log(data[0]["url"]);
    // catPhoto.src = data[0]["url"];
    // const height = data[0]["height"];

    const width = data[0]["width"];
    console.log("width: ", width);
    if (width > 500) {
      smallPhotoTitle.textContent = "It's a cat!";
      catPhoto.src = data[0]["url"];
    } else {
      smallPhotoTitle.textContent = "Mr. Crews";
    }
  });

const gitHubURL = "https://api.github.com/users/JonathanGrossmanITC/followers";
console.log(fetch(gitHubURL));
// fetch(gitHubURL)
//   .then((response) => response.json())
//   .then((data) => {
//     const navbar = document.getElementById("navbar");
//     for (let i = 0; i < data.length; i++) {
//       const newElement = document.createElement("div");
//       newElement.textContent = data[i]["login"];
//       newElement.id = data[i]["login"];
//       navbar.append(newElement);
//     }
//   });
