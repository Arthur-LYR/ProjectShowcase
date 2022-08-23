/** 
 * history.js 
 * Purpose: This file contains shared code that runs on history.html
 * Team: 133
 * Author: Abrar Iqbal
 */
"use strict";

/* 
    This function displays any historical trips for a user by generating the appropriate HTML from the data to form cards.
    Parameters:
        -
    Returns:
        -
*/
function displayHistory()
{
    let output = "";

    // Check if there are no historical trips
    if (history.length === 0)
    {
        output = "<br><br><br><br><br><br><br><br><br><br><br><br><br><h5 class='center'>You currently have no trips in your history</h5>";
    }
    else
    {
        // Generating history card by going through the history list in user class
        for (let i = 0; i < history.length; i++)
        {
            output += `<div class="history-card-wide mdl-card mdl-shadow--2dp center">
                        <div class="mdl-card__title">
                            <h3>${history[i].country}</h3>
                            <div class="mdl-layout-spacer"></div>
                            <h4>${dateString(new Date(history[i].date))}</h4>
                        </div>
                            <div class="mdl-card__actions mdl-card--border">
                                <a class="mdl-button mdl-button--colored mdl-js-button mdl-js-ripple-effect" onclick="view(${i})">
                                Details
                                </a>
                            </div>
                        </div><br>`
        }
    }

    // Output to User
	let historyCardRef = document.getElementById("historyCard");
	historyCardRef.innerHTML = output;
}

/*
    This function redirects the user to summary.html and displays the appropriate trip details based on the selected trip index
    Parameters:
        index: The trip index in the history array
    Returns:
        -
*/
function view(index)
{
    // Get Index for User Trip Array
    let tripIndex = user.getTripIndex(history[index]);
    storeData(tripIndex,TRIP_INDEX_KEY);
    window.location = "summary.html";
}

/*
    Global Code
*/
let history = user.getHistory();
displayHistory();

