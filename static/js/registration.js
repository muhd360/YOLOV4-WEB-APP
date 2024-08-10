
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



/*password query selectoro per validazione*/
const togglePasswordConfirm = document.querySelector('#togglePasswordConfirm');
const passwordConfirm = document.querySelector('#password_confirm');

// Show password for the confirm password field
togglePasswordConfirm.addEventListener('click', function() {
    const type = passwordConfirm.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordConfirm.setAttribute('type', type);

    // Toggle the eye icon
    togglePasswordConfirm.classList.toggle('bi-eye');
    togglePasswordConfirm.classList.toggle('bi-eye-slash');
});


/*SUBMIT BUTTON SUCCESSFUL MESAGE*/
document.addEventListener("DOMContentLoaded", function(){

        
    const alert_message=document.getElementById("signUpSuccess");
    const form_data = document.querySelector('form')
    const error_message = document.getElementById("signUpError");
    
    const signInUrl = form_data.getAttribute('data-sign-in-url')
    
    form_data.addEventListener('submit', function(event){


        event.preventDefault(); // // Prevent the default form submission

        const formData = new FormData(form_data);

        fetch('/Web_Dev_AI/registration', {

            method:'POST',
            body:formData
        })
        .then(response=>response.json())

        .then(data=>{

            if(data.Error){

                error_message.textContent = data.Error // display server error
                error_message.style.display = "block";
                setTimeout(function(){
                   
                    error_message.style.display='none';
                }, 3000);
              

            }else{
                // handle message registration
                alert_message.textContent = data.Success
                alert_message.style.display = "block"; 

                setTimeout(function(){
                    console.log('Hidding success')
                    alert_message.style.display='none';
                }, 3000);
             

                setTimeout(function() {
                    window.location.href = signInUrl; // Redirect to the sign-in page
                }, 3000);
            }

            
        })

        .catch(error=>{
            console.error('Error', error)
        })

    })
    
 
   
});
