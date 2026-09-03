from django.urls import path
from .view import nhanvien
from .view import thietbi
from .view import hieusuat
from .view import lohong
from .view import lienket
from .view import nhatkyloi
from .view import baocao

urlpatterns = [
    # Auth
    # Nhân viên
    path("api_get_ds_nv/", nhanvien.api_get_ds_nv, name="api_get_ds_nv"),
    path("api_get_nv/<str:ma_nv>/", nhanvien.api_get_nv, name="api_get_nv"),
    path("api_create_nv/", nhanvien.api_create_nv, name="api_create_nv"),
    path("api_update_nv/<str:ma_nv>/", nhanvien.api_update_nv, name="api_update_nv"),
    path("api_delete_nv/<str:ma_nv>/", nhanvien.api_delete_nv, name="api_delete_nv"),
    # Thiết bị
    path("api_get_ds_tb/", thietbi.api_get_ds_tb, name="api_get_ds_tb"),
    path("api_get_tb/<str:ma_tb>/", thietbi.api_get_tb, name="api_get_tb"),
    path("api_create_tb/", thietbi.api_create_tb, name="api_create_tb"),
    path("api_update_tb/<str:ma_tb>/", thietbi.api_update_tb, name="api_update_tb"),
    path("api_delete_tb/<str:ma_tb>/", thietbi.api_delete_tb, name="api_delete_tb"),
    path(
        "api_get_tb_theo_loai_tb",
        thietbi.api_get_tb_theo_loai_tb,
        name="api_get_tb_theo_loai_tb",
    ),
    # Hiệu suất
    path("api_get_ds_cshs/", hieusuat.api_get_ds_cshs, name="api_get_ds_cshs"),
    path("api_get_cshs/<str:ma_cs>/", hieusuat.api_get_cshs, name="api_get_cshs"),
    # Lỗ hổng
    path("api_get_ds_lh/", lohong.api_get_ds_lh, name="api_get_ds_lh"),
    path("api_get_lh/<str:ma_lh>/", lohong.api_get_lh, name="api_get_lh"),
    path("api_create_lh/", lohong.api_create_lh, name="api_create_lh"),
    path("api_update_lh/<str:ma_lh>/", lohong.api_update_lh, name="api_update_lh"),
    path("api_delete_lh/<str:ma_lh>/", lohong.api_delete_lh, name="api_delete_lh"),
    path(
        "api_get_lh_theo_trangthai",
        lohong.api_get_lh_theo_trangthai,
        name="api_get_lh_theo_trangthai",
    ),
    # Liên kết
    path("api_get_ds_lk/", lienket.api_get_ds_lk, name="api_get_ds_lk"),
    path("api_get_lk/<str:ma_lk>/", lienket.api_get_lk, name="api_get_lk"),
    path("api_create_lk/", lienket.api_create_lk, name="api_create_lk"),
    path("api_update_lk/<str:ma_lk>/", lienket.api_update_lk, name="api_update_lk"),
    path("api_delete_lk/<str:ma_lk>/", lienket.api_delete_lk, name="api_delete_lk"),
    # Nhật ký lỗi
    path("api_get_ds_nkl/", nhatkyloi.api_get_ds_nkl, name="api_get_ds_nkl"),
    path("api_get_nkl/<str:ma_loi>/", nhatkyloi.api_get_nkl, name="api_get_nkl"),
    path("api_create_nkl/", nhatkyloi.api_create_nkl, name="api_create_nkl"),
    path(
        "api_update_nkl/<str:ma_loi>/", nhatkyloi.api_update_nkl, name="api_update_nkl"
    ),
    path(
        "api_delete_nkl/<str:ma_loi>/", nhatkyloi.api_delete_nkl, name="api_delete_nkl"
    ),
    path(
        "api_get_nkl_theo_xuly",
        nhatkyloi.api_get_nkl_theo_xuly,
        name="api_get_nkl_theo_xuly",
    ),
    path(
        "api_phan_cong_nv_xuly_loi/<str:ma_loi>/",
        nhatkyloi.api_phan_cong_nv_xuly_loi,
        name="api_phan_cong_nv_xuly_loi",
    ),
    # Báo cáo
    path(
        "api_get_bao_cao_tong_quan",
        baocao.api_get_bao_cao_tong_quan,
        name="api_get_bao_cao_tong_quan",
    ),
    path(
        "api_get_tong_loi_nv_xu_ly",
        baocao.api_get_tong_loi_nv_xu_ly,
        name="api_get_tong_loi_nv_xu_ly",
    ),
    path(
        "api_get_kpi_nhan_vien",
        baocao.api_get_kpi_nhan_vien,
        name="api_get_kpi_nhan_vien",
    ),
    path(
        "api_get_tinh_trang_lo_hong",
        baocao.api_get_tinh_trang_lo_hong,
        name="api_get_tinh_trang_lo_hong",
    ),
    # ,
    path(
        "api_get_lo_hong_theo_thiet_bi",
        baocao.api_get_lo_hong_theo_thiet_bi,
        name="api_get_lo_hong_theo_thiet_bi",
    ),
]
