//validate student login data
validateLogin = function(data) {
    var errors = [];
    if (!data[0].value) {
        errors.push("Student Id can not be empty");
    }
    if (!data[1].value) {
        errors.push("This field can not be empty");
    }
    return errors;
};
//

const error = document.getElementsByClassName("error")[0]; //use as global var
const userInput = document.getElementsByClassName('login_input');
const errorOutput = document.getElementsByClassName('input_inline_error');
for (let i = 0; i < userInput.length; i++) {

    userInput[i].addEventListener('blur', () => {
        if (!userInput[i].value) {

            //check which input the user interact with
            if (userInput[i].type == 'text') {
                errorOutput[i].innerHTML = `<li class="fa fa-warning"></li> Student Id can not be empty`;
            } else {
                errorOutput[i].innerHTML = `<li class="fa fa-warning"></li> Provide your valid password`;
            }
        } else {
            // if input is not empty, hide warning messagee
            errorOutput[i].innerHTML = '';
        }
    })

}
// Submit login form
$(function() {
    $('#loginBtn').on('click', (event) => {
        event.preventDefault()
        const validate = validateLogin(userInput);
        error.innerHTML = '';
        if (validate.length == 0) {
            // if validation passed
            $('#loginBtn').html('Please wait...');
            $.ajax({
                url: 'login',
                method: 'POST',
                data: 'username=' + userInput[0].value.toUpperCase() + '&password=' + userInput[1].value,
                setTimeout: 3000
            }).done(function(data) {
                console.log(data)
                if (data.status == 200) {
                    // if login success
                    window.location.href = '/dashboard';
                } else {
                    // if login failed
                    $('#loginBtn').html('Login to Account');
                }
            }).fail(function(data) {
                $('#loginBtn').html('Login to Account');
            });

        } else {
            // if validation failed
            error.innerHTML = `<div class="error_msg" id="error_msg">
                            There are some errors in your form
                            <li class="fa fa-close err-close" data-id="error_msg" onclick="clostbtn('error_msg')"></li>
                        </div>`;
        }

    })
});


//activate form
const activateInput = document.getElementsByClassName('activate_input');
$(function() {
    $('#activateBtn').on('click', (event) => {
        event.preventDefault()
        const validate = validateLogin(activateInput);
        if (validate.length == 0 || activateInput[1].value > 11) {
            // if validation passed
            $('#activateBtn').html('Please wait...');
            $.ajax({
                url: 'activate',
                method: 'POST',
                data: 'username=' + activateInput[0].value.toUpperCase() + '&telephone=' + activateInput[1].value,
                setTimeout: 3000
            }).done(function(data) {
                console.log(data)
                $('#activateBtn').html('Activate Account');
                if (data.status == 200) {
                    // if login success
                    window.location.href = '/activate/verify';
                } else {
                    // if login failed
                    error.innerHTML = `<div class="error_msg" id="error_msg">
            <span>${data.message}</span>
            <li class="fa fa-close err-close-btn" data-id="error_msg" onclick="clostbtn('error_msg')"></li>
            </div>`;

                }
            }).fail(function(data) {
                $('#activateBtn').html('Activate Account');
                error.innerHTML = `<div class="error_msg" id="error_msg">
            <span>Request failed unexpectedly, try again</span>
            <li class="fa fa-close err-close-btn" data-id="error_msg" onclick="clostbtn('error_msg')"></li>
            </div>`;
            });

        } else {
            // if validation failed
            error.innerHTML = `<div class="error_msg" id="error_msg">
            <span>There are some errors in your form</span>
            <li class="fa fa-close err-close-btn" data-id="error_msg" onclick="clostbtn('error_msg')"></li>
            </div>`;
        }

    })
});


//close error message
const clostbtn = (id) => {
    const closeBtnParent = document.getElementById(id);
    closeBtnParent.style.display = 'none';

}

//actiavte code
$(function() {
    $('#verifybtn').on('click', (event) => {
        event.preventDefault();
        const activateCode = document.getElementsByClassName('activate_code')[0].value;
        error.innerHTML = '';
        if (activateCode == '') {
            error.innerHTML = `<div class="error_msg" id="error_msg">
            <span>Activation code can not be empty</span>
            <li class="fa fa-close err-close-btn" data-id="error_msg" onclick="clostbtn('error_msg')"></li>
            </div>`;

        } else {
            $('#verifybtn').html('Please wait...');
            $.ajax({
                url: 'verify',
                method: 'POST',
                data: 'code=' + activateCode,
                setTimeout: 3000
            }).done(function(data) {
                console.log(data)
                $('#verifybtn').html('Verify');
                if (data.status == 200) {
                    // if login success
                    window.location.href = '/activate/update';
                } else {
                    // if login failed
                    error.innerHTML = `<div class="error_msg" id="error_msg">
                <span>${data.message}</span>
            <li class="fa fa-close err-close-btn" data-id="error_msg" onclick="clostbtn('error_msg')"></li>
            </div>`;

                }
            }).fail(function(data) {
                $('#verifybtn').html('Verify');
                error.innerHTML = `<div class="error_msg" id="error_msg">
            <span>!Request failed unexpectedly, try again</span>
            <li class="fa fa-close err-close-btn" data-id="error_msg" onclick="clostbtn('error_msg')"></li>
            </div>`;
            });


        }

    })
})