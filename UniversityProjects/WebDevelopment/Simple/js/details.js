/** 
 * details.js
 * Purpose: This file contains code that will run on details.html
 * Team: 133
 * Author: Abrar Iqbal
 */
"use strict";

/*
	This function activates when the Continue Editting Button is clicked and redirects the user to index.html
	Parameters:
		-
	Returns:
		-
*/
function detailsHome()
{
	// Directing page
	window.location = "index.html";
}

/*
	This function activates when the Confirm Trip Button is clicked and checks if there are users within the global UserList class.
	If there are no users, redirect to login.html. Else, check if the relevant user is logged in. If the user is logged in, redirect to 
	booking.html. Else, redirect to login.html.
	Parameters:
		-
	Returns:
		-
*/
function detailsBooking()
{
	// Check if User is Logged in
	if (checkIfDataExistsLocalStorage(USER_DATA_KEY))
	{
		if (userList.length === 0)
		{
			window.location = "login.html";
		}
		else
		{
			if (user.login)
			{
				user.addTrip(trip);
				storeData(user.trips.length - 1,TRIP_INDEX_KEY);
				storeData(userList,USER_DATA_KEY);
				localStorage.removeItem(TRIP_DATA_KEY);
				window.location = "booking.html";
			}
			else
			{
				window.location = "login.html";
			}
		}
	}
	else
	{
		window.location = "login.html";
	}
}

/*
	Global Code
*/
// Bookmark page in local storage
storeData("details.html",IMPORTANT_PAGE_KEY);

// HTML Reference Variables
let chosenCountryRef = document.getElementById("chosenCountry");
let chosenDateRef = document.getElementById("chosenDate");
let chosenDepartureAirportRef = document.getElementById("chosenDepartureAirport");
let chosenArrivalAirportRef = document.getElementById("chosenArrivalAirport");
let numStopsRef = document.getElementById("numStops");

// Obtain Trip Data from Local Storage
if (checkIfDataExistsLocalStorage(TRIP_DATA_KEY))
{
	let restore = retrieveData(TRIP_DATA_KEY);
	trip.fromData(restore);

	// Display Relevant Details
	chosenCountryRef.innerText = trip.country;
	chosenDateRef.innerText = dateString(new Date(trip.date));
	chosenDepartureAirportRef.innerText = trip.departure;
	chosenArrivalAirportRef.innerText = trip.arrival;
	numStopsRef.innerText = trip.stops;
}
else
{
	chosenCountryRef.innerText = "NOT AVAILABLE";
	chosenDateRef.innerText = "NOT AVAILABLE";
	chosenDepartureAirportRef.innerText = "NOT AVAILABLE";
	chosenArrivalAirportRef.innerText = "NOT AVAILABLE";
	numStopsRef.innerText = "NOT AVAILABLE";
}