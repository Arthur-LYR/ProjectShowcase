/** 
 * index.js 
 * Purpose: This file contains shared code that runs on index.html
 * Team: 133
 * Author: Arthur Lee
 */
"use strict";

/*
    This function enables an MDL Text Input Field
    Parameters:
        id: The id of the text input element
    Returns:
        -
*/
function enableTextfield(id)
{
    let textfieldRef = document.getElementById(id);
    textfieldRef.setAttribute("class","mdl-textfield mdl-js-textfield mdl-textfield--floating-label has-placeholder");
}

/*
    This function disables an MDL Text Input Field
    Parameters:
        id: The id of the text input element
    Returns:
        -
*/
function disableTextfield(id)
{
    let textfieldRef = document.getElementById(id);
    textfieldRef.setAttribute("class","mdl-textfield mdl-js-textfield mdl-textfield--floating-label has-placeholder is-disabled");
}

/*
    This function validates the country inputted by the user and if valid, saves it and generates appropriate airport list
    Parameters:
        -
    Returns:
        -
*/
function getCountry()
{
    // Clear Appropriate Inputs
    departureAirportRef.value = "";
    arrivalAirportRef.value = "";

    // Check if country is valid
    if (checkCountryValid(countryRef.value))
    {
        // Enable Departure Airport Input
        departureAirportRef.removeAttribute("disabled");
        enableTextfield("departureAirportTextfield");

        // Keep Arrival Airports Disabled
        arrivalAirportRef.setAttribute("disabled","");
        disableTextfield("arrivalAirportTextfield")

        // Save User Input
        countryInput = countryRef.value;

        // Make Web Service Request for Airports
        let url = "https://eng1003.monash/OpenFlights/airports/";
        let data = {
            country: countryInput,
            callback: "generateDepartureAirports"
        };
        webServiceRequest(url,data);
    }
    else
    {
        // Display Error
        alert("Please input a valid country!");

        // Disable Future Inputs
        departureAirportRef.setAttribute("disabled","");
        disableTextfield("departureAirportTextfield");
        arrivalAirportRef.setAttribute("disabled","");
        disableTextfield("arrivalAirportTextfield");
    }
}

/*
    This function validates the date inputted by user and saves it if valid
    Parameters:
        -
    Returns:
        -
*/
function getDate()
{
    // Define Dates
    let today = new Date();
    today.setHours(0);
    today.setMinutes(0);
    today.setSeconds(0);
    today.setMilliseconds(0);
    let date = new Date(dateRef.value);

    // Check if Date Valid
    if (date >= today)
    {
        dateInput = date;
    }
    else
    {
        alert("Please input a valid date!");
    }
}

/*
    This function validates the departure airport inputted by user and saves it if valid
    Parameters:
        -
    Returns:
        -
*/
function getDepartureAirport()
{
    // Clear Appropriate Inputs
    arrivalAirportRef.value = "";
    map = "";

    // Check if Departure Airport Valid
    if (departureAirportList.includes(departureAirportRef.value))
    {
        // Enable Arrival Airports
        arrivalAirportRef.removeAttribute("disabled");
        enableTextfield("arrivalAirportTextfield");

        // Save User Input
        departureAirportInput = departureAirportRef.value;

        // Find Departure Airport Info
        departureAirportId = findAirportId(departureAirportInput);
        departureAirportCoords = findAirportCoords(departureAirportInput);
        departureAirportCity = findAirportCity(departureAirportInput);

        // Make Web Service Request for Routes
        let url = "https://eng1003.monash/OpenFlights/routes/";
        let data = {
            sourceAirport: departureAirportId,
            callback: "findArrivalAirports"
        };
        webServiceRequest(url,data);
    }
    else
    {
        alert("Please input a valid airport!");
        arrivalAirportRef.setAttribute("disabled","");
        disableTextfield("arrivalAirportTextfield");
    }
}

/*
    This function validates the arrival airport inputted by user and saves it if valid
    Parameters:
        -
    Returns:
        -
*/
function getArrivalAirport()
{
    // Check if Arrival Airport is Valid
    if (arrivalAirportList.includes(arrivalAirportRef.value))
    {
        // Save User Input
        arrivalAirportInput = arrivalAirportRef.value;
    }
    else
    {
        alert("Please input a valid airport!");
    }
}

/*
    This function finds the appropriate airport id from the airport name
    Parameters:
        airportName: Name of Airport
    Returns:
        The corresponding airport Id
*/
function findAirportId(airportName)
{
    // Loop through Airports
    for (let i = 0; i < airports.length; i++)
    {
        if (airportName === airports[i].name)
        {
            return airports[i].airportId;
        }
    }
}

/*
    This function finds the appropriate airport coordinates from the airport name
    Parameters:
        airportName: Name of Airport
    Returns:
        Corresponding longitude and latitude in array form
*/
function findAirportCoords(airportName)
{
    // Loop through Airports
    for (let i = 0; i < airports.length; i++)
    {
        if (airportName === airports[i].name)
        {
            return [airports[i].longitude,airports[i].latitude];
        }
    }
}

