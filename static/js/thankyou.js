document.addEventListener('DOMContentLoaded', function() {
    login_check()
    .then(token => {
        if (!token) {
            window.location.href = "/";
        }

    }).then( 
        (data) => {
            const login_name = document.querySelector('.headline');

            let url = "http://127.0.0.1:3000/thankyou?number=202310061554440739201";
            let number = url.split("=")[1];

            login_name.textContent = `Thank you, ${info_login['name']}! Your order number: ${number}`;

        }
    );
});
