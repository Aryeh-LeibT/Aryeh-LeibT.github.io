const gitHubApi = "https://api.github.com/users/JonathanGrossmanITC";

// // Fetch function returns a Promise
// // A Promise is a placeholder for a value that does not yet exist

// // console.log(fetch(gitHubApi));

// console.log("Before the fetch");

// fetch(gitHubApi)
//   .then((response) => response.json())
//   .then((data) => {
//     console.log(data);
//     console.log(data["avatar_url"]);
//     console.log(data["login"]);
//     console.log("from inside the Promise");

//     // DOM Manipulations
//     // For instance, get an element by its ID
//     // Set that element's textContent or src value (for an image)
//   });

// console.log("After the fetch");

let dogCEOUrl = "https://dog.ceo/api/breeds/image/random";

// console.log(fetch(dogCEOUrl));

// The fetch function returns a Promise
// A Promise - a placeholder for a value that does not yet exist

// (response) => response.json();

console.log(fetch(dogCEOUrl));
console.log("Before the fetch");

fetch(dogCEOUrl)
  .then((response) => response.json())
  .then((data) => {
    console.log(data["message"]);

    const dogPhoto = document.getElementById("dogPhoto");
    console.log(dogPhoto);
    dogPhoto.src = data["message"];

    console.log("from inside the Promise");
  });

console.log("After the fetch");

const jokesUrl = "https://official-joke-api.appspot.com/random_ten";
const jokesButton = document.getElementById("jokesButton");

const getJokes = () => {
  fetch(jokesUrl)
    .then((response) => response.json())
    .then((data) => {
      const jokesWrapper = document.getElementById("jokesWrapper");
      console.log(data);

      for (let i = 0; i < data.length; i++) {
        const joke = document.createElement("div");
        joke.classList.add("joke");

        const jokeSetup = document.createElement("div");
        jokeSetup.textContent = data[i]["setup"];
        jokeSetup.id = data[i]["setup"];
        jokeSetup.classList.add("joke-setup");

        const jokePunchline = document.createElement("div");
        jokePunchline.textContent = data[i]["punchline"];
        jokePunchline.id = data[i]["punchline"];
        jokePunchline.classList.add("joke-punchline");

        joke.append(jokeSetup, jokePunchline);
        jokesWrapper.append(joke);
      }
    });
};

jokesButton.addEventListener("click", getJokes);
