# QLMVT Web API

API Django REST Framework quản lý mạng viễn thông: nhân viên, thiết bị, liên
kết, nhật ký lỗi, lỗ hổng và chỉ số hiệu suất. Dữ liệu nghiệp vụ nằm trong
**Microsoft SQL Server**; file `db.sqlite3` trong repository không được
project sử dụng.

## Yêu cầu

- Python 3.12+ (khuyến nghị tạo virtual environment bằng Python 3.12 hoặc
  3.13).
- SQL Server có database `QuanLyMangVienThong`.
- ODBC Driver 18 for SQL Server.
- Windows: SQL Server/SSMS hoặc `sqlcmd`.
- macOS: Docker Desktop và container SQL Server (SQL Server không chạy native
  trên macOS).

## Cài đặt lần đầu

### 1. Clone và tạo môi trường Python

```bash
git clone <URL_REPOSITORY>
cd QLMVT_Web_API
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Windows PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Nếu PowerShell chặn activate, chạy một lần bằng PowerShell với quyền phù hợp:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### 2. Tạo database SQL Server

Tên database mặc định của project là `QuanLyMangVienThong`. File
[`MSSQL/SQL_total_local.sql`](MSSQL/SQL_total_local.sql) tạo database, bảng,
khóa, function, procedure, trigger và role. Chạy file này **một lần trên
database mới** bằng SSMS (mở file rồi bấm **Execute**) hoặc `sqlcmd`.

Windows PowerShell:

```powershell
sqlcmd -S localhost,1433 -U sa -P "<SA_PASSWORD>" -C `
  -i .\MSSQL\SQL_total_local.sql
```

macOS khi SQL Server chạy trong Docker:

```bash
docker cp MSSQL/SQL_total_local.sql sqlserver-mssql:/tmp/SQL_total_local.sql
docker exec sqlserver-mssql /opt/mssql-tools18/bin/sqlcmd \
  -S localhost -U sa -P '<SA_PASSWORD>' -C \
  -i /tmp/SQL_total_local.sql
```

Script hiện đặt `COMPATIBILITY_LEVEL = 170`. Nếu SQL Server của bạn không hỗ
trợ compatibility level 170, xóa hoặc comment hai dòng
`ALTER DATABASE ... SET COMPATIBILITY_LEVEL = 170` trước khi chạy; không xóa
các phần tạo bảng và object còn lại.

> Script tổng đã bao gồm các object SQL chính. Thư mục
> [`MSSQL/SQL_thuc_thi`](MSSQL/SQL_thuc_thi) chứa từng function/procedure/
> trigger/role riêng để chạy lại từng object khi cần. Không chạy lại script
> tạo database trên database đã tồn tại nếu chưa kiểm tra các lệnh `CREATE`.

### 3. Cấu hình biến môi trường

Tạo `.env` từ file mẫu:

```bash
cp .env.example .env
```

Trên Windows nếu `cp` không có, dùng:

```powershell
Copy-Item .env.example .env
```

Mở `.env` và đặt đúng thông tin SQL Server:

```dotenv
SECRET_KEY=change-me
DEBUG=True
DB_NAME=QuanLyMangVienThong
DB_USER=sa
DB_PASSWORD=<SA_PASSWORD>
DB_HOST=127.0.0.1
DB_PORT=1433
```

Không commit `.env`. Với Docker, `DB_HOST` vẫn là `127.0.0.1` vì Django chạy
trên máy host và cổng SQL Server được publish ra `1433`.

### 4. Tạo bảng quản trị Django

Các model nghiệp vụ có `managed = False`, nên Django không tạo/sửa các bảng
nghiệp vụ. Lệnh `migrate` chỉ tạo các bảng hệ thống Django (admin, session,
auth, token):

```bash
python manage.py migrate
python manage.py createsuperuser
```

Lệnh `createsuperuser` là tùy chọn, chỉ cần nếu dùng `/admin/`.

### 5. Kiểm tra và chạy API

```bash
python manage.py check
python manage.py runserver
```

Mở `http://127.0.0.1:8000/admin/` hoặc gọi API tại
`http://127.0.0.1:8000/qlmvt/`. Dừng server bằng `Ctrl+C`.

## SQL Server bằng Docker trên macOS

Nếu chưa có container:

```bash
docker run --name sqlserver-mssql \
  -e ACCEPT_EULA=Y \
  -e MSSQL_PID=Developer \
  -e MSSQL_SA_PASSWORD='<SA_PASSWORD>' \
  -p 1433:1433 -d mcr.microsoft.com/mssql/server:2022-latest
```

Chờ container sẵn sàng trước khi chạy file SQL:

```bash
docker logs -f sqlserver-mssql
```

