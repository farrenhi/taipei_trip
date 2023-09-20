// // modify getElementByID!

// document.getElementById('modal_form').addEventListener('submit', function(event) {
//     event.preventDefault();

//     let name = document.getElementById('name').value;
//     let email = document.getElementById('email').value;
//     let password = document.getElementById('password').value;

//     let data = {
//         "name": name,
//         "email": email,
//         "password": password,
//     };

//     fetch('/signup', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify(data)
//     })
//     .then(response => response.json())
//     .then(data => {
//         console.log('Success:', data); // check what is the print out here
//         console.log('Signup is good! Need to add info into webpage'); // check what is the print out here
//     })
//     .catch((error) => {
//         console.error('Error:', error);
//     });
// });



// above is script

// retrieve
// let token = localStorage.getItem('jwtToken');



