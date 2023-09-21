function login_check() {
    const token = localStorage.getItem('jwtToken');
    // console.log(token);

    if (token) {
    fetch('/api/user/auth', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
        }
    })
    .then(response => response.json())
    .then(data => {
        // console.log('Fetch Success Yes:', data);
        if (data["data"]) {
            document.getElementById('loginButton').style.display = 'none';
            document.getElementById('logout_button').style.display = 'block';

        } else if (data["error"]) {
            open_login();
        }
        
    })
    .catch((error) => {
        console.error('Fetch Error Error:', error);
    });
    }
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById("taipei_trip").addEventListener("click", function() {
        window.location.href = "/";
    });
});



function open_login() {
    document.getElementById('myModal').style.display = 'flex';
    document.getElementById('mask').style.display = 'block';
    document.getElementById('signup').style.display = 'none';
}

function open_signup() {
    document.getElementById('myModal').style.display = 'none';
    document.getElementById('mask').style.display = 'block';
    document.getElementById('signup').style.display = 'flex';
}


function close_both_dialogs() {
    document.getElementById('myModal').style.display = 'none';
    document.getElementById('mask').style.display = 'none';
    document.getElementById('signup').style.display = 'none';
}

document.getElementById('loginButton').addEventListener('click', open_login);
document.getElementById('link_login').addEventListener('click', open_login);
document.getElementById('link_signup').addEventListener('click', open_signup);

document.getElementById('close_signup').addEventListener('click', close_both_dialogs);
document.getElementById('close_login').addEventListener('click', close_both_dialogs);

document.getElementById('logout_button').addEventListener('click', function(event) {
    event.preventDefault();
    localStorage.removeItem('jwtToken');
    document.getElementById('loginButton').style.display = 'block';
    document.getElementById('logout_button').style.display = 'none';
    location.reload();
})

// document.getElementById('loginButton').addEventListener('click', function() {
//     document.getElementById('myModal').style.display = 'flex';
//     document.getElementById('mask').style.display = 'block';
//     // document.querySelector('.nav_box').style.backgroundColor = 'black';
//     // document.querySelector('.nav_box').style.opacity = 0.25;

//     });

    // document.querySelector('.close').addEventListener('click', function() {
    // document.getElementById('myModal').style.display = 'none';
    // document.getElementById('mask').style.display = 'none';
    // });

// Login process
document.getElementById('modal_form').addEventListener('submit', function(event) {
    event.preventDefault();

    let email = document.getElementById('email').value;
    let password = document.getElementById('password').value;

    let data = {
        "email": email,
        "password": password,
    };

    // console.log("check point on javascript 1");

    fetch('/api/user/auth', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Fetch Success Yes:', data); 
        if (data['token']) {
            localStorage.setItem('jwtToken', data['token']);
            // redirect the user to other place
            location.reload();
        } else {
            console.log(data['message']);
            const modalErrorBox = document.querySelector('.modal_error_box');
            modalErrorBox.style.display = 'block';
            modalErrorBox.textContent = data['message'];
        }
        
    })
    .catch((error) => {
        console.error('Fetch Error Error:', error);
    });
});


// Process Sign Up
document.getElementById('signup_form').addEventListener('submit', function(event) {
    event.preventDefault();

    let name = document.getElementById('name').value;
    let email = document.getElementById('signup_email').value;
    let password = document.getElementById('signup_password').value;

    let data = {
        "name": name,
        "email": email,
        "password": password,
    };

    // console.log("check point on javascript 1");

    fetch('/api/user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Signup Success Yes:', data); 
        const signup_status = document.getElementById('signup_status');
        signup_status.style.display = 'block';

        if (data['ok']) {
            // console.log(data['message']);
            signup_status.textContent = "You are now our member!";
        } else if (data.error) {
            signup_status.textContent = data.message;
        }
        
    })
    .catch((error) => {
        console.error('Fetch Error Error:', error);
    });
});



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