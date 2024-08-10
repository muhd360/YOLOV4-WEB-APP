
/*password query selector.*/
const togglePassword = document.querySelector('#togglePassword');
const password = document.querySelector('#password');


/*SHOW PASSAWORD */ 
togglePassword.addEventListener('click', function() {
    const text = password.getAttribute('type') === 'password' ? 'text' : 'password';
    console.log("text", text);
    password.setAttribute('type', text);
    
    // Toggle the eye and bi-eye icon
    togglePassword.classList.toggle('bi-eye');
    togglePassword.classList.toggle('bi-eye-slash');
});


/*SUBMIT BUTTON SUCCESSFUL MESAGE*/
document.addEventListener("DOMContentLoaded", function(){

        
  
        const alert_message=document.getElementById("successMessage");
        const error_message = document.getElementById("errorMessage")
        const sign_in_form = document.querySelector('form');
        const main_html = sign_in_form.getAttribute('data-main-url');

        sign_in_form.addEventListener('submit', function(event) {
            
            event.preventDefault();
            const formData = new FormData(sign_in_form);
    
            fetch('/Web_Dev_AI/sign', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.error) {
                    error_message.textContent = data.error;
                    error_message.style.display = "block";
                  
                   setTimeout(function() {
                    error_message.style.display = 'none'; // Redirect to the main page
                }, 3000);
                debugger;

                } else{
                    alert_message.textContent = data.success;
                    alert_message.style.display = "block";
            
                    setTimeout(function() {
                        console.log('Hidding success')
                        alert_message.style.display = 'none'; // Redirect to the main page
                    }, 3000);
                    debugger;
                    setTimeout(function() {
                        window.location.href = main_html; // Redirect to the main page
                    }, 3000);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                error_message.textContent = 'An error occurred during login.';
                error_message.style.display = "block";
                setTimeout(function() {
                    console.log('Hidding success')
                    error_message.style.display = 'none'; // Redirect to the main page
                }, 3000);
            });
        });

   
});


   /*alert_submit_button.addEventListener('click', function(event){

        //event.preventDefault();
        registration_form.submit()
        alert_message.style.display = "block";

        setTimeout(function(){
            alert_message.style.display = "none";
        }, 3000);
        
    });*/