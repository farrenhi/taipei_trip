function load_test() {
    console.log("js file from static folder");
}


// Assuming you have an HTML element with class 'carousel' to append the images
const carousel = document.querySelector('.sight_box_images');

// fetch('http://127.0.0.1:3000/api/attraction/10')
//   .then(response => response.json())
//   .then(data => {
//     const images = data.data.images;
    
//     images.forEach((imageUrl, index) => {
//       const imgElement = document.createElement('img');
//       imgElement.src = imageUrl;
//       imgElement.alt = `Image ${index + 1}`;
//       carousel.appendChild(imgElement);
//     });
//   })
//   .catch(error => console.error('Error fetching data:', error));

document.addEventListener('DOMContentLoaded', () => {
    fetch('http://127.0.0.1:3000/api/attraction/10')
      .then(response => response.json())
      .then(data => {
        const _images = data.data.images;
        const carousel = document.querySelector('.sight_box_images'); // Assuming .sight_box_images is the container for the images
        
        _images.forEach((imageUrl, index) => {
          const imgElement = document.createElement('img');
          imgElement.src = imageUrl;
          imgElement.alt = `Image ${index + 1}`;
          if (index === 0) { // Set the opacity of the first image to 1
            imgElement.style.opacity = '1';
          }
          carousel.appendChild(imgElement);
        });
      })
      .catch(error => console.error('Error fetching data:', error));
});

  

let currentImage = 0;

document.querySelector('.left-button').addEventListener('click', () => {
    let images = document.querySelectorAll('.sight_box_images img');
    console.log(currentImage);
    images[currentImage].style.opacity = '0';
    currentImage = (currentImage - 1 + images.length) % images.length;
    images[currentImage].style.opacity = '1';
});

document.querySelector('.right-button').addEventListener('click', () => {
    let images = document.querySelectorAll('.sight_box_images img');
    console.log(images);
    console.log(currentImage);
    images[currentImage].style.opacity = '0';
    currentImage = (currentImage + 1) % images.length;
    images[currentImage].style.opacity = '1';
});