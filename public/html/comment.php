<?php
require_once "database.php";

$name = $_POST["name"];
$email = $_POST["email"];
$organization = $_POST["organization"];
$role = $_POST["role"];
$subject = $_POST["subject"];
$problem = $_POST["problem"];
$sql= "INSERT INTO contacts(name, email, organization, role, subject, problem) VALUES ('" . $name . "', '" . $email . "', '" .  $organization . "',  '" .  $role . "', '" .  $subject . "', ' '" .  $problem . "')";
header("Location:homepage.php");
$conn->query($sql);
$conn->close();


?>
