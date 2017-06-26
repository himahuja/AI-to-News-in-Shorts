/////// CREATING VARAIBLE FOR AJAX /////////////////////
var xmlhttp;
var time;
var counter; //pseudo variable
/*
The iterator varibale allow different functionality on the same keydown event
*/
////////////// CREATING REQUEST OBJECT ////////////////
function GetXmlHttpObject(){
  if(window.XMLHttpRequest){
    return new XMLHttpRequest();
  }
  else if(window.ActiveXObject){
    return new ActiveXObject("Microsoft.XMLHTTP");
  }
  else{
    return null;
  }
}
////////////////////// stateChange ///////////////////////////
function stateChange() {
  if(xmlhttp.readyState == 4 && xmlhttp.status == 200){
    document.body.innerHTML = xmlhttp.responseText;
  }
}
/////////////////////////////////////////////////////////////////////
//////////////////////TIME RECODRING HELPERS/////////////////////////
function timeReset(){
  time = 0;
}
function timeAdd(){
  time = time + 1;
}
////////////////////////////////////////////////////////////////////
////////////////////// LOADING THE 1st ARTICLE /////////////////////
////////////////////////////////////////////////////////////////////
function loadfirstarticle(){

  xmlhttp = new GetXmlHttpObject;
  if(xmlhttp == null){
    alert("Your browser does not support XMLHTTP!");
    return;
  }
  var article = "getnews.php";
  var iid = 0
  var dir = 0
  article = article + "?dir=" + dir;
  article = article + "&iid=" + iid;
  article = article + "&t=0";
  xmlhttp.onreadystatechange = stateChange;
  xmlhttp.open("GET", article, true);
  xmlhttp.send(null);
  //Start the time counter after the first article is loaded
  timeReset();
  clearInterval(counter);
  counter = setInterval(timeAdd, 2000);
}

////////////////////////////////////////////////////////
///////////////// Change News Function /////////////////
///////////////////////////////////////////////////////
document.onkeydown = function(e) {
  //////////CREATING VARIABLES //////////////////
  e = e || window.event;
  xmlhttp = new GetXmlHttpObject;
  if(xmlhttp == null){
    alert("Your browser does not support XMLHTTP!");
    return;
  }

  var article = "getnews.php";
  article = article + "?dir=" + e.keyCode;
  var iid = document.getElementById("identity");
  if (iid == null){
    iid = 0;
  }
  else{
    iid = iid.innerHTML;
  }
  article = article + "&iid=" + iid;
  article = article + "&t=" + time;
  article = article + "&sid=" + Math.random();
  xmlhttp.onreadystatechange = stateChange;
  xmlhttp.open("GET", article, true);
  xmlhttp.send(null);
  timeReset();
  clearInterval(counter);
  counter = setInterval(timeAdd, 2000);
}
/////////////////////////////////////////////////