Khi log báo SQL Server đã sẵn sàng, nhấn `Ctrl+C`, sau đó thực hiện bước tạo
database ở trên. Lần sau chỉ cần:

```bash
docker start sqlserver-mssql
```

Mật khẩu SA phải có tối thiểu 8 ký tự và gồm chữ hoa, chữ thường, số và ký tự
đặc biệt. Dùng cùng mật khẩu đó trong `.env`.

## Backup và restore database

Nên backup trước khi chạy các script thay đổi schema hoặc dữ liệu.

### Backup bằng SSMS/sqlcmd trên Windows

Trong SSMS, chọn database `QuanLyMangVienThong` → **Tasks** → **Back Up...** →
chọn file `.bak` → **OK**. Hoặc dùng:

```powershell
sqlcmd -S localhost,1433 -U sa -P "<SA_PASSWORD>" -C -Q `
  "BACKUP DATABASE [QuanLyMangVienThong] TO DISK = N'C:\backup\QuanLyMangVienThong.bak' WITH INIT, FORMAT"
```

Restore bằng SSMS: chuột phải **Databases** → **Restore Database...** →
**Device** → chọn file `.bak` → chọn **Overwrite the existing database** nếu
đúng mục tiêu → **OK**. Có thể kiểm tra file backup bằng:

```powershell
sqlcmd -S localhost,1433 -U sa -P "<SA_PASSWORD>" -C -Q `
  "RESTORE VERIFYONLY FROM DISK = N'C:\backup\QuanLyMangVienThong.bak'"
```

### Backup/restore với Docker trên macOS

Backup vào container rồi copy ra máy:

```bash
docker exec sqlserver-mssql mkdir -p /var/opt/mssql/backup
docker exec sqlserver-mssql /opt/mssql-tools18/bin/sqlcmd \
  -S localhost -U sa -P '<SA_PASSWORD>' -C \
  -Q "BACKUP DATABASE [QuanLyMangVienThong] TO DISK = N'/var/opt/mssql/backup/QuanLyMangVienThong.bak' WITH INIT, FORMAT"
docker cp sqlserver-mssql:/var/opt/mssql/backup/QuanLyMangVienThong.bak .
```

Copy file backup vào container:

```bash
docker cp QuanLyMangVienThong.bak sqlserver-mssql:/var/opt/mssql/backup/
```

Xem tên logical file trước khi restore:

```bash
docker exec sqlserver-mssql /opt/mssql-tools18/bin/sqlcmd \
  -S localhost -U sa -P '<SA_PASSWORD>' -C \
  -Q "RESTORE FILELISTONLY FROM DISK = N'/var/opt/mssql/backup/QuanLyMangVienThong.bak'"
```

Sau đó restore bằng SSMS hoặc chạy `RESTORE DATABASE ... WITH MOVE ...` với
đúng `LogicalName` và đường dẫn `/var/opt/mssql/data/*.mdf`, `*.ldf` trả về từ
lệnh trên. Không restore đè database đang có kết nối; đóng API trước và dùng
`WITH REPLACE` chỉ khi chắc chắn file backup là bản cần phục hồi.

## API

Base URL: `http://127.0.0.1:8000/qlmvt`. Các API nhận/trả JSON. ID trong
`<...>` là giá trị thật. API tạo/cập nhật dùng `Content-Type: application/json`;
API tạo cho phép một object hoặc một mảng object. Các field JSON dùng tên
snake_case theo serializer (ví dụ `ho_ten`, `ma_tb`).

### USER: nhân viên

| Method | Endpoint | Mô tả |
|---|---|---|
| GET | `/qlmvt/api_get_ds_nv/` | Danh sách nhân viên |
| GET | `/qlmvt/api_get_nv/<ma_nv>/` | Một nhân viên |
| POST | `/qlmvt/api_create_nv/` | Tạo một/nhiều nhân viên |
| PUT | `/qlmvt/api_update_nv/<ma_nv>/` | Cập nhật nhân viên |
| DELETE | `/qlmvt/api_delete_nv/<ma_nv>/` | Xóa nhân viên |

Field nhân viên: `ho_ten`, `email`, `so_dien_thoai`, `vai_tro`,
`chuyen_mon`. `ma_nv` tự tăng.

### DEVICE: thiết bị

| Method | Endpoint | Mô tả |
|---|---|---|
| GET | `/qlmvt/api_get_ds_tb/` | Danh sách thiết bị |
| GET | `/qlmvt/api_get_tb/<ma_tb>/` | Một thiết bị |
| POST | `/qlmvt/api_create_tb/` | Tạo một/nhiều thiết bị |
| PUT | `/qlmvt/api_update_tb/<ma_tb>/` | Cập nhật thiết bị |
| DELETE | `/qlmvt/api_delete_tb/<ma_tb>/` | Xóa thiết bị |
| GET | `/qlmvt/api_get_tb_theo_loai_tb?loai_tb=router` | Lọc theo loại; bỏ query để lấy tất cả |

