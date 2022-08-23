/** 
 * signup.js 
 * Purpose: This file contains shared code that runs on signup.html
 * Team: 133
 * Author: Germaine Pok
 */
"use strict";

/*
    This function checks if the username inputted by the user has already been taken
    Parameters:
        -
    Returns:
        -
*/
function checkUsername()
{
    // Clear Error Area
    errorUsernameRef.innerText = "";

    // Check if username has been taken
    let userCheck = userList.users.findIndex(user => user.name === usernameRef.value);
    if (userCheck !== -1)
    {
        errorUsernameRef.innerText = "This username has been taken."; 
    }
}

/*
    This function checks if the email inputted by the user is in a valid form
    Parameters:
        -
    Returns:    
        -
*/
function checkEmail()
{
    // Clear Error Area
    errorEmailRef.innerText = "";

    // Check if email is in a valid form
    if (!/^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/.test(emailRef.value))
    {
        errorEmailRef.innerText = "Please input a valid email.";
    }
}

/*
    This function checks to see if the password inputted by the user is at least 8 characters long and contains no spaces
    Parameters:
        -
    Returns:
        -
*/
function checkPassword()
{
    // Clear Error Area
    errorPasswordRef.innerText = "";

    // Check if password is valid
    if (passwordRef.value.includes(" ") || passwordRef.value.length < 8)
    {
        errorPasswordRef.innerText = "Your password should not contain spaces and should be at least 8 characters long.";
    }
}

/*
    This function verifies if the second password input is the same as the initial password input
    Parameters:
        -
    Returns:
        -
*/
function checkPasswordVerify()
{
    // Clear Error Area
    errorPasswordVerifyRef.innerText = "";

    // Check if verification matches initial password input
    if (passwordVerifyRef.value !== passwordRef.value)
    {
        errorPasswordVerifyRef.innerText = "Your verification does not match your initial password.";
    }
}

/*
    This function redirects the user back to the login.html page.
    Parameters:
        -
    Returns:
        -
*/
function backButton()
{
    window.location = "login.html";
}

/*
    This function double checks all inputs and if all are valid, add the user to the global UserList class instance and update to 
    local storage
    Parameters:
        -
    Returns:
        -
*/
function createAccount()
{
    // Input Check Variables
    let usernameValid = true;
    let emailValid = true;
    let passwordValid = true;
    let passwordVerifyValid = true;

    // Check if username has been taken
    let userCheck = userList.users.findIndex(user => user.name === usernameRef.value);
    if (userCheck !== -1)
    {
        errorUsernameRef.innerText = "This username has been taken.";
        usernameValid = false;
    }

    // Check if email is in a valid form
    if (!/^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/.test(emailRef.value))
    {
        errorEmailRef.innerText = "Please input a valid email.";
        emailValid = false;
    }

    // Check if password is valid
    if (passwordRef.value.includes(" ") || passwordRef.value.length < 8)
    {
        errorPasswordRef.innerText = "Your password should not contain spaces and should be at least 8 characters long.";
        passwordValid = false;
    }

    // Check if verification matches initial password input
    if (passwordVerifyRef.value !== passwordRef.value)
    {
        errorPasswordVerifyRef.innerText = "Your verification does not match your initial password.";
        passwordVerifyValid = false;
    }

    // Create account if all inputs valid
    if (usernameValid && emailValid && passwordValid && passwordVerifyValid)
    {
        // Clear Error Areas
        errorUsernameRef.innerText = "";
        errorEmailRef.innerText = "";
        errorPasswordRef.innerText = "";
        errorPasswordVerifyRef.innerText = "";

        // Add User
        userList.addUser(usernameRef.value,emailRef.value,passwordRef.value);
        let index = userList.users.length - 1;

        // Update Local Storage
        storeData(userList,USER_DATA_KEY);
        storeData(index,USER_INDEX_KEY);

        // Redirect User
        let lastPage = retrieveData(IMPORTANT_PAGE_KEY);
        if (lastPage === "index.html")
        {
            window.location = "index.html";
        }
        else if (lastPage === "details.html")
        {
            window.location = "details.html";
        }
        else
        {
            window.location = "index.html";
        }
    }
}

/*
    This function confirms with the user if he/she wants to skip the trip booking process
    Parameters:
    -
    Return:
    -
*/
function noLoginBooking()
{
    if (confirm("Are you sure you do not want to sign up for an account? Your trip details will not be saved!"))
    {
        localStorage.removeItem(TRIP_DATA_KEY);
        window.location = "index.html";
    }
}

/*
    Global Code
*/
// HTML Reference Variables
let usernameRef = document.getElementById("username");
let emailRef = document.getElementById("email");
let passwordRef = document.getElementById("password");
let passwordVerifyRef = document.getElementById("passwordVerify");

// HTML Error Areas
let errorUsernameRef = document.getElementById("errorUsername");
let errorEmailRef = document.getElementById("errorEmail");
let errorPasswordRef = document.getElementById("errorPassword");
let errorPasswordVerifyRef = document.getElementById("errorPasswordVerify");

// Display book without account button only if user is directed to sign up page from details page
if (retrieveData(IMPORTANT_PAGE_KEY) === "details.html")
{
    let output = `<button class="mdl-button mdl-js-button mdl-button--raised mdl-button--accent mdl-color--blue-grey" onclick="noLoginBooking()">I don't want to save my trip</button>`;
    document.getElementById("bookWithoutAcc").innerHTML = output;
}