/*
    This function finds the appropriate airport city from the airport name
    Parameters:
        airportName: Name of Airport
    Returns:
        Corresponding airport city
*/
function findAirportCity(airportName)
{
    // Loop through Airports
    for (let i = 0; i < airports.length; i++)
    {
        if (airportName === airports[i].name)
        {
            return airports[i].city;
        }
    }
}

/*
    This function generates the appropriate HTML to display a dropdown list of departure airports in a country
    Parameters:
        airportData: Data returned from Airports API
    Returns:
        -
*/
function generateDepartureAirports(airportData)
{
    airports = airportData;

    // Clear Datalist
    departureAirportList = [];

    // Loop through airport data and collect names
    for (let i = 0; i < airportData.length; i++)
    {
        departureAirportList.push(airportData[i].name);
    }

    // Check if Departure Airport List is Empty
    if (departureAirportList === 0)
    {
        alert("This country has no airport information. Try another country.");
    }
    else
    {
        // Display Dropdown List
        departureAirportsRef.innerHTML = createDatalist(departureAirportList.sort());
    }
}

/*
    This function displays a map of all routes from an airport for the user and generates the appropriate HTML for the arrival airports
    Parameters:
        routeDate: Data returned from Routes API
    Returns:
        -
*/
function findArrivalAirports(routeData)
{
    // Clear Datalist and Map Inner HTML
    arrivalAirportList = [];
    mapRef.innerHTML = "";
    
    // Display Map
    mapboxgl.accessToken = MAPBOX_TOKEN;
    map = new mapboxgl.Map({
        container: "map",
        style: "mapbox://styles/mapbox/streets-v9", // stylesheet location
        center: departureAirportCoords, // starting position [lng, lat]
        zoom: 4, // starting zoom
    });

    // Create a marker with the set to appropriate coordinates
    let marker = new mapboxgl.Marker({ "color": "#FF0000" });
    marker.setLngLat(departureAirportCoords);

    // Create the respective popup
    let popup = new mapboxgl.Popup({ offset: 45});
    popup.setHTML("Departure: " + departureAirportInput + "<br>Location: " + departureAirportCity + ", " + countryInput);
    marker.setPopup(popup);

    // Display the marker
    marker.addTo(map);

    // Display the popup
    popup.addTo(map);  

    // Loop through route data
    for (let i = 0; i < routeData.length; i++)
    {
        let color = "#" + randomHex();
        let arrivalAirportId = routeData[i].destinationAirportId;

        for (let i = 0; i < airports.length; i++)
        {
            if (arrivalAirportId == airports[i].airportId)
            {
                let arrivalAirportCoords = [airports[i].longitude,airports[i].latitude];
                arrivalAirportList.push(airports[i].name);

                // Create a marker with the set to appropriate coordinates
                let marker = new mapboxgl.Marker({ "color": "#4240E3" });
                marker.setLngLat(arrivalAirportCoords);

                // Create the respective popup
                let popup = new mapboxgl.Popup({ offset: 45});
                popup.setHTML("Arrival: " + airports[i].name + "<br>Location: " + airports[i].city + ", " + airports[i].country);
                marker.setPopup(popup);

                // Display the marker
                marker.addTo(map);

                // Display the popup
                popup.addTo(map);  

                // Create Source for Lines
                let object = {
                    type: "geojson",
                    data: {
                        type: "Feature",
                        properties: {},
                        geometry: {
                            type: "LineString",
                            coordinates: [departureAirportCoords,arrivalAirportCoords]
                        }
                    }
                };

                // Display Lines on Map
                map.on("load", function() {
                    map.addLayer({
                        id: String(Math.random()),
                        type: "line",
                        source: object,
                        layout: { "line-join": "round", "line-cap": "round" },
                        paint: { "line-color": color, "line-width": 6 }
                    });
                });
            }
        }
    }

    // Remove Duplicate Airports
    arrivalAirportList = [...new Set(arrivalAirportList)];

    // Check if Arrival Airport List is Empty
    if (arrivalAirportList.length === 0)
    {
        arrivalAirportRef.setAttribute("disabled","");
        disableTextfield("arrivalAirportTextfield");
        alert("This airport has no domestic flights. Please try another airport.");
    }
    else
    {
        arrivalAirportsRef.innerHTML = createDatalist(arrivalAirportList.sort());
    }
}

/*
    This function generates the country airport data for connecting flight refreshes
    Parameters:
        -
    Returns:
        -
*/
function getAirportData(airportData)
{
    airports = airportData;

    // Update Departure Airport Info
    departureAirportId = findAirportId(departureAirportInput);
    departureAirportCoords = findAirportCoords(departureAirportInput);
    departureAirportCity = findAirportCity(departureAirportInput);
    generateDepartureAirports(airportData);

    // Make Web Service Request for Routes
    let url = "https://eng1003.monash/OpenFlights/routes/";
    let data = {
        sourceAirport: departureAirportId,
        callback: "findArrivalAirports"
    };
    webServiceRequest(url,data);
}

