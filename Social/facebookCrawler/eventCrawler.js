/**
 * @file Retrieving events around the four locations of the project
 * 		 from Facebooks Graph API in a specified time interval and within 
 * 		 a specified radius.
 * 		 Example usage: node eventCrawler.js 1970-01-01 2018-03-21 5000
 * @author Nico Daheim ndaheim@uni-koblenz.de
 * @requires facebook-events-by-location-core
 * @requires fs
 * @requires dotenv to load the FEBL_ACCESS_TOKEN environment variable
 * @arg The start of the interval considered for retrieval in any 
 * strtotime date value or unix timestamp as accepted by the Graph API
 * @arg The end of the interval considered for retrieval in any 
 * strtotime date value or unix timestamp as accepted by the Graph API
 * @arg [radius=10000] The radius considered for retrieval 
 */

var EventSearch = require("facebook-events-by-location-core");
/* @var {EventSearch} es - The nodejs module used for retrieval */
var es = new EventSearch();
/* @var fs - The nodejs filesystem module */
var fs = require('fs');
require('dotenv').config();
/* @var token - The app access token used for the Graph API */
var token = process.env.FEBL_ACCESS_TOKEN;

const ANTALYA = {
	name: "Antalya",
	lat: 36.852569,
	lng: 30.782124
};

const ANTWERPEN = {
	name: "Antwerpen",
	lat: 51.258820,
	lng: 4.355700
};

const CORK = {
	name: "Cork",
	lat: 51.902240,
	lng: -8.440441
};

const THESSALONIKI = {
	name: "Thessaloniki",
	lat: 40.444869,
	lng: 22.916779
};

const CITIES = [
	ANTALYA, 
	ANTWERPEN, 
	CORK, 
	THESSALONIKI
];

if(process.argv.length < 4) {
	throw Error("Expected parameters not given \nspecify start and end as " +
				 "strtotime date value or UNIX timestamp and optionally " +
				 "a radius as a Number");
}

var args = process.argv.slice(2);
/* @var {String} start of the interval */
var start = args[0];
/* @var {String} end of the interval */
var end = args[1];
/* @var {Number} the radius in metres within which events are retrieved */
var radius = args.size === 3 ? parseInt(args[2]) : 10000;

CITIES.forEach(city => {
	getEvents(city, start, end, radius);
});

/**
 * Retrieves and writes the Facebook events, which took/take place in the specified city within
 * the specified timeframe and radius into a JSON file
 * 
 * @param city 
 * @param {String} start Start of the interval
 * @param {End} end End of the interval
 * @param {Number} radius Radius used for retrieval 
 */ 
function getEvents(city, start, end, radius) {
	es.search({
	  "lat": city.lat,
	  "lng": city.lng,
	  "since": start,
	  "until": end,
	  "distance": radius,
	  "accessToken": token
	}).then(function (events) {
		console.log('Retrieved events in ' + city.name);
		var filename = city.name + '_' + start + '_' + end + '.json';
		writeFile(filename, JSON.stringify(events));
	}).catch(function (error) {
	    console.error(JSON.stringify(error));
	});
}

/**
 * Writes the given input into the specified file
 * 
 * @param {String} filename Name of the file to be written
 * @param {String} input content of the file
 */
function writeFile(filename, input) {
	const PATH = __dirname + '/outputs';
	// check if output folder exists and create it if it does not
    if (!fs.existsSync(PATH)) {
        fs.mkdir(PATH);
    }
    fs.appendFile(PATH + '/' + filename, input, function (err) {
        if (err) throw err;
        console.log('Saved events in ' + PATH + '/' + filename);
    }); 
}