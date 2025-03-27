<?php
header('Access-Control-Allow-Origin: *');
header('Content-Type: application/json');
error_reporting(E_ALL);
ini_set('display_errors', 1);

include 'DbConnect.php';
$objDb = new DbConnect();
$conn = $objDb->connect();
$currentPage = $_SERVER['REQUEST_URI'];

$url = isset($_GET['id']) ? $_GET['id'] : null;
$sl = isset($_GET['sl']) ? $_GET['sl'] : null;

if ($url === null) {
    echo json_encode(['error' => 'ID parameter is missing']);
    exit;
}

$sql = "SELECT * FROM tat_ca_san_pham WHERE id = :id";
$stmt = $conn->prepare($sql);
$stmt->bindParam(':id', $url, PDO::PARAM_STR); 
$stmt->execute();
$users = $stmt->fetchAll(PDO::FETCH_ASSOC);

if (empty($users)) {
    echo json_encode(['error' => 'No product found for the given ID']);
    exit;
}

$product = $users[0];

$checkSql = "SELECT * FROM store WHERE id = :id";
$checkStmt = $conn->prepare($checkSql);
$checkStmt->bindParam(':id', $product['id'], PDO::PARAM_INT);
$checkStmt->execute();
$existingProduct = $checkStmt->fetch(PDO::FETCH_ASSOC);

if ($existingProduct) {
    $updateSql = "UPDATE store SET so_luong = :sl WHERE id = :id";
    $updateStmt = $conn->prepare($updateSql);

    $updateStmt->bindParam(':id', $product['id'], PDO::PARAM_INT);
    $updateStmt->bindParam(':sl', $sl, PDO::PARAM_INT);

    $updateStmt->execute();
} else {
    $insertSql = "INSERT INTO store (id, name, gia_goc, gia, giam_gia, tap, tac_gia, doi_tuong, khuon_kho, so_trang, trong_luong, Page, Status, so_luong) 
                   VALUES (:id, :name, :gia_goc, :gia, :giam_gia, :tap, :tac_gia, :doi_tuong, :khuon_kho, :so_trang, :trong_luong, 'tat_ca_san_pham', 'Active', :sl)";

    $insertStmt = $conn->prepare($insertSql);

    $insertStmt->bindParam(':id', $product['id'], PDO::PARAM_INT);
    $insertStmt->bindParam(':name', $product['name'], PDO::PARAM_STR);
    $insertStmt->bindParam(':gia_goc', $product['gia_goc'], PDO::PARAM_STR);
    $insertStmt->bindParam(':gia', $product['gia'], PDO::PARAM_STR);
    $insertStmt->bindParam(':giam_gia', $product['giam_gia'], PDO::PARAM_STR);
    $insertStmt->bindParam(':tap', $product['tap'], PDO::PARAM_STR);
    $insertStmt->bindParam(':tac_gia', $product['tac_gia'], PDO::PARAM_STR);
    $insertStmt->bindParam(':doi_tuong', $product['doi_tuong'], PDO::PARAM_STR);
    $insertStmt->bindParam(':khuon_kho', $product['khuon_kho'], PDO::PARAM_STR);
    $insertStmt->bindParam(':so_trang', $product['so_trang'], PDO::PARAM_STR);
    $insertStmt->bindParam(':trong_luong', $product['trong_luong'], PDO::PARAM_STR);
    $insertStmt->bindParam(':sl', $sl, PDO::PARAM_STR);

    $insertStmt->execute();
}

$conn = null; 

echo json_encode($users); 
?>