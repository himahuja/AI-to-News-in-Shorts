<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "News-Articles";

// Create connection
$conn = mysqli_connect($servername, $username, $password, $dbname);
// Check connection
if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}

////////////////////
$last_iid = 154;
/////////////////


//// GETTING IID ////
$_iid = $_GET["iid"];
/////////////////////


/*
████████ ██ ███    ███ ███████
   ██    ██ ████  ████ ██
   ██    ██ ██ ████ ██ █████
   ██    ██ ██  ██  ██ ██
   ██    ██ ██      ██ ███████
*/



if(isset($_GET["t"])){
  $_t   = $_GET["t"];
  $update = "INSERT INTO stats (iid, bookmark, readmore, counter)
             VALUES ('$_iid', NULL, NULL, '$_t')
             ON DUPLICATE KEY UPDATE
             counter = counter + $_t";
  mysqli_query($conn, $update);
}

/*
██████  ███████  █████  ██████        ███    ███  ██████  ██████  ███████
██   ██ ██      ██   ██ ██   ██       ████  ████ ██    ██ ██   ██ ██
██████  █████   ███████ ██   ██       ██ ████ ██ ██    ██ ██████  █████
██   ██ ██      ██   ██ ██   ██       ██  ██  ██ ██    ██ ██   ██ ██
██   ██ ███████ ██   ██ ██████        ██      ██  ██████  ██   ██ ███████
*/

if(isset($_GET["readmore"])){
  $_readmore = $_GET["readmore"];
  if($_readmore === 1){
    $_readmore = 'Y';
  }
  $readmoreupdate = "INSERT INTO stats (iid, bookmark, readmore, counter)
             VALUES ('$_iid', NULL, '$_readmore', NULL)
             ON DUPLICATE KEY UPDATE
             readmore = '$_readmore'";
  mysqli_query($conn, $readmoreupdate);
}

/*
██████   ██████   ██████  ██   ██ ███    ███  █████  ██████  ██   ██
██   ██ ██    ██ ██    ██ ██  ██  ████  ████ ██   ██ ██   ██ ██  ██
██████  ██    ██ ██    ██ █████   ██ ████ ██ ███████ ██████  █████
██   ██ ██    ██ ██    ██ ██  ██  ██  ██  ██ ██   ██ ██   ██ ██  ██
██████   ██████   ██████  ██   ██ ██      ██ ██   ██ ██   ██ ██   ██
*/


if(isset($_GET["bookmark"])){
  $_bookmark = $_GET["bookmark"]? 'Y':'N';
  $bookmarkupdate =     "INSERT INTO stats (iid, bookmark, readmore, counter)
             VALUES ('$_iid', '$_bookmark', NULL, NULL)
             ON DUPLICATE KEY UPDATE
             bookmark = '$_bookmark'";
  mysqli_query($conn, $bookmarkupdate);
}

/*
██████  ██ ██████  ███████  ██████ ████████ ██  ██████  ███    ██
██   ██ ██ ██   ██ ██      ██         ██    ██ ██    ██ ████   ██
██   ██ ██ ██████  █████   ██         ██    ██ ██    ██ ██ ██  ██
██   ██ ██ ██   ██ ██      ██         ██    ██ ██    ██ ██  ██ ██
██████  ██ ██   ██ ███████  ██████    ██    ██  ██████  ██   ████
*/



if(isset($_GET["dir"])){
  $_dir = $_GET["dir"];
  if($_dir == 38 || $_dir == 37){
    $_dir = -1;
  }
  else if($_dir == 40 || $_dir == 39){
    $_dir = 1;
  }
  else{
    $_dir = 0;
  }
  ////////////// ADJUSTING IID //////////////
  if($_dir == -1 && $_iid == 0){
    $_iid = $last_iid;
  }

  else if($_dir == 1 && $_iid == $last_iid){
    $_iid = 0;
  }
  else{
    $_iid = $_iid + $_dir;
  }
}

/*
 ██████  ██    ██ ███████ ██████  ██    ██
██    ██ ██    ██ ██      ██   ██  ██  ██
██    ██ ██    ██ █████   ██████    ████
██ ▄▄ ██ ██    ██ ██      ██   ██    ██
 ██████   ██████  ███████ ██   ██    ██
    ▀▀
*/



$query = "SELECT iid, headline, articleBody, author, source, image
        FROM articles WHERE iid = '$_iid'";
$result = mysqli_query($conn, $query);

$bookmark_check = "SELECT iid, bookmark FROM stats WHERE iid = '$_iid'";
$result2 = mysqli_query($conn, $bookmark_check);

if (mysqli_num_rows($result) > 0) {
    // output data of each row
    while($row = mysqli_fetch_assoc($result)){
        echo "<div id='container'><section><article id = 'news-card'>
        <div id = 'identity' style='display:none'>".$row["iid"]."</div>";
        echo $row["image"];
        echo "<h1>".$row["headline"]."</h1>
        <p>".$row["author"]."</p>
        <p>".$row["articleBody"]."</p>
        <a href='".$row["source"]."' class='readmore' onclick='return readmorenews();' target='_blank'>
        Read more</a>";
        if(mysqli_num_rows($result2) > 0){
          while($statement = mysqli_fetch_assoc($result2)){
            if($statement["bookmark"] == 'Y'){
              echo "<button id='switch' class='switchon' onclick='bookmarknews()'>
              Bookmark</button>";
            }
            else{
              echo"<button id='switch' class='switchoff' onclick='bookmarknews()'>
              Bookmark</button>";
            }
          }
        } else{
            echo"<button id='switch' class='switchoff' onclick='bookmarknews()'>
            Bookmark</button>";
        }
        echo "</article></section></div>";
    }
} else {
    echo "0 results";
}

mysqli_close($conn);
?>
