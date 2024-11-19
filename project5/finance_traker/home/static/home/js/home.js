document.addEventListener('DOMContentLoaded', () => {
    console.log('Registration page')
    const registrationBtn = document.querySelector('.register-btn');

    if (registrationBtn) {
        registrationBtn.addEventListener('click', registerBtn);
    }
});
 

function registerBtn() {
    console.log('clicked reg btn');
}