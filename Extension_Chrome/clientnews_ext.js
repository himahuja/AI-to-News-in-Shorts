/////// CREATING VARAIBLE FOR AJAX /////////////////////
var xmlhttp;
var time;
var counter; //pseudo variable
var php = 'http://localhost/NIS/AI-to-News-in-Shorts/Extension_Chrome/getnews_ext.php';
///////////////////////////////////////////////////////
//////////////////////////////////////////////////////


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
//////////////////////////////////////////////////////////////
////////////////////// stateChange ///////////////////////////
/////////////////////////////////////////////////////////////
function stateChange() {
  if(xmlhttp.readyState == 4 && xmlhttp.status == 200){
    document.body.innerHTML = xmlhttp.responseText;
  }
}
//////////////////////////////////////////////////////////////
//////////////////////TIME RECODRING HELPERS/////////////////
/////////////////////////////////////////////////////////////
function timeReset(){
  time = 0;
}
function timeAdd(){
  time = time + 1;
}
/////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////

/*
██████  ███████  █████  ██████        ███    ███  ██████  ██████  ███████
██   ██ ██      ██   ██ ██   ██       ████  ████ ██    ██ ██   ██ ██
██████  █████   ███████ ██   ██       ██ ████ ██ ██    ██ ██████  █████
██   ██ ██      ██   ██ ██   ██       ██  ██  ██ ██    ██ ██   ██ ██
██   ██ ███████ ██   ██ ██████        ██      ██  ██████  ██   ██ ███████
*/
document.addEventListener('DOMContentLoaded', function() {
  if( document.getElementById('morenews')){
    // onClick's logic below:
    document.getElementById('morenews').addEventListener('click', readmorenews);
  }
});


function readmorenews(){
  console.log('Well! Hello good reader!')
  xmlhttp = new GetXmlHttpObject;
  if(xmlhttp == null){
    alert("Your browser does not support XMLHTTP!");
    return;
  }
  var article = php;
  var iid = document.getElementById('identity').innerHTML;
  article = article + "?iid=" + iid;
  var temp = 1;
  article = article + "&readmore=" + temp;
  article = article + "&t=" + time;
  xmlhttp.onreadystatechange = stateChange;
  xmlhttp.open("GET", article, true);
  xmlhttp.send(null);
  timeReset();
  clearInterval(counter);
  counter = setInterval(timeAdd, 2000);
  return true;
}

/*
██████   ██████   ██████  ██   ██ ███    ███  █████  ██████  ██   ██
██   ██ ██    ██ ██    ██ ██  ██  ████  ████ ██   ██ ██   ██ ██  ██
██████  ██    ██ ██    ██ █████   ██ ████ ██ ███████ ██████  █████
██   ██ ██    ██ ██    ██ ██  ██  ██  ██  ██ ██   ██ ██   ██ ██  ██
██████   ██████   ██████  ██   ██ ██      ██ ██   ██ ██   ██ ██   ██
*/

function bookmarknews(){
  var bookmark;
  button = document.getElementById('switch')
  if (button.classList.contains('switchoff')){
    button.className = "switchon";
    bookmark = 1;
  }
  else if(button.classList.contains('switchon')){
    button.className = "switchoff";
    bookmark = 0;
  }
  xmlhttp = new GetXmlHttpObject;
  if(xmlhttp == null){
    alert("Your browser does not support XMLHTTP!");
    return;
  }
  var article = php;
  var iid = document.getElementById('identity').innerHTML;
  article = article + "?iid=" + iid;
  article = article + "&bookmark=" + bookmark;
  article = article + "&t=" + time;
  xmlhttp.onreadystatechange = stateChange;
  xmlhttp.open("GET", article, true);
  xmlhttp.send(null);
  timeReset();
  clearInterval(counter);
  counter = setInterval(timeAdd, 2000);
  console.log('Bookmark' + iid + " " + bookmark);
}

window.addEventListener('DOMContentLoaded', function() {
  if( document.getElementById('switch')){
    // onClick's logic below:
    document.getElementById('switch').addEventListener('click', bookmarknews);
  }
});

/*
██       ██████   █████  ██████      ███████ ██ ██████  ███████ ████████
██      ██    ██ ██   ██ ██   ██     ██      ██ ██   ██ ██         ██
██      ██    ██ ███████ ██   ██     █████   ██ ██████  ███████    ██
██      ██    ██ ██   ██ ██   ██     ██      ██ ██   ██      ██    ██
███████  ██████  ██   ██ ██████      ██      ██ ██   ██ ███████    ██
*/

window.addEventListener('DOMContentLoaded', function() {
  document.getElementById("everything").addEventListener("load", loadfirstarticle);
});

function loadfirstarticle(){
  xmlhttp = new GetXmlHttpObject;
  if(xmlhttp == null){
    alert("Your browser does not support XMLHTTP!");
    return;
  }
  var article = php;
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

/*
 ██████ ██   ██  █████  ███    ██  ██████  ███████     ███    ██ ███████ ██     ██ ███████
██      ██   ██ ██   ██ ████   ██ ██       ██          ████   ██ ██      ██     ██ ██
██      ███████ ███████ ██ ██  ██ ██   ███ █████       ██ ██  ██ █████   ██  █  ██ ███████
██      ██   ██ ██   ██ ██  ██ ██ ██    ██ ██          ██  ██ ██ ██      ██ ███ ██      ██
 ██████ ██   ██ ██   ██ ██   ████  ██████  ███████     ██   ████ ███████  ███ ███  ███████
*/


document.onkeydown = function(e) {

  e = e || window.event;
  xmlhttp = new GetXmlHttpObject;
  if(xmlhttp == null){
    alert("Your browser does not support XMLHTTP!");
    return;
  }

  var article = php;
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
