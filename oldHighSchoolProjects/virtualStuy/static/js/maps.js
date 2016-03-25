//sets the current period as a global variable
var currPd;

/**
* Loads student/teacher location onto svgs based on period
* @param: none
* @return: none
**/
var loadMaps = function() {

    $.getJSON("/getPeople", function(people) {
	console.log(people);
	$(".person").remove();
	var svgns = "http://www.w3.org/2000/svg";
	for (var i in people) {
	    var newCircle = document.createElementNS(svgns, "circle");
	    newCircle.setAttributeNS(null, 'class', 'person');
	    newCircle.setAttributeNS(null, 'id', people[i][0]);
	    newCircle.setAttributeNS(null, 'cx', 5 + Math.floor(Math.random()*490));
	    newCircle.setAttributeNS(null, 'cy', 5 + Math.floor(Math.random()*15));
	    newCircle.setAttributeNS(null, 'r', 3);
	    newCircle.setAttributeNS(null, 'stroke', 'black');
	    var color;
	    switch (people[i][3]) {
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
	    
	    var f;
	    
	    try {
		//checks if currently outside school hours
		if (currPd == -1){
		    f = Math.floor(people[i][4][0] / 100);
		}
		else{
		    f = Math.floor(people[i][4][currPd -1] / 100);
		}

		switch (f){
		case 1:
		    $("#svg-one").append(newCircle);
		    break;
		case 2:
		    $("#svg-two").append(newCircle);
		    break;
		case 3:
		    $("#svg-three").append(newCircle);
		    break;
		case 4:
		    $("#svg-four").append(newCircle);
		    break;
		case 5:
		    $("#svg-five").append(newCircle);
		    break;
		case 6:
		    $("#svg-six").append(newCircle);
		    break;
		case 7:
		    $("#svg-seven").append(newCircle);
		    break;
		case 8:
		    $("#svg-eight").append(newCircle);
		    break;
		case 9:
		    $("#svg-nine").append(newCircle);
		    break;
		case 10:
		    $("#svg-ten").append(newCircle);
		break;
		}
	    }
	    catch(err){
	    }
	}
    });
}


/**
* Takes id of a particular bubble; displays profile at bottom
* @params: each bubble is tied to the event
* @return: compiles String representing profile from server 
**/
var getProfile = function(evt) {
    var circle = evt.target;
    var myID = circle.getAttribute("id");
    $.getJSON("/getProfile", {id:myID}, function(person) {
	$("#restOfProfiles").empty();
	$("#schedule").empty();
	console.log(person);
	$("#restOfProfiles").append(person[0]);
	$("#schedule").append(person[1]);
  
	//JSON.stringify(person)	
    });
    //scroll down automatically
    $('html, body').animate({ scrollTop: $(document).height()},'50');
}

/**
* Based on the value of the grades drop down, loads the bubbles of that grade
* @params: option chosen in grades drop-down
* @return: none
**/

var loadMapsByGrade = function() {

    var grade = $(".choose-grade")[0].value;
   
    if (grade == "13"){
	loadMaps();
	return;
    }
	
    $.getJSON("/getPeopleByGrade", {grade:grade}, function(people) {
	console.log(people);
	
	$(".person").remove();
	var svgns = "http://www.w3.org/2000/svg";
	for (var i in people) {
	    var newCircle = document.createElementNS(svgns, "circle");
	    newCircle.setAttributeNS(null, 'class', 'person');
	    newCircle.setAttributeNS(null, 'id', people[i][0]);
	    newCircle.setAttributeNS(null, 'cx', 5 + Math.floor(Math.random()*490));
	    newCircle.setAttributeNS(null, 'cy', 5 + Math.floor(Math.random()*15));
	    newCircle.setAttributeNS(null, 'r', 3);
	    newCircle.setAttributeNS(null, 'stroke', 'black');
	    var color;
	    switch (people[i][3]) {
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
	   

	    var f;
	    
	    try {
		//checks if currently outside school hours
		if (currPd == -1){
		    f = Math.floor(people[i][4][0] / 100);
		}
		else{
		    f = Math.floor(people[i][4][currPd -1] / 100);
		}

		switch (f){
		case 1:
		    $("#svg-one").append(newCircle);
		    break;
		case 2:
		    $("#svg-two").append(newCircle);
		    break;
		case 3:
		    $("#svg-three").append(newCircle);
		    break;
		case 4:
		    $("#svg-four").append(newCircle);
		    break;
		case 5:
		    $("#svg-five").append(newCircle);
		    break;
		case 6:
		    $("#svg-six").append(newCircle);
		    break;
		case 7:
		    $("#svg-seven").append(newCircle);
		    break;
		case 8:
		    $("#svg-eight").append(newCircle);
		    break;
		case 9:
		    $("#svg-nine").append(newCircle);
		    break;
		case 10:
		    $("#svg-ten").append(newCircle);
		    break;
		}
	    }
	    catch(err){
	    }
	}
    });
}

/**
* Changes currentPeriod based on current time. Default is 1st pd.
* @params: none
* @return: none
**/
var setPeriod = function() {
    //gets current time in a string
    var currTime = "01/01/2011 ".concat(new Date().toString().split(" ")[4]);

    //uncomment the next line to test during outside school hours
    //var currTime = "01/01/2011 09:09:09";

    //console.log(currTime);

    //makes a list of the beginnings of pds                          
    var pds = ["01/01/2011 08:00:00", "01/01/2011 08:45:00", 
	       "01/01/2011 09:30:00", "01/01/2011 10:19:00", 
	       "01/01/2011 11:04:00", "01/01/2011 11:49:00", 
	       "01/01/2011 12:34:00", "01/01/2011 13:19:00", 
	       "01/01/2011 14:04:00", "01/01/2011 14:49:00",
	       "01/01/2011 15:30:00"]
    
    //compares currTime with pds to find currPd    
    if (Date.parse(currTime) < Date.parse(pds[0]) ||
        Date.parse(currTime) > Date.parse(pds[10])){
        currPd = -1;
    }
    else{
        for (var i = 1; i <= 10; i++){
	    if (Date.parse(currTime) < Date.parse(pds[i])){
                currPd = i;
		break;
	    }
	}
    }
}


//varName = "";

/**
* Opens up tiny box with location-specific map upon clicking zoom button
* @params: each zoom button for each floor is bound to the event
* @return: calls the tinyBoxPage with a more specific zoomed map
**/
var zoom = function() {
    var svgName = "#svg-" + $(this)[0].id.substring(5);
    console.log(svgName);

    var circles = $("circle", $(svgName));
    var ids = [];
    $(circles).each(function() {
	ids.push($(this).attr("id"));
    });
   
    //console.log(ids);

    var idString = ids.join(",");

    console.log(idString);

    /*
    for (var i=0; i<ids.length; i++) {
	var varName = "id" + i;
	window[varName] = ids[i];

    }*/
   
    var svgID = ($(svgName).attr("id"));
    var myFloor = svgID.substring(4);

    //console.log(myFloor);

    switch(myFloor) {
    case "ten":
	myFloor = 10;
	break;
    case "nine":
	myFloor = 9;
	break;
    case "eight":
	myFloor = 8;
	break;
    case "seven":
	myFloor = 7;
	break;
    case "six":
	myFloor = 6;
	break;
    case "five":
	myFloor = 5;
	break;
    case "four":
	myFloor = 4;
	break;
    case "three":
	myFloor = 3;
	break;
    case "two":
	myFloor = 2;
	break;
    case "one":
	myFloor = 1;
	break;
    }

    //console.log(myFloor);

    $.getJSON("/getTinyBoxData", {floor:myFloor, period:currPd, idString:idString}, function(data) {
    });

    var content = '<Iframe Id="FrameTiny" Src="' + 'tinyBoxPage' + '" Width="100%" Height="100%" Scrolling="Yes" Frameborder="Yes" Marginwidth="10" Marginheight="10"></Iframe>';
    TINY.box.show({html: content, width: 1100, height:600});
    console.log("showing tiny box");
}

/**
* Based on person found by the keyword search, loads that one person on map. 
* @param: chosen result after keyword search
* @returns: none
**/

var loadMapsByPerson = function() {
    var id = $(".results")[0].value;
    console.log(id);
    
    $.getJSON("/getProfileItems", {id:id}, function(person) {
	console.log(person);
	
	$(".person").remove();
	var svgns = "http://www.w3.org/2000/svg";
	var newCircle = document.createElementNS(svgns, "circle");
	newCircle.setAttributeNS(null, 'class', 'person');
	newCircle.setAttributeNS(null, 'id', person[0]);
	newCircle.setAttributeNS(null, 'cx', 5 + Math.floor(Math.random()*490));
	newCircle.setAttributeNS(null, 'cy', 5 + Math.floor(Math.random()*15));
	newCircle.setAttributeNS(null, 'r', 3);
	newCircle.setAttributeNS(null, 'stroke', 'black');
	var color;
	switch (person[3]) {
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
	   
	var f;
	
	try {
	    //checks if currently outside school hours
	    if (currPd == -1){
		f = Math.floor(person[4][0] / 100);
	    }
	    else{
		f = Math.floor(person[4][currPd -1] / 100);
	    }
	    
	    switch (f){
	    case 1:
		$("#svg-one").append(newCircle);
		break;
	    case 2:
		$("#svg-two").append(newCircle);
		break;
	    case 3:
		$("#svg-three").append(newCircle);
		break;
	    case 4:
		$("#svg-four").append(newCircle);
		break;
	    case 5:
		$("#svg-five").append(newCircle);
		break;
	    case 6:
		$("#svg-six").append(newCircle);
		break;
	    case 7:
		$("#svg-seven").append(newCircle);
		break;
	    case 8:
		$("#svg-eight").append(newCircle);
		break;
	    case 9:
		$("#svg-nine").append(newCircle);
		break;
	    case 10:
		$("#svg-ten").append(newCircle);
		break;
	    }
	}
	catch(err){
	}
    });
}

/**
* takes search keyword and returns a list of result in a drop down
* @params: name typed into search bar
* @return: list of results that can be clicked on
**/

var loadResults = function() {
    var name = $("#searchName")[0].value;
    console.log(name);
    $.getJSON("/getSearchResults", {name:name}, function(list) {
	console.log(list);

	$(".results").empty();
	if (list.length == 0)
	    $(".results").append('<option value="'+'no'+'">'+'No Results'+'</option>');
	else {
	    $(".results").append('<option value="'+'no'+'">'+'Results Below'+'</option>');
	    for (person in list){
		$(".results").append('<option value="'+list[person][0]+'">'+list[person][1]+' '+list[person][2]+', '+list[person][3]+'</option>');
	    }
	}
    });
    $(".results").show();
    $(".results").change(loadMapsByPerson);
}

/**
* Binds search bar to respond to enter
* @params: none
* @return: none
**/
var enterKey = function(){
    e = window.event;
    if(e.which == 13) {
	e.preventDefault();
	$('#search').click();
    }
}
 
$(document).ready(function() {
    //finds the initial period
    setPeriod();
    var now = currPd;
    console.log(now);
    //tells server the initial period
    $.getJSON("/getPeriod", {period:now}, function(data) {
    });

    //loads the initial map
    loadMaps();

    //when grade is changed, reloads map with that specific grade
    $(".choose-grade").change(loadMapsByGrade);
    //binds search button to display a list of results based on keyword
    $("#search").click(loadResults);

    //binds all the zoom buttons to the zoom function to go into the tinybox
    $("#zoom-ten").click(zoom);
    $("#zoom-nine").click(zoom);
    $("#zoom-eight").click(zoom);
    $("#zoom-seven").click(zoom);
    $("#zoom-six").click(zoom);
    $("#zoom-five").click(zoom);
    $("#zoom-four").click(zoom);
    $("#zoom-three").click(zoom);
    $("#zoom-two").click(zoom);
    $("#zoom-one").click(zoom);

    //constantly checks to see if the period changed, and if so tells server
    setInterval(function() {
	var pdBefore = currPd;
	setPeriod();
	var pdAfter = currPd;
	if (pdBefore != pdAfter) {
	    $.getJSON("/getPeriod", {period:currPd}, function(data){
	    });
	    loadMaps();
	}
    }, 500);

});