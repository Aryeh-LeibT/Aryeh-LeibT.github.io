console.log("from index.js");

const url = "https://type.fit/api/quotes";

const savedQuotes = JSON.parse(sessionStorage.getItem("quotes"));
// const savedQuotes = JSON.parse(localStorage.getItem("quotes"));
console.log(savedQuotes);
if (!savedQuotes) {
  sessionStorage.setItem("quotes", JSON.stringify([]));
}

const saveQuote = (event) => {
  savedQuotes.push(event.target.textContent);
  sessionStorage.setItem("quotes", JSON.stringify(savedQuotes));

  //   localStorage.setItem("quotes", JSON.stringify(savedQuotes));
};

fetch(url)
  .then((response) => response.json())
  .then((data) => {
    const quotesWrapper = document.getElementById("quotesWrapper");
    for (let i = 0; i <= 9; i++) {
      const quoteItem = document.createElement("div");
      quoteItem.classList.add("quote-item");

      const quote = document.createElement("div");
      quote.textContent = data[i]["text"];
      quote.classList.add("quote");
      quote.addEventListener("click", saveQuote);

      const author = document.createElement("div");
      author.textContent = data[i]["author"];
      author.classList.add("author");

      quoteItem.append(quote, author);
      quotesWrapper.append(quoteItem);
    }
  });

const pathnameURL = window.location.pathname;

// One way to do this:
const pathnameURLArray = pathnameURL.split("/");
const lastIndex = pathnameURLArray.length - 1;
const lastItem = pathnameURLArray[lastIndex];
const titleFromUrl = lastItem.replace(".html", "").replace("_", " ");

// Another way to do this:
// const titleFromUrl = pathnameURL
//   .replace("/Users/jonathangrossman/Desktop/first_steps_april_live/", "")
//   .replace(".html", "")
//   .replace("html/", "")
//   .replace("_", " ");

console.log(titleFromUrl);

const titleHtml = document.getElementById("title");
titleHtml.textContent = titleFromUrl;
console.log(titleFromUrl);
