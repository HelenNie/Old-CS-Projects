/**
* Makes a person object
* @param : string id, string first, string last, string grade, list rooms
* @return : N/A
*/

var person = function(id, first, last, grade, rooms) {
    this.id = id;
    this.first = first;
    this.last = last;
    this.grade = grade;
    this.rooms = rooms;
}

/**
* Makes a list using the room numbers entered in the form
* @param : N/A
* @return : returns the list
*/

var makeRoomList = function() {
    var rmlist = [];
    for (var i=0; i<$(".rooms").length; i++) 
	rmlist.push($(".rooms")[i].value);
    console.log(rmlist);
    return rmlist;
}

/**
* Makes a new person object with the info in the form. Saves the person object.
* @param : N/A
* @return : N/A
*/

var createAccount = function() {
    var p1 = new person($("#idnum")[0].value, $("#first")[0].value, $("#last")[0].value, $("#grade")[0].value, makeRoomList());
    console.log(JSON.stringify(p1));
    saveAccount(p1);
}


/**
* Uses AJAX to send user's info to database for storage. Notifies user if account was made or if ID is already registered. Allows user to login with newly registered ID.
* @param : person p1
* @return : N/A
*/

var saveAccount = function(p1) {
    $.getJSON("/saveData", {id:p1['id'], first:p1['first'], last:p1['last'], grade:p1['grade'], room1:p1['rooms'][0], room2:p1['rooms'][1], room3:p1['rooms'][2], room4:p1['rooms'][3], room5:p1['rooms'][4], room6:p1['rooms'][5], room7:p1['rooms'][6], room8:p1['rooms'][7], room9:p1['rooms'][8], room10:p1['rooms'][9]}, function(bool) {
	console.log(bool);
	if (!bool)
	    $("#message").text("Sorry, an account by that ID already exists. Please sign up another account.");
	else
	    $("#success").show();
    });
}


/**
* Binds submit button to createAccount method
* @param : N/A
* @return : N/A
*/

$(document).ready(function() {
    $("#submit").click(createAccount);
});