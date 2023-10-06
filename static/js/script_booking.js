document.addEventListener('DOMContentLoaded', function() {
    login_check()
    .then(token => {
        if (!token) {
            window.location.href = "/";
        } else {
            return get_trip(token);
        };
        console.log(token);

    }).then( 
        (data) => {
            const login_name = document.querySelector('.headline');
            login_name.textContent = `Hello ${info_login['name']}, here is your booking.`;

        if (data['data']) {
            const carousel = document.querySelector('.sight_box_booking_carousel');
            const imgElement = document.createElement('img');
            imgElement.src = data['data']['attraction']['image'];
            carousel.appendChild(imgElement);

            let sightname = document.getElementById('booking_sight_name');
            sightname.textContent = `Taipei Trip: ${data['data']['attraction']['name']}`;

            let date = document.getElementById('booking_date');
            date.textContent = `Date: ${data['data']['date']}`;

            let time = document.getElementById('booking_time');
            time.textContent = `Time: ${data['data']['time']}`;

            let feeElement = document.getElementById('booking_fee');
            feeElement.textContent = `Fee: USD ${data['data']['price']}`;

            let confirm_box_price = document.querySelector('.confirm_box_price');
            confirm_box_price.textContent = `Fee: USD ${data['data']['price']}`;


            let address = document.getElementById('booking_address');
            address.textContent = `Address: ${data['data']['attraction']['address']}`;
        } else {
            document.querySelector('.no_booking').style.display = 'block';
            document.querySelector('.sight_book_info').style.display = 'none';
            document.querySelector('.contact_form_outer').style.display = 'none';
            document.querySelector('.payment').style.display = 'none';
            document.querySelector('.confirm_box_outer').style.display = 'none';
            document.querySelector('.footer').style.alignItems = 'flex-start';

        }

        }
    );
});


function get_trip(token) {  
    return fetch('/api/booking', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
        },
    })
    .then(bookingResponse => bookingResponse.json())
    // .then(bookingData => {
    //     console.log('Booking Data:', bookingData);
    // })
    .catch((bookingError) => {
        console.error('Booking Fetch Error:', bookingError);
    });
  }

// function get_trip(token) {  
//     fetch('/api/booking', {
//         method: 'GET',
//         headers: {
//             'Content-Type': 'application/json',
//             'Authorization': `Bearer ${token}`,
//         },
//     })
//     .then(bookingResponse => bookingResponse.json())
//     .then(bookingData => {
//         console.log('Booking Data:', bookingData);
//     })
//     .catch((bookingError) => {
//         console.error('Booking Fetch Error:', bookingError);
//     });
//   }


document.querySelector('.booking_delete').addEventListener('click', () => {
    const token = localStorage.getItem('jwtToken');
      if (token) {
        delete_trip(token);
      };
  });


  function delete_trip(token) {  
    return fetch('/api/booking', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
        },
    })
    .then(bookingResponse => bookingResponse.json())
    .then(bookingData => {
        console.log('Booking Data:', bookingData);
        location.reload();

    })
    .catch((bookingError) => {
        console.error('Booking Fetch Error:', bookingError);
    });
  }