/** 
 * summary.js 
 * Purpose: This file contains shared code that runs on summary.html
 * Team: 133
 * Author: Abrar Iqbal
 */
"use strict";

/*
	This function redirects the user to summaryDetailed.html
	Parameters:
		-
	Returns:
		-
*/
function summary()
{
	// Directing page
	window.location = "summaryDetailed.html";
}

/*
	Global Code
*/
// Obtain index of trip chosen by user
let tripIndex = retrieveData(TRIP_INDEX_KEY);

// Display country, date, departure, arrival, number of stops, and route
document.getElementById("chosenCountry").innerHTML = user.trips[tripIndex].country;
document.getElementById("chosenDate").innerHTML = dateString(new Date(user.trips[tripIndex].date));
document.getElementById("chosenDepartureAirport").innerHTML = user.trips[tripIndex].departure;
document.getElementById("chosenArrivalAirport").innerHTML = user.trips[tripIndex].arrival;
document.getElementById("numStops").innerHTML = user.trips[tripIndex].stops;