/** 
 * summaryDetailed.js 
 * Purpose: This file contains shared code that runs on summaryDetailed.html
 * Team: 133
 * Author: Cheryl Lau
 */
"use strict";

/*
    This function to lists the names of all airport stops within the trip.
    Parameters:
        -
    Returns:
        output: A string of all airport stops
        non: String "N/A" if there are no airport stops
*/
function displayStops() 
{
    if (chosenTrip.flights.length>=2)
    {
        let output = "<ol>";
        for (let i = 0; i<chosenTrip.flights.length-1; i++) 
        {
            output += `<h5><li>${chosenTrip.flights[i].endAirport}</li></h5>`;
        }
        return output + "</ol>";
    }
    else
    {
        let non = "<h5 style='text-align:center;'>N/A</h5>";
        return non;
    }
}

/* 
    This is the callback function to find information for all airports in trip such as its coordinates into
    order to be displayed on a map.
    Parameters:
        data: Data returned by web service
    Returns:
        -
*/
function airportMarker(data)
{
    // finding coordinates of departure airport to use as center of map displayed
    let firstAirport = chosenTrip.departure;
    let centerCoorIndex = data.findIndex(
        function (airportCoor) 
        {
            return airportCoor.name == firstAirport;
        }
    )
    let centerCoor = [data[centerCoorIndex].longitude,data[centerCoorIndex].latitude];

    // displaying temporary map 
    mapboxgl.accessToken = MAPBOX_TOKEN;
    let map = new mapboxgl.Map({
        container: "map",
        style: "mapbox://styles/mapbox/streets-v9", // stylesheet location
        center: centerCoor, // starting position [lng, lat]
        zoom: 5 // starting zoom
    });
    // display markers and pop ups for departure airport
    let marker = new mapboxgl.Marker({ "color": "#FF0000" });
    marker.setLngLat(centerCoor);

    let popup = new mapboxgl.Popup({ offset: 45 });
    popup.setHTML(`Airport:${firstAirport}<br>Location:${chosenTrip.country}`);

    marker.setPopup(popup)

    // Display the marker.
    marker.addTo(map);

    // Display the popup.
    popup.addTo(map);

    // create source for route lines
    let object =
    {
        type: "geojson",
        data: {
            type: "Feature",
            properties: {},
            geometry: {
                type: "LineString",
                coordinates: []
            }
        }
    };
    object.data.geometry.coordinates[0] = centerCoor;

    // display markers and pop ups of the remaining airports
    for (let i = 0; i < chosenTrip.flights.length; i++) 
    {
        let airport= chosenTrip.flights[i].endAirport;
        let result1 = data.findIndex(
            function (airportName) 
            {
                return airportName.name == airport;
            }
        )

        // declaring airport coordinates
        let airportLat = data[result1].latitude;
        let airportLng = data[result1].longitude;
        let coordinates = [airportLng, airportLat];

        // declaring airport city
        let airportCity = data[result1].city;
        
        // setting markers and pop ups
        // set last airport marker to be red
        let marker = new mapboxgl.Marker({ "color": "#0000FF" });
        if (i==chosenTrip.flights.length-1)
        {
            marker = new mapboxgl.Marker({ "color": "#FF0000" });
        }
        marker.setLngLat(coordinates);

        let popup = new mapboxgl.Popup({ offset: 45 });
        popup.setHTML(`Airport:${airport}<br>Location:${airportCity}`);

        marker.setPopup(popup)

        // Display the marker.
        marker.addTo(map);

        // Display the popup.
        popup.addTo(map);
    
	    object.data.geometry.coordinates[i+1] = coordinates;
    }
    // display lines of routes
    map.on("load", function () {
        map.addLayer({
            id: "map",
            type: "line",
            source: object,
            layout: { "line-join": "round", "line-cap": "round" },
            paint: { "line-color": "#888", "line-width": 6 }
        })
    })
}

/*
    Global Code
*/
// Obtain index of trip chosen by user
let tripIndex = retrieveData(TRIP_INDEX_KEY);

// Displaying country,date,departure,arrival,number of stops and route
let chosenTrip = user.trips[tripIndex];
document.getElementById("chosenCountry").innerHTML = chosenTrip.country;
document.getElementById("chosenDate").innerHTML = dateString(new Date(chosenTrip.date));
document.getElementById("chosenDepartureAirport").innerHTML = chosenTrip.departure;
document.getElementById("chosenArrivalAirport").innerHTML = chosenTrip.arrival;
document.getElementById("numStops").innerHTML = chosenTrip.stops;
document.getElementById("stopList").innerHTML = displayStops();

// Creating web service link
let url =`https://eng1003.monash/OpenFlights/airports/?country=${chosenTrip.country}&callback=airportMarker`;
let script = document.createElement('script');
script.src = url;
document.body.appendChild(script);
