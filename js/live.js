const footer = document.getElementById("footer");

let intro = "My favorite places are: ";
const placesArray = [
  "Rome",
  "Jerusalem",
  "Mexico",
  "Kansas City",
  "Tel Aviv",
  "London",
];

const theOtherPlaceArray = ["Bedroom"];

const buildFooterMessage = (array) => {
  for (let i = 0; i < array.length; i++) {
    // Check if "i" isn't last or second-to-last item
    if (i === array.length - 1) {
      // Check if last item
      intro += "and " + array[i];
    } else if (i === array.length - 2) {
      // Check if second-to-last
      intro += array[i] + " ";
    } else {
      // For everything else
      intro += array[i] + ", ";
    }
  }
};

buildFooterMessage(placesArray);
// buildFooterMessage(theOtherPlaceArray);

const urlPath = window.location.pathname;
const thisHTMLPage = urlPath.replace(
  "/Users/jonathangrossman/Desktop/live_first_steps/html/",
  ""
);
const pageName = thisHTMLPage.replace(".html", "");
const selectedPageLink = document.getElementById(pageName);
console.log(selectedPageLink);
selectedPageLink.classList.add("selected-navbar-item");

// selectedPageLink.classList.remove("navbar-item");

// Another possible (but unfinished) approach to get navbar items
// const navbarLinks = document.getElementsByClassName("navbar-item");
// for (let i = 0; i < navbarLinks.length; i++) {
//   if (pageName === "final_day") {
//     console.log("final", pageName);
//   } else if (pageName === "about") {
//     console.log("about", pageName);
//   }
// }
