function validateUsername(usernameElement) {
    const username = usernameElement.value;
    const alphanumericPattern = /^[a-z0-9]{5,40}$/i;
    if (!alphanumericPattern.test(username)) {
        alert("Username must be alphanumeric and 5-40 characters long.");
        return false;
    }
    return true;
}

function validateEmail(emailElement) {
    const email = emailElement.value;
    const emailPattern = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;
    if (!emailPattern.test(email)) {
        alert("Please enter a valid email address.");
        return false;
    }
    return true;
}

function validatePassword(passwordElement) {
    const password = passwordElement.value;
    if (password.length < 8 || password.length > 40) {
        alert("Password must be between 8 and 40 characters long.");
        return false;
    }
    return true;
}

function validateAddress(addressElement) {
    const address = addressElement.value;
    if (address.length < 6 || address.length > 254) {
        alert("Address must be between 6 and 254 characters long.");
        return false;
    }
    return true;
}

function validateForm() {
    const usernameInput = document.getElementById('username');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const addressInput = document.getElementById('address');

    // Validate each field and focus if invalid
    if (!validateUsername(usernameInput)) {
        usernameInput.focus();
        return false;
    }
    if (!validateEmail(emailInput)) {
        emailInput.focus();
        return false;
    }
    if (!validatePassword(passwordInput)) {
        passwordInput.focus();
        return false;
    }
    if (!validateAddress(addressInput)) {
        addressInput.focus();
        return false;
    }
    return true; // All validations passed
}

function setupValidation() {
    const signupForm = document.getElementById('signupForm');
    signupForm.addEventListener('submit', function(event) {
        if (!validateForm()) {
            event.preventDefault(); // Prevent form submission if validation fails
        }
    });
}

window.onload = setupValidation;
