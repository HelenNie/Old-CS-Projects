$(document).ready(function() {
  $(".hideFirst").hide();

  var url = window.location.href;
  //var url = "http://web.mit.edu/2.744/www/Results/studentSubmissions/conceptSketches/honey_badger/znie/";
  var keyIndex = url.indexOf("honey_badger")+13;
  var keyPlus = url.substring(keyIndex);
  var endIndex = keyPlus.indexOf("/");
  if (endIndex == -1) {
    endIndex = keyPlus.length;
  }
  var key = keyPlus.substring(0,endIndex);

  if (key == "storyboard") {
    $("#storyboard").show();
    $("#storyboard-tab").addClass("current");
  } else {
    $("#"+key).show();
    $("#subtabs").show();
    $("#"+key+"-tab").addClass("current");
  }

});

function showStoryboard() {
  $(".hideFirst").hide();
  $("#storyboard").show();
}

function showConceptSketches() {
  $(".hideFirst").hide();
  $("#subtabs").show();
  $("#hehuynh").show();
  $("#subtabs a").removeClass("current");
  $("#hehuynh-tab").addClass("current");
}

function switchConceptSketch(elem) {
  $(".subtabDiv").hide();
  var divId = elem.id.split('-')[0];
  $("#"+divId).show();
}

$(function () {
$("#tabs a").click(function (e) {
  e.preventDefault();
  $("#tabs a").addClass("current").not(this).removeClass("current");
});
});

$(function () {
$("#subtabs a").click(function (e) {
  e.preventDefault();
  $("#subtabs a").addClass("current").not(this).removeClass("current");
});
});
