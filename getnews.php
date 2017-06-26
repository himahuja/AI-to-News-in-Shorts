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

/////////// GETTING PARAMETERS ////////////

$_dir = $_GET["dir"];
$_iid = $_GET["iid"];
$_t   = $_GET["t"];
////////////STORING THE TIME OF THE CURRENT Article/////////////////
$update = "INSERT INTO stats (iid, bookmark, readmore, counter)
           VALUES ('$_iid', NULL, NULL, '$_t')
           ON DUPLICATE KEY UPDATE
           counter = counter + $_t";

mysqli_query($conn, $update);
////////////// SETTING MOTION /////////////
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
  $_iid = 45768;
}

else if($_dir == 1 && $_iid == 45768){
  $_iid = 0;
}
else{
  $_iid = $_iid + $_dir;
}

////////// QUERYING THE DATASET ///////////

$sql = "SELECT iid, headline, articleBody, author FROM articles WHERE iid = '$_iid'";
$result = mysqli_query($conn, $sql);

//////////////////////////////////////////////////////////////////////
if (mysqli_num_rows($result) > 0) {
    // output data of each row
    while($row = mysqli_fetch_assoc($result)){
        echo "<div id='container'><section><article id = 'news-card'>
        <div id = 'identity' >".$row["iid"]."</div>
        <h1>". $row["headline"]."</h1>
        <p>".$row["author"]."</p>
        <p>".$row["articleBody"]."</p>
        <a href='#' class='readmore'>Read more</a>
        <form action = 'getnews.php' method = 'post'>
        <input type = 'checkbox' name = 'bookmark'>Bookmark?</input>
        </form>
        </article></section></div>";
    }
} else {
    echo "0 results";
}
mysqli_close($conn);
?>
