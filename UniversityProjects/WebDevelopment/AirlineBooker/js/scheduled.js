/** 
 * scheduled.js 
 * Purpose: This file contains shared code that runs on scheduled.html
 * Team: 133
 * Author: Cheryl Lau
 */
"use strict";

/* 
    This function displays any existing scheduled trips for a user by generating the appropriate HTML from the data to form cards.
    Parameters:
        -
    Returns:
        -
*/
function displayScheduled()
{
    let output = "";

    // Check if there are no scheduled trips
    if (scheduled.length === 0)
    {
        output = "<br><br><br><br><br><br><br><br><br><br><br><br><br><h5 class='center'>You currently have no trips that are scheduled</h5>";
    }
    else
    {
        // Generating scheduled card by going through the scheduled list in user class
        for (let i = 0; i < scheduled.length; i++)
        {
            output += `<div class="history-card-wide mdl-card mdl-shadow--2dp center">
                        <div class="mdl-card__title">
                            <h3>${scheduled[i].country}</h3>
                            <div class="mdl-layout-spacer"></div>
                            <h4>${dateString(new Date(scheduled[i].date))}</h4>
                        </div>
                            <div class="mdl-card__actions mdl-card--border">
                                <a class="mdl-button mdl-button--colored mdl-js-button mdl-js-ripple-effect" onclick="view(${i})">
                                Details
                                </a>
                            </div>
                            <div class="mdl-card__menu">
                                <button class="mdl-button mdl-button--icon mdl-js-button mdl-js-ripple-effect" style="color:#ff0000" onclick="deleteButton(${i})">
                                <i class="material-icons">delete_forever</i>
                                </button>
                            </div>
                        </div><br>`
        }
    }

    // Output to User
    let scheduleCardRef = document.getElementById("scheduleCard");
    scheduleCardRef.innerHTML = output;
}

/*
    This function deletes a scheduled trip based on the selected index from the visible list and in local storage of USER_DATA_KEY
    Parameters:
        index: The trip index in the scheduled array
    Returns:
        -
*/
function deleteButton(index)
{
    // Get Index for User Trip Array
    let tripIndex = user.getTripIndex(scheduled[index]);
    if (confirm("Your scheduled trip will be deleted permanently by clicking OK. Are you sure you want to cancel your trip?"))
    {
        // Remove trip from scheduled in user class
        user.removeTrip(tripIndex);
        storeData(userList,USER_DATA_KEY);
        location.reload();
    }
}

/*
    This function redirects the user to summary.html and displays the appropriate trip details based on the selected trip index
    Parameters:
        index: The trip index in the scheduled array
    Returns:
        -
*/
function view(index)
{
    // Get Index for User Trip Array
    let tripIndex = user.getTripIndex(scheduled[index]);
    storeData(tripIndex,TRIP_INDEX_KEY);
    window.location = "summary.html";
}

/*
    Global Code
*/
let scheduled = user.getScheduled();
displayScheduled();