Field thiết bị: `ten_tb`, `loai_tb`, `dia_chi_ip`, `vi_tri`, `trang_thai`,
`tinh_trang`. `ma_tb` tự tăng; `dia_chi_ip` là duy nhất.

### PERFORMANCE: chỉ số hiệu suất

| Method | Endpoint | Mô tả |
|---|---|---|
| GET | `/qlmvt/api_get_ds_cshs/` | Danh sách chỉ số |
| GET | `/qlmvt/api_get_cshs/<ma_cs>/` | Một chỉ số |

Field: `ma_tb`, `thoi_gian_ghi_nhan`, `do_tre`, `mat_goi`,
`bang_thong_su_dung`.

### VULNERABILITY: lỗ hổng

| Method | Endpoint | Mô tả |
|---|---|---|
| GET | `/qlmvt/api_get_ds_lh/` | Danh sách lỗ hổng |
| GET | `/qlmvt/api_get_lh/<ma_lh>/` | Một lỗ hổng |
| POST | `/qlmvt/api_create_lh/` | Tạo một/nhiều lỗ hổng |
| PUT | `/qlmvt/api_update_lh/<ma_lh>/` | Cập nhật lỗ hổng |
| DELETE | `/qlmvt/api_delete_lh/<ma_lh>/` | Xóa lỗ hổng |
| GET | `/qlmvt/api_get_lh_theo_trangthai?trang_thai=fixed` | Lọc `fixed`, `unfixed`, `processing`; bỏ query để lấy tất cả |

Field: `ma_tb`, `ten_lo_hong`, `muc_do`, `trang_thai_khac_phuc`,
`thoi_gian_xay_ra_su_co`, `thoi_gian_xu_ly_su_co`, `manv_xuly`.

### LINK: liên kết

| Method | Endpoint | Mô tả |
|---|---|---|
| GET | `/qlmvt/api_get_ds_lk/` | Danh sách liên kết |
| GET | `/qlmvt/api_get_lk/<ma_lk>/` | Một liên kết |
| POST | `/qlmvt/api_create_lk/` | Tạo một/nhiều liên kết |
| PUT | `/qlmvt/api_update_lk/<ma_lk>/` | Cập nhật liên kết |
| DELETE | `/qlmvt/api_delete_lk/<ma_lk>/` | Xóa liên kết |

Field: `matb_goc`, `matb_dich`, `bang_thong_toi_da`, `manv_tao`.

### ERROR LOG: nhật ký lỗi

| Method | Endpoint | Mô tả |
|---|---|---|
| GET | `/qlmvt/api_get_ds_nkl/` | Danh sách nhật ký lỗi |
| GET | `/qlmvt/api_get_nkl/<ma_loi>/` | Một nhật ký lỗi |
| POST | `/qlmvt/api_create_nkl/` | Tạo một/nhiều nhật ký lỗi |
| PUT | `/qlmvt/api_update_nkl/<ma_loi>/` | Cập nhật nhật ký lỗi |
| DELETE | `/qlmvt/api_delete_nkl/<ma_loi>/` | Xóa nhật ký lỗi |
| GET | `/qlmvt/api_get_nkl_theo_xuly?da_xu_ly=true` | Lọc `true` hoặc `false`; bỏ query để lấy tất cả |
| PUT | `/qlmvt/api_phan_cong_nv_xuly_loi/<ma_loi>/` | Phân công nhân viên xử lý |

Field: `ma_tb`, `thoi_gian_loi`, `mo_ta_loi`, `muc_do_nghiem_trong`,
`manv_xuly`, `da_xu_ly`, `thoi_gian_hoan_thanh`.

### REPORT: báo cáo

Các URL báo cáo trong source không có dấu `/` cuối; hãy gọi đúng như dưới đây
để tránh redirect ngoài ý muốn:

| Method | Endpoint | Mô tả |
|---|---|---|
| GET | `/qlmvt/api_get_bao_cao_tong_quan` | Tổng số liệu toàn hệ thống |
| GET | `/qlmvt/api_get_tong_loi_nv_xu_ly` | Tổng lỗi theo nhân viên |
| GET | `/qlmvt/api_get_kpi_nhan_vien` | KPI nhân viên (cần function SQL) |
| GET | `/qlmvt/api_get_tinh_trang_lo_hong` | Số lỗ hổng theo trạng thái |
| GET | `/qlmvt/api_get_lo_hong_theo_thiet_bi` | Lỗ hổng theo thiết bị (cần procedure SQL) |

