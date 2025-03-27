<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "tiem_sach";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die(json_encode(["success" => false, "message" => "Kết nối thất bại: " . $conn->connect_error]));
}

header('Access-Control-Allow-Origin: http://localhost:3000');
header('Content-Type: application/json; charset=utf-8');
$conn->set_charset("utf8");

$id = mysqli_real_escape_string($conn, $_POST["id"]);
$name = mysqli_real_escape_string($conn, $_POST["name"]);
$gia_goc = mysqli_real_escape_string($conn, $_POST["gia_goc"]);
$giam_gia = mysqli_real_escape_string($conn, $_POST["giam_gia"]);
$gia = intval($gia_goc * (1 - ($giam_gia / 100)));
$tap = mysqli_real_escape_string($conn, $_POST["tap"]);
$tac_gia = mysqli_real_escape_string($conn, $_POST["tac_gia"]);
$doi_tuong = mysqli_real_escape_string($conn, $_POST["doi_tuong"]);
$khuon_kho = mysqli_real_escape_string($conn, $_POST["khuon_kho"]);
$so_trang = mysqli_real_escape_string($conn, $_POST["so_trang"]);
$trong_luong = mysqli_real_escape_string($conn, $_POST["trong_luong"]);
$status = "Active";

$tables = [
    "Kien_thuc_khoa_hoc",
    "Lich_su_truyen_thong",
    "Truyen_tranh",
    "Van_hoc_nuoc_ngoai",
    "Van_hoc_Viet_Nam",
    "Wings_book",
];

$response = [];

// Update `tat_ca_san_pham` table
$sql = "UPDATE tat_ca_san_pham SET name = ?, gia_goc = ?, gia = ?, giam_gia = ?, tap = ?, tac_gia = ?, doi_tuong = ?, khuon_kho = ?, so_trang = ?, trong_luong = ? WHERE id = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("ssssssssssi", $name, $gia_goc, $gia, $giam_gia, $tap, $tac_gia, $doi_tuong, $khuon_kho, $so_trang, $trong_luong, $id);

if ($stmt->execute()) {
    $response["success"] = true;
    $response["message"] = "Dữ liệu đã được cập nhật thành công.";
} else {
    $response["success"] = false;
    $response["message"] = "Lỗi khi cập nhật dữ liệu: " . $stmt->error;
    echo json_encode($response);
    $conn->close();
    exit;
}
$stmt->close();

foreach ($tables as $table) {
    if (isset($_POST[$table])) {
        $sql = "UPDATE " . strtolower($table) . " SET name = ?, gia_goc = ?, gia = ?, giam_gia = ?, tap = ?, tac_gia = ?, doi_tuong = ?, khuon_kho = ?, so_trang = ?, trong_luong = ? WHERE id = ?";
        $stmt = $conn->prepare($sql);
        $stmt->bind_param("ssssssssssi", $name, $gia_goc, $gia, $giam_gia, $tap, $tac_gia, $doi_tuong, $khuon_kho, $so_trang, $trong_luong, $id);

        if (!$stmt->execute()) {
            $response["success"] = false;
            $response["message"] = "Lỗi khi cập nhật bảng $table: " . $stmt->error;
            echo json_encode($response);
            $conn->close();
            exit;
        }
        $stmt->close();
    }
}

$upload_dirs = [
    'kien_thuc_khoa_hoc' => './images/kien_thuc_khoa_hoc/' . $id . '/',
    'lich_su_truyen_thong' => './images/lich_su_truyen_thong/' . $id . '/',
    'tat_ca_san_pham' => './images/tat_ca_san_pham/' . $id . '/',
    'truyen_tranh' => './images/truyen_tranh/' . $id . '/',
    'van_hoc_nuoc_ngoai' => './images/van_hoc_nuoc_ngoai/' . $id . '/',
    'van_hoc_viet_nam' => './images/van_hoc_viet_nam/' . $id . '/',
    'wings_book' => './images/wings_book/' . $id . '/',
];

function deleteDirectory($dir) {
    if (!is_dir($dir)) {
        return false;
    }

    $files = array_diff(scandir($dir), ['.', '..']);

    foreach ($files as $file) {
        $filePath = "$dir/$file";
        if (is_dir($filePath)) {
            deleteDirectory($filePath);
        } else {
            unlink($filePath);
        }
    }
    return rmdir($dir);
}

foreach ($upload_dirs as $dir) {
    if (is_dir($dir)) {
        deleteDirectory($dir);
    }
}

function getName($name) {
    $path = explode("_", $name); 
    echo $path[count($path) - 1];
    return $path[count($path) - 1]; 
}

$countName = 0;

if (isset($_FILES['file'])) {
    foreach ($_FILES['file']['name'] as $key => $name) {
        $temp_path = $_FILES['file']['tmp_name'][$key];
        $fileInfo = pathinfo($name);
        $filename = $id . '_' . basename($countName++) . '_.' . $fileInfo['extension'];
        if (!file_exists($upload_dirs['tat_ca_san_pham'])) {
            mkdir($upload_dirs['tat_ca_san_pham'], 0777, true);
        }
        $target_path = $upload_dirs['tat_ca_san_pham'] . $filename;
        if (move_uploaded_file($temp_path, $target_path)) {
            foreach ($tables as $table) {
                if (isset($_POST[$table])) {
                    $dir = $upload_dirs[strtolower($table)];
                    if (!file_exists($dir)) {
                        mkdir($dir, 0777, true);
                    }
                    copy($target_path, $dir . $filename);
                }
            }
        } else {
            $response["success"] = false;
            $response["message"] = "Lỗi khi tải lên file: " . $name;
            echo json_encode($response);
            $conn->close();
            exit;
        }
    }
}

echo json_encode($response);
$conn->close();
?>