<?php
header('Access-Control-Allow-Origin: *');
header('Content-Type: application/json');
error_reporting(E_ALL);
ini_set('display_errors', 1);

include 'DbConnect.php';
$objDb = new DbConnect();
$conn = $objDb->connect();
$currentPage = $_SERVER['REQUEST_URI'];

$url = isset($_GET['url']) ? $_GET['url'] : null;
$variable = isset($_GET['variable']) ? $_GET['variable'] : null;

$sql = "SELECT * FROM $url WHERE id = :id";
$stmt = $conn->prepare($sql);
$stmt->bindParam(':id', $variable, PDO::PARAM_STR); 
$stmt->execute();
$users = $stmt->fetchAll(PDO::FETCH_ASSOC);

$conn = null; 
echo json_encode($users);
?>