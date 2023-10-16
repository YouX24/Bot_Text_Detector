<?php
$DB_HOST="localhost";
$DB_USER="root";
$DB_PASSWORD="";
$DB_NAME="botmysql";
$conn=new mysqli($DB_HOST,$DB_USER,$DB_PASSWORD,$DB_NAME);
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
else{
    echo "Connected successfully";
}
?>