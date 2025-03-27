<?php
header('Access-Control-Allow-Origin: *');
header('Content-Type: application/json');
error_reporting(E_ALL);
ini_set('display_errors', 1);

include 'DbConnect.php';
$objDb = new DbConnect();
$conn = $objDb->connect();
$currentPage = $_SERVER['REQUEST_URI'];

$variable = isset($_GET['variable']) ? $_GET['variable'] : null;
$url = isset($_GET['url']) ? $_GET['url'] : null;
$status = isset($_GET['status']) ? $_GET['status'] : null;

if ($variable !== null) {
    $sql = "UPDATE $url SET $url WHERE Status = :status";
    $stmt = $conn->prepare($sql);
    $stmt->bindParam(':status', $variable, PDO::PARAM_STR); 
    $stmt->execute();
    $users = $stmt->fetchAll(PDO::FETCH_ASSOC);
} else {
    $users = [];
}

$conn = null;
if ($users) {
    echo json_encode($users);
} else {
    echo json_encode(['message' => 'No records found']);
}
?>
