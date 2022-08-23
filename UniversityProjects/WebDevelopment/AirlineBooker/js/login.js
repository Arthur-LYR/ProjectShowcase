/** 
 * login.js 
 * Purpose: This file contains shared code that runs on login.html
 * Team: 133
 * Author: Germaine Pok
 */
"use strict";

/*
    This function retrieves the inputs by the user and checks to see if they are valid
    Parameters:
        -
    Returns:
        -
*/
function login()
{
    // HTML Reference Variables
    let username = document.getElementById("username").value;
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;
    let error = document.getElementById("errorLogin");

    // Check if username, email, and password are valid
    let user = userList.users.find(user => user.name === username);
    let index = userList.users.findIndex(user => user.name === username);
    if (typeof(user) === "undefined" || email !== user.email || password !== user.password)
    {
        error.innerText = "Your username, email, or password is invalid";
    }
    else if (typeof(user) !== "undefined" && email === user.email && password === user.password)
    {
        error.innerText = "";
        userList.users[index].login = true;
        storeData(userList,USER_DATA_KEY);
        storeData(index,USER_INDEX_KEY);

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
    This function redirects the user to the signup.html page
    Parameters:
        -
    Returns:
        -
*/
function signup()
{
	// Directing page
	window.location = "signup.html";
}