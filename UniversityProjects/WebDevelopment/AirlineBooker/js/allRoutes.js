/** 
 * allRoutes.js
 * Purpose: This file contains code that will run on allRoutes.html
 * Team: 133
 * Author: Arthur Lee
 */
"use strict";

/*
    This function validates the user's country input and if valid displays a map of the selected country and collects the airport
    data of that country.
    Parameters:
        -
    Returns:
        -
*/
function getAirports()
{
    // Check if country is valid
    if (checkCountryValid(countryRef.value))
    {
        // Clear Error and Map
        countryErrorRef.innerText = "";
        map = "";

        // Display map
        mapboxgl.accessToken = MAPBOX_TOKEN;
        let mapboxClient = mapboxSdk({ accessToken: mapboxgl.accessToken });
        mapboxClient.geocoding
            .forwardGeocode({
                query: countryRef.value,
                autocomplete: false,
                limit: 1
            })
            .send()
            .then(function (response) {
                if (response && response.body && response.body.features && response.body.features.length) 
                {
                    let feature = response.body.features[0];

                    map = new mapboxgl.Map({
                        container: 'map',
                        style: 'mapbox://styles/mapbox/streets-v11',
                        center: feature.center,
                        zoom: 4,
                    });
                }
            });
            
        // Make Web Service Request
        let url = "https://eng1003.monash/OpenFlights/airports/";
        let data = {
            country: countryRef.value,
            callback: "generateAirportList"
        };
        webServiceRequest(url,data);
    }
    else
    {
        countryErrorRef.innerText = "Please input a valid country!";
    }
}

/*
    This function transfers the collected airport data into a global variable and collects the data of all routes in a country
    Parameters:
        -
    Returns:
        -
*/
function generateAirportList(airportData)
{
    // Transfer Airport Data to Global Variable
    airports = airportData;

    // Make Web Service Request
    let url = "https://eng1003.monash/OpenFlights/allroutes/";
    let data = {
        country: countryRef.value,
        callback: "generateAllRoutes"
    }
    webServiceRequest(url,data);
}

/*
    This function is displays the appropriate markers, popups, and lines on the map for each route
    Parameters:
        -
    Returns:
        -
*/
function generateAllRoutes(allRoutes)
{
    // Initialise and Define Source / Destination Airport Coords
    let sourceCoordList = [];
    let destinationCoordList = [];

    // Loop through All Routes
    for (let i = 0; i < allRoutes.length; i++)
    {
        // Initialise Variables
        let route = allRoutes[i];
        let color = "#" + randomHex();

        // Source Airport Variables
        let sourceAirportId = String(route.sourceAirportId)
        let sourceCoord = []; // [lng, lat]
        let sourceAirportName = "";
        let sourceAirportCity = "";
        let sourceAirportCountry = "";

        // Destination Airport Variables
        let destinationAirportId = String(route.destinationAirportId);
        let destinationCoord = []; // [lng, lat]
        let destinationAirportName = "";
        let destinationAirportCity = "";
        let destinationAirportCountry = "";

        // Find airport info in airports array
        let sourceAirport = airports.find(airport => airport.airportId === sourceAirportId);
        if (typeof(sourceAirport) !== "undefined")
        {
            sourceCoord = [sourceAirport.longitude,sourceAirport.latitude];
            sourceAirportName = sourceAirport.name;
            sourceAirportCity = sourceAirport.city;
            sourceAirportCountry = sourceAirport.country;
        }
        let destinationAirport = airports.find(airport => airport.airportId === destinationAirportId);
        if (typeof(destinationAirport) !== "undefined")
        {
            destinationCoord = [destinationAirport.longitude,destinationAirport.latitude];
            destinationAirportName = destinationAirport.name;
            destinationAirportCity = destinationAirport.city;
            destinationAirportCountry = destinationAirport.country;
        }

        // Check if coordinates are valid
        if (sourceCoord.length !== 0 && destinationCoord.length !== 0)
        {
            // Update Source / Destination Coords with valid Coords
            sourceCoordList.push(sourceCoord);
            destinationCoordList.push(destinationCoord);

            // Create markers with the set to appropriate coordinates
            let sourceMarker = new mapboxgl.Marker({ "color": "#FF0000" });
            let destinationMarker = new mapboxgl.Marker({ "color": "#FF0000" });
            sourceMarker.setLngLat(sourceCoord);
            destinationMarker.setLngLat(destinationCoord);

            // Create the respective popups
            let sourcePopup = new mapboxgl.Popup({ offset: 45});
            let destinationPopup = new mapboxgl.Popup({ offset: 45});

            // Set Popup Descriptions
            sourcePopup.setHTML("Airport: " + sourceAirportName + "<br>Location: " + sourceAirportCity + ", " + sourceAirportCountry);
            destinationPopup.setHTML("Airport: " + destinationAirportName + "<br>Location: " + destinationAirportCity + ", " + destinationAirportCountry);

            // Set Markers to Popups
            sourceMarker.setPopup(sourcePopup);
            destinationMarker.setPopup(destinationPopup);

            // Display the markers
            sourceMarker.addTo(map);
            destinationMarker.addTo(map);

            // Display the popups
            sourcePopup.addTo(map); 
            destinationPopup.addTo(map); 

            // Create Source for Lines
            let object = {
                type: "geojson",
                data: {
                    type: "Feature",
                    properties: {},
                    geometry: {
                        type: "LineString",
                        coordinates: [sourceCoord,destinationCoord]
                    }
                }
            };
        
            // Display Lines on Map
            map.addLayer({
                id: String(Math.random()),
                type: "line",
                source: object,
                layout: { "line-join": "round", "line-cap": "round" },
                paint: { "line-color": color, "line-width": 6 }
            });
        }
    }

    // Check if no route data in country
    if (sourceCoordList.length === 0 || destinationCoordList.length === 0)
    {
        countryErrorRef.innerText = "This country has no available flight route data. Please try another country.";
    }
}

/* 
    Global Code
*/
// HTML Reference Variables
let countriesRef = document.getElementById("countries");
let countryRef = document.getElementById("country");
let countryErrorRef = document.getElementById("countryError");

// Initialise Important Variables
let map;
let airports = [];

// Create Country Datalist
countriesRef.innerHTML = createDatalist(countryData);