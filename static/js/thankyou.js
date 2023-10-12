
function get_thankyou_page() {
    const login_name = document.querySelector('.headline');
    let url = window.location.href;
    let number = url.split("=")[1];
    login_name.textContent = `Thank you, ${info_login['name']}! Your order number: ${number}`;
}

// document.addEventListener('DOMContentLoaded', function() {
//     login_check()
//     .then(token => {
//         if (!token) {
//             window.location.href = "/";
//         }

//     }).then( 
//         (data) => {
//             const login_name = document.querySelector('.headline');
//             let url = window.location.href
//             let number = url.split("=")[1];

//             login_name.textContent = `Thank you, ${info_login['name']}! Your order number: ${number}`;

//         }
//     );
// });
