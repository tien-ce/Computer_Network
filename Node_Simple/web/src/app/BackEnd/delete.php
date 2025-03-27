<?php 
error_reporting(E_ALL);
ini_set('display_errors', 1);

if (isset($_GET['file'])) {
    $file = $_GET['file'];
    $baseDir = realpath(dirname(__FILE__) . '/../../../../file_server');
    $fullPath = realpath($file);

    if ($fullPath && strpos($fullPath, $baseDir) === 0) {
        if (unlink($fullPath)) {
            echo json_encode(['status' => 'success', 'message' => 'File deleted successfully.']);
        } else {
            echo json_encode(['status' => 'error', 'message' => 'Failed to delete file.']);
        }
    } else {
        echo json_encode(['status' => 'error', 'message' => 'Invalid file path.']);
    }
} else {
    echo json_encode(['status' => 'error', 'message' => 'No file specified.']);
}
?>