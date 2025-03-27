<?php
header('Access-Control-Allow-Origin: *');
header('Content-Type: application/json');
error_reporting(E_ALL);
ini_set('display_errors', 1);

include 'DbConnect.php';
$objDb = new DbConnect();
$conn = $objDb->connect();

$id = isset($_GET['id']) ? $_GET['id'] : null;

if ($id === null) {
    echo json_encode(['message' => 'Required parameters are missing.']);
    exit;
}

$tables = [
    "tat_ca_san_pham",
    "kien_thuc_khoa_hoc",
    "lich_su_truyen_thong",
    "truyen_tranh",
    "van_hoc_nuoc_ngoai",
    "van_hoc_Viet_Nam",
    "wings_book",
];

function deleteDirectory($dir) {
    if (!is_dir($dir)) {
        return false;
    }

    $items = scandir($dir);
    foreach ($items as $item) {
        if ($item == '.' || $item == '..') {
            continue;
        }
        $path = $dir . DIRECTORY_SEPARATOR . $item;
        if (is_dir($path)) {
            deleteDirectory($path); 
        } else {
            unlink($path); 
        }
    }
    return rmdir($dir); 
}

$found = false;
$deletedTables = [];

foreach ($tables as $table) {
    $stmt = $conn->prepare("SELECT COUNT(*) FROM $table WHERE id = :id");
    $stmt->bindParam(':id', $id, PDO::PARAM_INT);
    $stmt->execute();
    $count = $stmt->fetchColumn();

    if ($count > 0) {
        $found = true;
        $target = "./../images/$table/$id";

        if (is_dir($target)) {
            deleteDirectory($target);
        }

        $sql = "DELETE FROM $table WHERE id = :id"; 
        $stmt = $conn->prepare($sql);
        $stmt->bindParam(':id', $id, PDO::PARAM_INT);
        
        if ($stmt->execute()) {
            $deletedTables[] = $table; 
        }
    }
}

if ($found) {
    echo json_encode(['message' => 'Record deleted successfully from the following tables: ' . implode(', ', $deletedTables)]);
} else {
    echo json_encode(['message' => 'ID not found in any table.']);
}

$conn = null;
?>