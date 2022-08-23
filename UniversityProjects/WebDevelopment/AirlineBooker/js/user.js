/** 
 * user.js 
 * Purpose: This file contains shared code that runs on user.html
 * Team: 133
 * Author: Cheryl Lau
 */
"use strict";

/*
    This function allows the user to change their password by prompting the user for their old password,
    checking to see if the password is correct, prompting the user for their new password, checking to see if
    it is at least 8 characters and has no spaces, prompting the user to validate the new password, and
    if valid, change the password.
    Parameters:
        -
    Returns:
        -
*/
function changePass()
{
    let valid="";
    let validity=true;
    let valid2="";
    let pass=prompt("Enter existing password:")
    //check if password entered is same as existing password
    if (pass==user.password) // if same, prompt to enter new password
    {
        valid=prompt("Enter New Password:")
        // check if new password has spacebar
        for (let i=0;i<valid.length;i++)
        {
            if (valid[i]==" ")
            {
                validity=false
            }
        }
        //check if it meets password requirements
        if (valid.length>=8 && validity)
        {
            valid2=prompt("Please re-enter password:");
            //check if re-entered password is consistent with new password
            // alert user password successfully changed if consistent
            if (valid2==valid)
            {
                user.password=valid2;
                alert("Your password has been successfully changed");
                storeData(userList,USER_DATA_KEY);
            }
            // alert password not consistent if re-entered password not the same as new password
            else
            {
                alert("Your Password is not consistent. Please try again.")
            }
        }
        else if (valid.length<8)
        {
            alert("Your Password must be more than 8 characters")
        }
        else if (validity==false)
        {
            alert("Your Password must not contain any spaces")
        }
    }
    else if (pass ==null)
    {
        // Do nothing
    }
    else
    {
        alert("Invalid Password") // if different, alert invalid password
    }
}


/*
    This function confirms with the user if they want to log out of their account. If yes, the user is logged
    out of their account and being redirected to home page.
    Parameters:
        -
    Returns:
        -
*/
function logOut()
{
    if (confirm("Are you sure you want to log out of your account?"))
    {
        user.login = false;
        window.location = "index.html";
        storeData(userList,USER_DATA_KEY);
    }
}

/*
    Global Code
*/
// Retrieve name and email of user
document.getElementById("name").innerHTML = user.name;
document.getElementById("email").innerHTML = user.email;
document.getElementById("numOfScheduled").innerHTML = user.getScheduled().length;
document.getElementById("numOfHistory").innerHTML = user.getHistory().length;