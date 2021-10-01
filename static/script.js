// TODO(daniel): This do not work for now.
// NOTE(daniel): Client-side password evaluation.
let password_input = document.getElementById("password")
let confirm_password_input = document.getElementById("confirm-password");

function validatePassword(){
    if(password.value != confirm_password.value) {
        confirm_password.setCustomValidity("Falha na confirmação de senha.");
    } else {
        confirm_password.setCustomValidity('');
    }
}

confirm_password_input.onchange = validatePassword;
confirm_password_input.onkeyup = validatePassword;
