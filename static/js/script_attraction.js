// function load_test() {
//     console.log("good load!");
// }

// Assuming you have an HTML element with class 'carousel' to append the images
const carousel = document.querySelector('.sight_box_images');

function getAttractionIdFromUrl() {
    var url = window.location.href; // Get the current URL
    var parts = url.split('/'); // Split the URL by '/'
    var id = parts[parts.length - 1]; // Get the last part of the URL
    return id;
}

var attractionId = getAttractionIdFromUrl();

document.addEventListener('DOMContentLoaded', () => {
    fetch('/api/attraction/' + attractionId)
      .then(response => response.json())
      .then(data => {
        const _images = data.data.images;
        const carousel = document.querySelector('.sight_box_images'); // Assuming .sight_box_images is the container for the images
        
        const sight_name = data.data.name;
        const mrt = data.data.mrt;
        const category = data.data.category;
        const description = data.data.description;
        const address = data.data.address;
        const transport = data.data.transport;

        const sight_name_box = document.querySelector('.rightbox1');
        sight_name_box.textContent = sight_name;

        const mrt_box = document.querySelector('.rightbox2');
        mrt_box.textContent = category + " at " + mrt ;

        const description_box = document.querySelector('.info_description');
        description_box.textContent = description;

        const address_box = document.querySelector('.address');
        address_box.textContent = address;

        const transport_box = document.querySelector('.transport');
        transport_box.textContent = transport;

        const pagination = document.querySelector('.overlay_dot');

        _images.forEach((imageUrl, index) => {
          const imgElement = document.createElement('img');
          
          const dot = document.createElement('span');
          dot.classList.add('dot');

          imgElement.src = imageUrl;
          imgElement.alt = `Image ${index + 1}`;
          if (index === 0) { // Set the opacity of the first image to 1
            imgElement.style.opacity = '1';
            // dot.classList.add('dot_active');
            dot.style.backgroundColor = "black";
            dot.style.border = "1px solid white";
          }
          carousel.appendChild(imgElement);
          pagination.appendChild(dot);

        });
      })
      // .catch(error => console.error('Error fetching data:', error));
      .catch(error => {
        console.error('Error fetching data:', error);
        window.location.href = "/"; // Redirect to the specified location
      });
});

let currentImage = 0;

document.querySelector('.left-button').addEventListener('click', () => {
    let images = document.querySelectorAll('.sight_box_images img');
    let dots = document.querySelectorAll('.dot');
    images[currentImage].style.opacity = '0';
    dots[currentImage].style.backgroundColor = "white";
    dots[currentImage].style.border = "white";
    
    currentImage = (currentImage - 1 + images.length) % images.length;
    images[currentImage].style.opacity = '1';
    dots[currentImage].style.backgroundColor = "black";
    dots[currentImage].style.border = "1px solid white";
});

document.querySelector('.right-button').addEventListener('click', () => {
    let images = document.querySelectorAll('.sight_box_images img');
    let dots = document.querySelectorAll('.dot');
    images[currentImage].style.opacity = '0';
    dots[currentImage].style.backgroundColor = "white";
    dots[currentImage].style.border = "white";

    currentImage = (currentImage + 1) % images.length;
    images[currentImage].style.opacity = '1';
    dots[currentImage].style.backgroundColor = "black";
    dots[currentImage].style.border = "1px solid white";
});


function updateFee(selectedTime) {
  var feeElement = document.getElementById('fee');
  var fee;

  if (selectedTime === 'morning') {
      fee = 70;
      // document.getElementById('morning').src = "/static/images/radio_solid.png";
      // document.getElementById('evening').src = "/static/images/radio_hollow.png";
  } else if (selectedTime === 'evening') {
      fee = 80;
      // document.getElementById('morning').src = "/static/images/radio_hollow.png";
      // document.getElementById('evening').src = "/static/images/radio_solid.png";
  } else {
      fee = '';
  }

  feeElement.textContent = `Fee: USD ${fee}`;
}

// Call the function initially to set the default value
updateFee();


