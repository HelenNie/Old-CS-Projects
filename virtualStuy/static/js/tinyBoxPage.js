/**
* Sets up tinyBox page. Calls makeDefault to make rooms.
* @param : N/A
* @return : N/A
*/

var makeMap = function() {
    
    //gets the svg document
    var oddMap = $("#zoom-map-odd");
    var evenMap = $("#zoom-map-even");
    
    //gets the floor number
    var floor = parseFloat($("#floor").attr("value"));
    console.log(floor);

    //gets svg document info
    var width = parseFloat(oddMap.attr("width"));
    var height = parseFloat(oddMap.attr("height"));
    
    //sets rows and columns
    var cols = 21;

    //sets w h for each room
    var w = width / cols;
    var h = height;
    
    //builds floor
    switch (floor) {
    case 0:
	$("#message").append('<p>No floor to display</p>');
	break;
    case 1:
	makeDefault(oddMap, evenMap, floor, w, h);
	break;
    case 2:
	makeDefault(oddMap, evenMap, floor, w, h);
	break;
    case 3:
	makeDefault(oddMap, evenMap, floor, w, h);
	break;
    case 4:
	makeDefault(oddMap, evenMap, floor, w, h);
	break;
    case 5:
	makeDefault(oddMap, evenMap, floor, w, h);
	break;
    case 6:
	makeDefault(oddMap, evenMap, floor, w, h);
	break;
    case 7:
	makeDefault(oddMap, evenMap, floor, w, h);
	break;
    case 8:
	makeDefault(oddMap, evenMap, floor, w, h);
	break;
    case 9:
	makeDefault(oddMap, evenMap, floor, w, h);
	break;
    case 10:
	makeDefault(oddMap, evenMap, floor, w, h);
	break;
    }
}

/**
* Makes the rooms on the map
* @param : svn oddMap, svn evenMap, int floor, int w, int h
* @return : N/A
*/

var makeDefault = function(oddMap, evenMap, floor, w, h){
    var x = 0;
    var y = 0;
    
    var special = "gym";

    var svgns = "http://www.w3.org/2000/svg";

    oddMap.empty();
    evenMap.empty();

    if (floor == 5)
	special = "cafe";
	
    //makes odd-numbered rooms
    for (var i = 1; i < 43; i = i + 2) {
	
	room = floor * 100 + i;

	if (i == 41)
	    room = special;

        var newRoom = document.createElementNS(svgns, "rect");
        newRoom.setAttributeNS(null, 'class', 'room');
        newRoom.setAttributeNS(null, 'id', room);
        newRoom.setAttributeNS(null, 'x', x);
        newRoom.setAttributeNS(null, 'y', y);
        newRoom.setAttributeNS(null, 'width', w);
	newRoom.setAttributeNS(null, 'height', h);
        newRoom.setAttributeNS(null, 'stroke', 'black');
        newRoom.setAttributeNS(null, 'fill', 'white');	
	
	oddMap.append(newRoom);
	
	x = x + w;
    }

    x = 0;

    //makes even-numbered rooms
    for (var i = 0; i < 43; i = i + 2) {
	room = floor * 100 + i;
	
        var newRoom = document.createElementNS(svgns, "rect");
        newRoom.setAttributeNS(null, 'class', 'room');
        newRoom.setAttributeNS(null, 'id', room);
        newRoom.setAttributeNS(null, 'x', x);
        newRoom.setAttributeNS(null, 'y', y);
        newRoom.setAttributeNS(null, 'width', w);
	newRoom.setAttributeNS(null, 'height', h);
        newRoom.setAttributeNS(null, 'stroke', 'black');
        newRoom.setAttributeNS(null, 'fill', 'white');	

	evenMap.append(newRoom);
	x = x + w;
    }
}


/**
* Makes a bubble for each person and adds them to the correct rooms
* @param : N/A
* @return : N/A
*/   

