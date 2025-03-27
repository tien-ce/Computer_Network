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
$gia = intval($gia_goc - ($gia_goc * $giam_gia) / 100);
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

$sql = "INSERT INTO tat_ca_san_pham (id, name, gia_goc, gia, giam_gia, tap, tac_gia, doi_tuong, khuon_kho, so_trang, trong_luong, Page, Status) 
        VALUES ('$id', '$name', '$gia_goc', '$gia', '$giam_gia', '$tap', '$tac_gia', '$doi_tuong', '$khuon_kho', '$so_trang', '$trong_luong', 'tat_ca_san_pham', 'Active')";

$response = [];
if ($conn->query($sql) === TRUE) {
    $response["success"] = true;
    $response["message"] = "Dữ liệu đã được thêm thành công.";
} else {
    $response["success"] = false;
    $response["message"] = "Lỗi khi thêm dữ liệu: " . $conn->error;
    echo json_encode($response);
    $conn->close();
    exit;
}

foreach ($tables as $table) {
    if (isset($_POST[$table])) {
        $sql = "INSERT INTO " . strtolower($table) . "(id, name, gia_goc, gia, giam_gia, tap, tac_gia, doi_tuong, khuon_kho, so_trang, trong_luong, Page, Status)
                VALUES ('$id', '$name', '$gia_goc', '$gia', '$giam_gia', '$tap', '$tac_gia', '$doi_tuong', '$khuon_kho', '$so_trang', '$trong_luong', '$table', 'Active')";

        if ($conn->query($sql) !== TRUE) {
            $response["success"] = false;
            $response["message"] = "Lỗi khi thêm vào bảng $table: " . $conn->error;
            echo json_encode($response);
            $conn->close();
            exit;
        }
    }
}

$upload_dirs = [
    'kien_thuc_khoa_hoc' => './images/kien_thuc_khoa_hoc/' . $id . '/',
    'lich_su_truyen_thong' => './images/lich_su_truyen_thong/' . $id . '/',
    'tat_ca_san_pham' => './images/tat_ca_san_pham/' . $id . '/',
    'truyen_tranh' => './images/truyen_tranh/' . $id . '/',
    'van_hoc_nuoc_ngoai' => './images/van_hoc_nuoc_ngoai/' . $id . '/',
    'van_hoc_viet_nam' => './images/van_hoc_viet_nam/' . $id . '/',
    'wings_book' => './images/wings_book/' . $id . '/'
];

$countName = 0;

if (isset($_FILES['file'])) {
    $test = 1;
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

$response["message"] = "Tất cả dữ liệu đã được xử lý thành công.";
echo json_encode($response);
$conn->close();
?>