/////// CREATING VARAIBLE FOR AJAX /////////////////////
var xmlhttp;
////////////// CREATING REQUEST OBJECT ////////////////
function GetXmlHttpObject(){
  if(window.XMLHttpRequest){
    return new XMLHttpRequest();
  }
  else if(window.ActiveXObject){
    return new ActiveXObject("Microsoft.XMLHTTP")
  }
  else{
    return null
  }
}
////////////////////// stateChange ///////////////////////////

function stateChange() {
  if(xmlhttp.readyState == 4 && xmlhttp.status == 200){
    document.getElementById("container").innerHTML = xmlhttp.responseText;
  }
}

///////////////// change news function /////////////////
document.onkeydown = function(e) {
  e = e || window.event;
  xmlhttp = new GetXmlHttpObject;
  if(xmlhttp == null){
    alert("Your browser does not support XMLHTTP!");
    return;
  }

  var article = "getnews.php";
  article = article + "?dir=" + e.keyCode;
  var iid = document.getElementById("identity").innerHTML;
  if (iid == null){
    iid = 0;
  }
  article = article + "&iid=" + iid;
  article = article + "&sid=" + Math.random();
  xmlhttp.onreadystatechange = stateChange;
  xmlhttp.open("GET", article, true);
  xmlhttp.send(null);
}
/////////////////////////////////////////////////
