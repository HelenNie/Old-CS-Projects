//loads the dropdown with the movies

function getDropdown(){
    $.getJSON("/get_dropdown", function(data) {
        $("#mlist").empty();
	if (data['ids'].length) > 0 {
        for (var i = -1; i < data['ids'].length; i++){
	    if (i == -1) {
		$("#mlist").append('<option value="'+000+'">' + "Select a movie to view its info:" + '<\p>');
	    }
	    else {
		var item=$('<option value="'+data['ids'][i]+'">'+data['titles'][i]+" "+data['dates'][i]+'</option>');
		$("#mlist").append(item);
	    }
        }
	}
	else {
	    console.log("nope");
	    $("#results").append("<b>" + "NO MOVIES FOUND! GO BACK TO SEARCH AGAIN" + "</b>");
	}
	$("#mlist").change(loadInfo);
    });
}
//loads the result stuff by calling getInfo
function loadInfo(data) {
    var moviestuff = $(this).attr('value')
    getInfo(moviestuff)
    
}
//fills the results div with the results
function getInfo(movie_id){
    var counter;
    counter = 0;
    $.getJSON("/get_info", {movie_id: movie_id}, function (data) {
//new_tab(data['review']);
	$('#results').empty();
	$('#ytapiplayer').empty();
	$("#movieTitle").empty();
	$("#movieTitle").append("<b>" + data['title'] + "</b>");
        for (var d in data) {
	    if (data[d] == null)
		$('#results').append('<p><b><i>' + d + ":"+ '</i></b>' + " unavailable" + '</p>');
	    else if (d == "review"){
		if (data[d] == "no review available")
		    $('#results').append('<p><b><i>' + d + ":"+ '</i></b>' + ' ' + data[d] + '<\p>');
		else{
		    $('#results').append('<p><b><i>' + d + ": " + '</i></b><a id="rlink" href="'+data[d]+'">' + data[d] + '</a><\p>');
		    $('#rlink').click(function() {
			$(this).attr('target', '_blank');
		    });
		}
	    }
	    else if (d == "similar movies"){
		$('#results').append('<p><b><i>' + d + ":"+ '</i></b></p>');
		$('#results').append('<select id="similar">' + '</select>');
		$('#similar').append('<option value="'+000+'">' + "Select a movie to view its info:" + '<\p>');
		var titles = [];
		var ids = [];
		var dates = [];
		var rtitles = data[d];
		for (var thing in rtitles){
		    id = rtitles[thing]['id'];
		    title = rtitles[thing]['title'];
		    date = rtitles[thing]['date'];
		    $('#similar').append('<option value="'+id+'">' + title + " " + date + '<\p>');
		}
	    }
	    else if (d != "trailer_id" && d != "id" ) {
		$('#results').append('<p><b><i>' + d + ":"+ '</i></b>' + ' ' + data[d] + '<\p>');
	    }
        }
	$('#similar').change(changePage);

//stuff with the youtube API. Works! Wooo!
	$('#noTrailer').empty();
	movie_trailer_id = data['trailer_id'];
	if (movie_trailer_id == 'IJNR2EpS0jw')
	    $('#noTrailer').append('<p id="no_trailer"><b>' + "The Trailer could not be found. Please enjoy 'Dumb Ways To Die' instead!" + '<b><p><br><br>');
	
	    var params = { allowScriptAccess: "always" };
	    var atts = { id: "myytplayer" };
	    $("#myytplayer").attr('data', "http://www.youtube.com/v/" + movie_trailer_id + "?enablejsapi=1&playerapiid=ytplayer&version=3");
	    var url = "http://www.youtube.com/v/" + movie_trailer_id + "?enablejsapi=1&playerapiid=ytplayer&version=3";
	    swfobject.embedSWF(url,"ytapiplayer","425", "356", "8", null, null, params, atts);
	
    });
}

function new_tab(url)
{
    window.open(url, '_blank');
    window.focus();
}


function changePage(data) {
    console.log("hi");
    var movieid = $(this).attr('value');
    getInfo(movieid);
}

//what's running
$(document).ready(function(){
    getDropdown();
});