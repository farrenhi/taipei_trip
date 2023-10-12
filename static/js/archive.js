// const currentURL = 'http://127.0.0.1:3000/booking'
// const currentURL = "http://127.0.0.1:3000/"
const currentURL = 'http://127.0.0.1:3000/thankyou?number=202310121525125497581'

const lastSlashIndex = currentURL.lastIndexOf('/');
const pathAfterLastSlash = currentURL.substring(lastSlashIndex + 1);

console.log(pathAfterLastSlash);

const path_before_questionmark = pathAfterLastSlash.lastIndexOf('?')
const keyword = pathAfterLastSlash.substring(lastSlashIndex);

console.log(keyword); // Output: thankyou

// const firstEnglishCharacters = pathAfterLastSlash.match(/[a-zA-Z]+/)[0];

// console.log(firstEnglishCharacters); // Output: thankyou




// const currentURL = new URL(window.location.href); // Parse the URL
// const pathAfterLastSlash = currentURL.pathname.substring(currentURL.pathname.lastIndexOf('/') + 1);
// console.log(pathAfterLastSlash);



// const currentURL = 'http://127.0.0.1:3000/thankyou?number=202310121525125497581'
// const pathAfterLastSlash = currentURL.pathname.substring(currentURL.pathname.lastIndexOf('/') + 1);
// console.log(pathAfterLastSlash);

// const lastSlashIndex = currentURL.lastIndexOf('/');
// const pathAfterLastSlash = currentURL.substring(lastSlashIndex + 1);
// console.log(pathAfterLastSlash);
