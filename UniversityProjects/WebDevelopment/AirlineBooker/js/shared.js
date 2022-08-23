/** 
 * shared.js 
 * Purpose: This file contains shared code that runs on all html pages
 * Team: 133
 * Author: Arthur Lee
 */
"use strict";

// Mapbox Token
const MAPBOX_TOKEN = "pk.eyJ1IjoiYXJ0aHVybHlyIiwiYSI6ImNrZnBhdzFpOTB5eHUycXM1ZTN4MnlxaXEifQ.HV9FzvnOCpRYUxXlENlRAw";

// Local Storage Keys
const USER_DATA_KEY = "localUserData";
const USER_INDEX_KEY = "selectedUserIndex";
const TRIP_DATA_KEY = "localTripData";
const TRIP_INDEX_KEY = "selectedTripIndex";
const IMPORTANT_PAGE_KEY = "lastImportantPage";

class Flight
{
    constructor(country = "",date = "",startAirport = "",endAirport = "")
    {
        this._country = country;
        this._date = date;
        this._startAirport = startAirport;
        this._endAirport = endAirport;
    }

    // Accessors
    get country() { return this._country; }
    get date() { return this._date; } 
    get startAirport() { return this._startAirport; }
    get endAirport() { return this._endAirport; } 

    // Mutators: NONE

    // Methods
    fromData(data)
    {
        this._country = data._country;
        this._date = data._date;
        this._startAirport = data._startAirport;
        this._endAirport = data._endAirport;
    }
}

class Trip
{
    constructor()
    {
        this._flights = [];
    }

    // Accessors
    get flights() { return this._flights; }
    get country() { return this._flights[0].country; }
    get date() { return this._flights[0].date; }
    get departure() { return this._flights[0].startAirport; }
    get arrival() { return this._flights[this._flights.length - 1].endAirport; }
    get count() { return this._flights.length; }
    get stops() { return this._flights.length - 1; }

    // Mutators: NONE

    // Methods
    addFlight(country,date,startAirport,endAirport)
    {
        let flight = new Flight(country,date,startAirport,endAirport);
        this._flights.push(flight);
    }
    removePrevious()
    {
        this._flights.splice(this._flights.length - 1,1);
    }
    fromData(data)
    {
        let datalist = data._flights;
		this._flights = [];
		for (let i = 0; i < datalist.length; i++)
		{
			let flight = new Flight();
			flight.fromData(datalist[i]);
			this._flights.push(flight);
        }  
    }
}

class User
{
    constructor(name = "",email = "",password = "")
    {
        this._name = name;
        this._email = email;
        this._password = password;
        this._login = true;
        this._trips = [];
    }

    // Accessors
    get name() { return this._name; }
    get email() { return this._email; }
    get password() { return this._password; }
    get login() { return this._login; }
    get trips() { return this._trips; }

    // Mutators
    set name(name) { this._name = name; }
    set email(email) { this._email = email; }
    set password(password) { this._password = password; }
    set login(login) { this._login = login; }

    // Methods
    addTrip(trip)
    {
        this._trips.push(trip);
    }
    removeTrip(index)
    {
        this._trips.splice(index,1);
    }
    getTripIndex(trip)
    {
        for (let i = 0; i < this._trips.length; i++)
        {
            if (trip === this._trips[i])
            {
                return i;
            }
        }
    }
    getScheduled()
    {
        let today = new Date();
        today.setHours(0);
        today.setMinutes(0);
        today.setSeconds(0);
        today.setMilliseconds(0);
        let scheduled = [];
        for (let i = 0; i < this._trips.length; i++)
        {
            if (new Date(this._trips[i].date) >= today)
            {
                scheduled.push(this._trips[i]);
            }
        }
        return scheduled.sort((a,b) => new Date(b.date).getTime() - new Date(a.date).getTime());
    }
    getHistory()
    {
        let today = new Date();
        today.setHours(0);
        today.setMinutes(0);
        today.setSeconds(0);
        today.setMilliseconds(0);
        let history = [];
        for (let i = 0; i < this._trips.length; i++)
        {
            if (new Date(this._trips[i].date) < today)
            {
                history.push(this._trips[i]);
            }
        }
        return history.sort((a,b) => new Date(b.date).getTime() - new Date(a.date).getTime());
    }
    fromData(data)
    {
        this._name = data._name;
        this._email = data._email;
        this._password = data._password;
        this._login = data._login;

        // Trips
        let trips = data._trips;
        this._trips = [];
        for (let i = 0; i < trips.length; i++)
		{
			let trip = new Trip();
			trip.fromData(trips[i]);
            this._trips.push(trip);
        }
    }
}

class UserList
{
    constructor()
    {
        this._users = [];
    }

    // Accessors
    get users() { return this._users; }
    get count() { return this._users.length; }
    
    // Mutators: NONE

    // Methods
    addUser(name,email,password)
    {
        let user = new User(name,email,password);
        this._users.push(user);
    }
    getUser(index)
    {
        return this._users[index];
    }
    fromData(data)
    {
        this._users = [];
        let datalist = data._users;
		for(let i = 0; i < datalist.length; i++)
		{
			let user = new User();
			user.fromData(datalist[i]);
            this._users.push(user);
        }
    }
}

