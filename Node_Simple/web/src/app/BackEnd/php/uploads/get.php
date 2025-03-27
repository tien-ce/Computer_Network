<?php
header('Access-Control-Allow-Origin: *');
header('Content-Type: application/json');
error_reporting(E_ALL);
ini_set('display_errors', 1);

include 'DbConnect.php';
$objDb = new DbConnect();
$conn = $objDb->connect();

$url = isset($_GET['url']) ? $_GET['url'] : null;
$variable = isset($_GET['variable']) ? $_GET['variable'] : null;

echo $url;

if ($url) {
    if ($variable === null) {
        $sql = "SELECT * FROM $url";
        $stmt = $conn->prepare($sql);
        $stmt->execute();
        $users = $stmt->fetchAll(PDO::FETCH_ASSOC);
    } else {
        $sql = "SELECT * FROM $url WHERE id = :id";
        $stmt = $conn->prepare($sql);
        $stmt->bindParam(':id', $variable, PDO::PARAM_STR); 
        $stmt->execute();
        $users = $stmt->fetchAll(PDO::FETCH_ASSOC);
    }
    
    if ($users) {
        echo json_encode($users);
    } else {
        echo json_encode(['message' => 'No records found']);
    }
} else {
    echo json_encode(['message' => 'URL parameter is missing.']);
}

$conn = null;
?>
