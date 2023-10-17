// document.addEventListener('DOMContentLoaded', function() {
//     login_check()
//     .then(token => {
//         if (!token) {
//             window.location.href = "/";
//         } else {
//             return get_trip(token);
//         };
//         // console.log(token);

//     }).then( 
//         (data) => {
//             const login_name = document.querySelector('.headline');
//             login_name.textContent = `Hello ${info_login['name']}, here is your booking.`;

//         if (data['data']) {
//             const carousel = document.querySelector('.sight_box_booking_carousel');
//             const imgElement = document.createElement('img');
//             imgElement.src = data['data']['attraction']['image'];
//             carousel.appendChild(imgElement);

//             let sightname = document.getElementById('booking_sight_name');
//             sightname.textContent = `Taipei Trip: ${data['data']['attraction']['name']}`;

//             let date = document.getElementById('booking_date');
//             date.textContent = `Date: ${data['data']['date']}`;

//             let time = document.getElementById('booking_time');
//             time.textContent = `Time: ${data['data']['time']}`;

//             let feeElement = document.getElementById('booking_fee');
//             feeElement.textContent = `Fee: USD ${data['data']['price']}`;

//             let confirm_box_price = document.querySelector('.confirm_box_price');
//             confirm_box_price.textContent = `Fee: USD ${data['data']['price']}`;


//             let address = document.getElementById('booking_address');
//             address.textContent = `Address: ${data['data']['attraction']['address']}`;
//         } else {
//             document.querySelector('.no_booking').style.display = 'block';
//             document.querySelector('.sight_book_info').style.display = 'none';
//             document.querySelector('.contact_form_outer').style.display = 'none';
//             document.querySelector('.payment').style.display = 'none';
//             document.querySelector('.confirm_box_outer').style.display = 'none';
//             document.querySelector('.footer').style.alignItems = 'flex-start';

//         }

//         }
//     );
// });
const token = localStorage.getItem('jwtToken');

async function get_booking_page() {
    const data = await get_trip(token);
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
};





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

let fields = {
    number: {
        // css selector
        element: '#card-number',
        placeholder: '**** **** **** ****'
    },
    expirationDate: {
        // DOM object
        element: document.getElementById('card-expiration-date'),
        placeholder: 'MM / YY'
    },
    ccv: {
        element: '#card-ccv',
        placeholder: 'CVV or CVC'
    }
}

let styles = {
    // Style all elements
    'input': {
        'color': 'gray'
    },
    // Styling ccv field
    'input.ccv': {
        // 'font-size': '16px'
    },
    // Styling expiration-date field
    'input.expiration-date': {
        // 'font-size': '16px'
    },
    // Styling card-number field
    'input.card-number': {
        // 'font-size': '16px'
    },
    // style focus state
    ':focus': {
        // 'color': 'black'
    },
    // style valid state
    '.valid': {
        'color': 'green'
    },
    // style invalid state
    '.invalid': {
        'color': 'red'
    },
    // Media queries
    // Note that these apply to the iframe, not the root window.
    '@media screen and (max-width: 400px)': {
        'input': {
            'color': 'orange'
        }
    }
}

TPDirect.card.setup({
    fields: fields,
    styles: styles,
    // is the card number is correct, it would show the last 6 digits
    isMaskCreditCardNumber: true,
    maskCreditCardNumberRange: {
        beginIndex: 6,
        endIndex: 11
    }
})



TPDirect.card.onUpdate(function (update) {
    // update.canGetPrime === true
    // --> you can call TPDirect.card.getPrime()
    if (update.canGetPrime) {
        // Enable submit Button to get prime.
        // submitButton.removeAttribute('disabled')
    } else {
        // Disable submit Button to get prime.
        // submitButton.setAttribute('disabled', true)
    }

    // cardTypes = ['mastercard', 'visa', 'jcb', 'amex', 'unionpay','unknown']
    if (update.cardType === 'visa') {
        // Handle card type visa.
    }

    // if number field is wrong 
    if (update.status.number === 2) {
        // setNumberFormGroupToError()
    } else if (update.status.number === 0) {
        // setNumberFormGroupToSuccess()
    } else {
        // setNumberFormGroupToNormal()
    }

    if (update.status.expiry === 2) {
        // setNumberFormGroupToError()
    } else if (update.status.expiry === 0) {
        // setNumberFormGroupToSuccess()
    } else {
        // setNumberFormGroupToNormal()
    }

    if (update.status.ccv === 2) {
        // setNumberFormGroupToError()
    } else if (update.status.ccv === 0) {
        // setNumberFormGroupToSuccess()
    } else {
        // setNumberFormGroupToNormal()
    }
})


// call TPDirect.card.getPrime when user submit form to get tappay prime
// $('form').on('submit', onSubmit)

async function onSubmit(event) {
    event.preventDefault()

    // get the status of TapPay Fields
    const tappayStatus = TPDirect.card.getTappayFieldsStatus()

    // chekc if it is good to getPrime
    if (tappayStatus.canGetPrime === false) {
        alert('can not get prime')
        return
    }

    // Get prime
    const prime_result = await get_tappay_prime();
    // console.log(prime_result);

    let booking_result = await send_booking_to_backend(prime_result);
    booking_result = await booking_result.json();

    const order_number = booking_result.data.number;
    const redirectUrl = `/thankyou?number=${order_number}`;
    window.location.href = redirectUrl;
}

function get_tappay_prime() {
    return new Promise(
        function(resolve, reject) {
            TPDirect.card.getPrime((result) => {
                if (result.status !== 0) {
                    alert('get prime error ' + result.msg)
                    return
                }
                resolve(result.card.prime);
                reject("cannot get prime data");
            })
        }
    )
}

async function send_booking_to_backend(prime) {
    const token = localStorage.getItem('jwtToken')
    let data = await get_trip(token);

    let name = document.getElementById('contact_name').value;
    let email = document.getElementById('contact_email').value;
    let phone = document.getElementById('contact_mobile').value;
    // console.log("testinfoL", info_login['member_login_id']);

    data_order = {
        "prime": prime,
        "order": {
            "price": data['data']['price'],
            "trip": {
                "attraction": data['data']['attraction']
            },
            "date": data['data']['date'],
            "time": data['data']['time'],
        },
        "contact": {
            "name": name,
            "email": email,
            "phone": phone,
        },
        "member_login_id": info_login['member_login_id'],
    }
    
    return fetch('/api/orders', {
        method:'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(data_order)
    }
    )
}