## Ví dụ gọi API

```bash
curl http://127.0.0.1:8000/qlmvt/api_get_ds_tb/
curl "http://127.0.0.1:8000/qlmvt/api_get_lh_theo_trangthai?trang_thai=fixed"
curl -X POST http://127.0.0.1:8000/qlmvt/api_create_nv/ \
  -H "Content-Type: application/json" \
  -d '{"ho_ten":"Nguyen Van A","email":"a@example.com","vai_tro":"Ky thuat"}'
```

## Lỗi thường gặp

- **Login timeout / ODBC Driver not found**: cài ODBC Driver 18, kiểm tra SQL
  Server đang chạy và `.env` có đúng host, port, user, password.
- **Database does not exist**: chạy `MSSQL/SQL_total_local.sql` trước
  `migrate`.
- **Invalid object name**: database chưa được khởi tạo đủ schema hoặc đang trỏ
  nhầm database.
- **Port 1433 already in use**: đổi port publish của Docker (ví dụ
  `-p 1434:1433`) và đặt `DB_PORT=1434`.
- **Không thấy dữ liệu**: script tạo schema không tự sinh dữ liệu nghiệp vụ;
  dùng POST API hoặc nạp dữ liệu backup.

## API backup/restore và import/export dữ liệu

Các API này thao tác trên **toàn bộ 6 bảng nghiệp vụ**: `NhanVien`,
`ThietBi`, `LienKet`, `ChiSoHieuSuat`, `LoHong` và `NhatKyLoi`. Đây là
backup/restore dữ liệu dạng JSON của ứng dụng, không phải file backup vật lý
`.bak` của SQL Server.

### Quyền truy cập

Chỉ Django staff/superuser mới được gọi hai API này (`IsAdminUser`). Trước tiên
hãy tạo tài khoản quản trị:

```bash
python manage.py createsuperuser
```

Khi gọi API, đăng nhập bằng session Django hoặc cơ chế authentication đang
được cấu hình cho project. Nếu dùng trình duyệt, có thể đăng nhập tại
`http://127.0.0.1:8000/admin/` trước rồi gọi API trong cùng session.

### Export/backup JSON

```text
GET /qlmvt/api_backup_database/
```

API trả về file tải xuống có tên dạng
`qlmvt-backup-YYYYMMDDTHHMMSSZ.json`. File có cấu trúc:

```json
{
  "format": "qlmvt-json-backup",
  "version": 1,
  "models": {
    "nhanvien": [],
    "thietbi": [],
    "lienket": [],
    "hieusuat": [],
    "lohong": [],
    "nhatkyloi": []
  }
}
```

Ví dụ export bằng `curl` sau khi đã có cookie session:

```bash
curl -b cookies.txt -c cookies.txt \
  -o qlmvt-backup.json \
  http://127.0.0.1:8000/qlmvt/api_backup_database/
```

### Import/restore JSON

```text
POST /qlmvt/api_restore_database/
```

Có thể gửi file bằng multipart với field `backup_file` (hoặc `file`):

```bash
curl -b cookies.txt \
  -F "backup_file=@qlmvt-backup.json" \
  http://127.0.0.1:8000/qlmvt/api_restore_database/
```

Hoặc gửi trực tiếp nội dung JSON trong request body:

```bash
curl -b cookies.txt \
  -H "Content-Type: application/json" \
  --data-binary @qlmvt-backup.json \
  http://127.0.0.1:8000/qlmvt/api_restore_database/
```

Windows PowerShell dùng cú pháp tương tự:

```powershell
curl.exe -b cookies.txt `
  -F "backup_file=@qlmvt-backup.json" `
  http://127.0.0.1:8000/qlmvt/api_restore_database/
```

Khi restore, hệ thống kiểm tra `format`, `version`, tên model và field trước
khi ghi dữ liệu. Các bản ghi được cập nhật theo khóa chính hoặc tạo mới nếu
chưa tồn tại; **các bản ghi đang có nhưng không nằm trong file backup không bị
xóa**. Thứ tự khôi phục được xử lý để không vi phạm khóa ngoại. Thành công
trả về số bản ghi đã xử lý theo từng model:

```json
{
  "message": "Khôi phục dữ liệu thành công.",
  "restored": {
    "nhanvien": 10,
    "thietbi": 20,
    "lienket": 12,
    "hieusuat": 100,
    "lohong": 15,
    "nhatkyloi": 30
  }
}
```

Nên tạo một file export mới trước khi import/restore. Không sửa thủ công
`format`, `version`, tên model hoặc tên field trong file; payload không hợp lệ
sẽ trả về lỗi `400`. Nếu restore lỗi giữa chừng, transaction sẽ rollback.