/*
    This function cancels the user's trip entirely
    Parameters:
        -
    Returns:
        -
*/
function cancelTrip()
{
    if (trip.count === 0)
    {
        alert("You have no trip to delete!");
    }
    else
    {
        if (confirm("Are you sure you want to cancel your trip?"))
        {
            localStorage.removeItem(TRIP_DATA_KEY);
            location.reload();
        }
    }
}

/*
    This function removes the previous flight route in a user's trip
    Parameters:
        -
    Returns:
        -
*/
function removePrevious()
{
    if (trip.count > 1)
    {
        trip.removePrevious();
        storeData(trip,TRIP_DATA_KEY);
        location.reload();
        departureAirportRef.value = trip.flights[trip.count - 1].startAirport;
    }
    else if (trip.count === 1)
    {
        if (confirm("Are you sure you want to cancel your trip?"))
        {
            localStorage.removeItem(TRIP_DATA_KEY);
            location.reload();
        }
    }
    else
    {
        alert("You have no previous routes in your trip to remove!");
    }
}

/*
    This function confirms if the user wants to finish booking their trip and if yes, saves the information and displays the details page
    Parameters:
        -
    Returns:
        -
*/
function finish()
{
    let date = new Date(dateRef.value);
    let today = new Date();
    today.setHours(0);
    today.setMinutes(0);
    today.setSeconds(0);
    today.setMilliseconds(0);

    // Check if Inputs Valid
    if (checkCountryValid(countryRef.value) && date >= today && departureAirportList.includes(departureAirportRef.value) && arrivalAirportList.includes(arrivalAirportRef.value))
    {
        if (confirm("Are you sure you want to finish booking?"))
        {
            trip.addFlight(countryInput,dateInput,departureAirportInput,arrivalAirportInput);
            storeData(trip,TRIP_DATA_KEY);
            window.location = "details.html";
        }
    }
    else
    {
        alert("Please fill in the necessary fields appropriately!");
    }
}

/*
    This function refreshes the page and allows the user to book the next flight route for their trip
    Parameters:
        -
    Returns:
        -
*/
function nextRoute()
{
    let date = new Date(dateRef.value);
    let today = new Date();
    today.setHours(0);
    today.setMinutes(0);
    today.setSeconds(0);
    today.setMilliseconds(0);

    // Check if Inputs Valid
    if (checkCountryValid(countryRef.value) && date >= today && departureAirportList.includes(departureAirportRef.value) && arrivalAirportList.includes(arrivalAirportRef.value))
    {
        trip.addFlight(countryInput,dateInput,departureAirportInput,arrivalAirportInput);
        storeData(trip,TRIP_DATA_KEY);
        location.reload();
    }
    else
    {
        alert("Please fill in the necessary fields appropriately!");
    }
}

/*
    Global Code
*/
// Bookmark page in local storage
storeData("index.html",IMPORTANT_PAGE_KEY);

// Initialise Map
let map;

// User Input Variables
let countryInput = "";
let dateInput = "";
let departureAirportInput = "";
let arrivalAirportInput = "";

// Departure Airport Info
let departureAirportId = "";
let departureAirportCoords = [];
let departureAirportCity = "";

// Airport Data Variable
let airports = [];

// HTML Reference Variables
let numRoutesRef = document.getElementById("numRoutes");
let countryRef = document.getElementById("country");
let dateRef = document.getElementById("date");
let departureAirportRef = document.getElementById("departureAirport");
let arrivalAirportRef = document.getElementById("arrivalAirport");
let mapRef = document.getElementById("map");

// HTML Datalist Variables
let countriesRef = document.getElementById("countries");
let departureAirportsRef = document.getElementById("departureAirports");
let arrivalAirportsRef = document.getElementById("arrivalAirports");

// Create Country Datalist
countriesRef.innerHTML = createDatalist(countryData);

// Departure / Arrival Airport Array
let departureAirportList = [];
let arrivalAirportList = [];

// Limit Date input to future dates
let minDate = dateHTML(new Date());
dateRef.setAttribute("min",minDate);

// Check if existing trip data exists and retrieve if it does
if (checkIfDataExistsLocalStorage(TRIP_DATA_KEY))
{
    let restore = retrieveData(TRIP_DATA_KEY);
    trip.fromData(restore);

    // Update Input Fields
    numRoutesRef.innerText = trip.count;
    countryRef.value = trip.country;
    dateRef.value = dateHTML(new Date(trip.date));
    departureAirportRef.value = trip.arrival;
    arrivalAirportRef.value = "";

    // Update User Input
    countryInput = countryRef.value;
    dateInput = new Date(dateRef.value);
    departureAirportInput = departureAirportRef.value;
    arrivalAirportInput = "";
}

// Display page appropriately if more than zero routes
if (Number(numRoutesRef.innerText) > 0)
{
    // Disable / Enable Appropriate Fields
    countryRef.setAttribute("disabled","");
    dateRef.setAttribute("disabled","");
    departureAirportRef.setAttribute("disabled","");
    arrivalAirportRef.removeAttribute("disabled");
    
    // Make Web Service Request for Airports
    let url = "https://eng1003.monash/OpenFlights/airports/";
    let data = {
        country: countryInput,
        callback: "getAirportData"
    };
    webServiceRequest(url,data);
}