var addPeople = function(){
    
    //gets the svg document
    var oddMap = $("#zoom-map-odd");
    var evenMap = $("#zoom-map-even");
    
    //gets the floor number
    var floor = parseFloat($("#floor").attr("value"));

    //gets svg document info
    var width = parseFloat(oddMap.attr("width"));
    var height = parseFloat(oddMap.attr("height"));
    
    //sets rows and columns
    var cols = 21;
    var rows = 3;

    //sets w h for each room
    var w = width / cols;
    var h = height;

    var room;
    var period = $("#period").attr('value');
    if (period == -1){
	period = 1;
    }

    var ids = [];
    for (var i = 0; i < $(".ID").length; i++){
	ids.push($(".ID")[i].value);
    }
    
    console.log(ids);
    console.log(period);

    var svgns = "http://www.w3.org/2000/svg";
    
    for (var j = 0; j < ids.length; j++){
	$.getJSON("/getProfileItems", {id:ids[j]}, function(profile){
	    var room = profile[4][period - 1];
	    var roomId = '#' + room;

	    //special cases (gym, cafe)
	    if (parseFloat(room) == 500){
		var myX = (parseFloat($("#cafe").attr('x')) + 10) + (Math.floor(Math.random() * (w - 20)));
		var myY = (parseFloat($("#cafe").attr('y')) + 10) + (Math.floor(Math.random() * (h - 20)));
		room = floor * 100 + 41;
	    }
	    else if (parseFloat(room) > floor * 100 + 40){
		var myX = (parseFloat($("#gym").attr('x')) + 10) + (Math.floor(Math.random() * (w - 20)));
		var myY = (parseFloat($("#gym").attr('y')) + 10) + (Math.floor(Math.random() * (h - 20)));
		room = floor * 100 + 41;
	    }
	    
	    //regular room numbers
	    else{
		var myX = (parseFloat($(roomId).attr('x')) + 10) + (Math.floor(Math.random() * (w - 20)));
		var myY = (parseFloat($(roomId).attr('y')) + 10) + (Math.floor(Math.random() * (h - 20)));
	    }

	    //makes the bubble
	    var newCircle = document.createElementNS(svgns, "circle");
	    newCircle.setAttributeNS(null, 'class', 'person');
	    newCircle.setAttributeNS(null, 'id', profile[0]);
	    newCircle.setAttributeNS(null, 'cx', myX); 
	    newCircle.setAttributeNS(null, 'cy', myY);
	    newCircle.setAttributeNS(null, 'r', 10);
	    newCircle.setAttributeNS(null, 'stroke', 'black');
	    var color;
	    switch (profile[3]) {
	    case 0:
                color = "red";
                break;
	    case "9":
		color = "green";
                break;
	    case "10":
                color = "brown";
                break;
	    case "11":
                color = "magenta";
                break;
	    case "12":
                color = "yellow";
                break;
	    }
	    newCircle.setAttributeNS(null, 'fill', color);
	    newCircle.setAttributeNS(null, 'onclick', 'getProfile(evt)');

	    switch (room % 2) {
	    case 1:
		oddMap.append(newCircle);
		break;
	    case 0:
		evenMap.append(newCircle);
		break;
	    }
	});	
    }
}

/*func getProfile()
**@params: none  
**This function, assigned on click to each bubble representing a student or teacher on the 10 svg maps takes the ID number/keyword of the clicked user and calls the "getProfile" server-side method to return
the object the bubble represents. The profile information of this user/teacher will then be printed on a div at the bottom of the page. */


/**
* An event is triggered when a bubble is clicked. The bubble's ID is sent to database to retrieve the bubble's profile. The profile is displayed on the map
* @param : event evt
* @return : N/A
*/   

var getProfile = function(evt) {
    var c = evt.target;
    var proID = c.getAttribute("id");
    $.getJSON("/getProfile", {id:proID}, function(person) {
        $("#restOfProfiles").empty();
        $("#schedule").empty();
        console.log(person);
        $("#restOfProfiles").append(person[0]);
        $("#schedule").append(person[1]);
    });
}


/**
* hides the profile is it being displayed in the tinyBox
* @param : N/A
* @return : N/A
*/   

var hideProfile = function() {
    $("#restOfProfiles").empty();
    $("#schedule").empty();
}

/**
* Makes the map. Adds the bubbles to it. Binds the "hide profile" button to the hideProfile method.
* @param : N/A
* @return : N/A
*/   

$(document).ready(function() {
    makeMap();
    addPeople();
    $("#hideProfile").click(hideProfile);
});

