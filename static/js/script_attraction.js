// function load_test() {
//     console.log("good load!");
// }

// Assuming you have an HTML element with class 'carousel' to append the images
const carousel = document.querySelector('.sight_box_images');

function getAttractionIdFromUrl() {
    let url = window.location.href; // Get the current URL
    let parts = url.split('/'); // Split the URL by '/'
    let id = parts[parts.length - 1]; // Get the last part of the URL
    return id;
}

let attractionId = getAttractionIdFromUrl();

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


document.querySelector('.bookingform_button_text').addEventListener('click', () => {
  force_login = true;
  // login_check();
  login_check()
  .then(token => {
    if (token) {
        book_trip(token);
    }})
  // .then(() => (window.location.href = "/booking"))
  // Q: how to put it here?
});

let data = {"attractionId": attractionId,}

function book_trip(token) {

  data['date'] = document.getElementById('targetDate').value;

  fetch('/api/booking', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(data)
  })
  .then(bookingResponse => bookingResponse.json())
  .then(bookingData => {
      // Handle the data from the second fetch here
      console.log('Booking Data:', bookingData);
      window.location.href = "/booking";
  })
  .catch((bookingError) => {
      console.error('Booking Fetch Error:', bookingError);
  });
}

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
  let feeElement = document.getElementById('fee');
  let fee;

  if (selectedTime === 'Morning') {
      fee = 70;
      // document.getElementById('morning').src = "/static/images/radio_solid.png";
      // document.getElementById('evening').src = "/static/images/radio_hollow.png";
  } else if (selectedTime === 'Afternoon') {
      fee = 80;
      // document.getElementById('morning').src = "/static/images/radio_hollow.png";
      // document.getElementById('evening').src = "/static/images/radio_solid.png";
  } else {
      fee = '';
  }

  data['time'] = selectedTime;
  data['price'] = fee;

  feeElement.textContent = `Fee: USD ${fee}`;
}

// Call the function initially to set the default value
updateFee();


