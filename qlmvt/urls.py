from django.urls import path
from .view import nhanvien
from .view import thietbi
from .view import hieusuat
from .view import lohong
from .view import lienket
from .view import nhatkyloi

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
    # Hiệu suất
    path("api_get_ds_hs/", hieusuat.api_get_ds_hs, name="api_get_ds_hs"),
    path("api_get_hs/<str:ma_hs>/", hieusuat.api_get_hs, name="api_get_hs"),
    # Lỗ hổng
    path("api_get_ds_lh/", lohong.api_get_ds_lh, name="api_get_ds_lh"),
    path("api_get_lh/<str:ma_lh>/", lohong.api_get_lh, name="api_get_lh"),
    path("api_create_lh/", lohong.api_create_lh, name="api_create_lh"),
    # Liên kết
    path("api_get_ds_lk/", lienket.api_get_ds_lk, name="api_get_ds_lk"),
    path("api_get_lk/<str:ma_lk>/", lienket.api_get_lk, name="api_get_lk"),
    path("api_create_lk/", lienket.api_create_lk, name="api_create_lk"),
    # Nhật ký lỗi
    path("api_get_ds_nkl/", nhatkyloi.api_get_ds_nkl, name="api_get_ds_nkl"),
    path("api_get_nkl/<str:ma_nkl>/", nhatkyloi.api_get_nkl, name="api_get_nkl"),
    path("api_create_nkl/", nhatkyloi.api_create_nkl, name="api_create_nkl"),
    # Báo cáo
]