/*
    This function checks if there is existing data in a specific key in local storage
    Parameters: 
        key: Key to check if data exists
    Returns: 
        A boolean (true - if data exists and contains some value, false - if data does not exist or is empty)
*/
function checkIfDataExistsLocalStorage(key)
{
    // Retrieve data from LOCKER_DATA_KEY
    let data = retrieveData(key);

    // Check if data exists
    if (typeof(data) !== "undefined" && data !== null && data !== undefined && data !== "")
    {
        return true;
    }
    else
    {
        return false;
    }
}

/*  
    This function is responsible for storing data into Local Storage at a specififc key.
    Parameters: 
        data: Data to be stored in local storage
        key: Key to store data in
    Returns:
        -
*/
function storeData(data,key)
{
    // Check if Data is object
    if (typeof data === "object")
    {
        data = JSON.stringify(data);
    }

    // Store data into local storage
    localStorage.setItem(key,data);
}

/*  
    This function is responsible for retrieving data from Local Storage from a specififc key.
    Parameters: 
        key: Key retrieve data from
    Returns:
        data: Data in stored in key 
*/
function retrieveData(key)
{
    // Retrieve data from local storage
    let data = localStorage.getItem(key);

    // Return Data
    try
    {
        data = JSON.parse(data);
    }
    catch(e)
    {
        console.log(e);
    }
    finally
    {
        return data;
    }
}

/*
    This function creates HTML for the options in a datalist using data in an array
    Parameters:
        array: An array of data
    Returns:
        output: HTML for datalist options
*/
function createDatalist(array)
{
    // Define and Initalise Output
    let output = "";

    // Loop through Array
    for (let i = 0; i < array.length; i++)
    {
        output += '<option value="' + array[i] + '">';
    }
    
    // Return Output
    return output;
}

/*
    This function checks if a country is a valid country by refering to the countryData array
    Parameters:
        country: Name of a country to check if valid
    Returns:
        boolean (true if country is in countryData; false if country is not in countryData)
*/
function checkCountryValid(country)
{
    // Loop through countryData array
    for (let i = 0; i < countryData.length; i++)
    {
        // If in list, return true
        if (country === countryData[i])
        {
            return true;
        }
    }
    // Else, return false
    return false;
}

/*
    This function generates a random hexadecimal value
    Parameters:
        -
    Returns:
        Random hexadecimal number
*/
function randomHex()
{
    // Obtained From: https://www.w3resource.com/javascript-exercises/fundamental/javascript-fundamental-exercise-11.php
    return (Math.random() * 0xfffff * 1000000).toString(16).slice(0,6);
}

/*
    This function converts a date into the format yyyy-MM-dd
    Parameters:
        date: A date with datatype date
    Returns:
        dateHTML: Date in form of yyyy-MM-dd as a string
*/
function dateHTML(date)
{
    // Get Year, Month, and Date
    let year = date.getFullYear();
    let month = date.getMonth() + 1;
    let day = date.getDate();
    
    // Add Zero in front for appropriate months and days
    if (month < 10)
    {
        month = "0" + month;
    }
    if (day < 10)
    {
        day = "0" + day;
    }
    
    // Concatenate Values 
    let dateHTML = year + "-" + month + "-" + day;
    return dateHTML;
}

/*
    This function converts a date object into the form dd/mm/yyyy
    Parameters:
        date: A date object
    Returns:
        A date in the form of the string dd/mm/yyyy
*/
function dateString(date)
{
    let dd = String(date.getDate()).padStart(2, '0');
    let mm = String(date.getMonth() + 1).padStart(2, '0'); //January is 0!
    let yyyy = date.getFullYear();
    return dd + '/' + mm + '/' + yyyy;
}

/*
    Global Code
*/
// Create Global UserList class instance
let userList = new UserList();

// Create Global Trip class instance
let trip = new Trip();

// User Variables
let user;
let userIndex;

// HTML Reference Variables
let profileRef = document.getElementById("profile");
let scheduledRef = document.getElementById("scheduled");
let historyRef = document.getElementById("history");

// Check if Local Storage is available
if (typeof(Storage) !== "undefined")
{
    // Check if existing user data exists and retrieve if it does
    if (checkIfDataExistsLocalStorage(USER_DATA_KEY))
    {
        let restore = retrieveData(USER_DATA_KEY);
        userList.fromData(restore);
    }

    // Check if existing user index exists and retrieve if does
    if (checkIfDataExistsLocalStorage(USER_INDEX_KEY))
    {
        // Get Appropriate User 
        userIndex = retrieveData(USER_INDEX_KEY);
        user = userList.getUser(userIndex);

        // Check if user logged in
        if (user.login)
        {
            // Update Display Accordingly
            profileRef.innerText = user.name;
            profileRef.setAttribute("href","user.html");
            scheduledRef.setAttribute("href","scheduled.html");
            historyRef.setAttribute("href","history.html");
        }
        else
        {
            // Update Display Accordingly
            profileRef.innerText = "Login";
            profileRef.setAttribute("href","login.html");
            scheduledRef.setAttribute("href","login.html");
            historyRef.setAttribute("href","login.html");
        }
    }
    else
    {
        // Update Display Accordingly
        profileRef.innerText = "Login";
        profileRef.setAttribute("href","login.html");
        scheduledRef.setAttribute("href","login.html");
        historyRef.setAttribute("href","login.html");
    }   
}
else
{
    console.error("Local Storage is not supported by current browser.");
}

