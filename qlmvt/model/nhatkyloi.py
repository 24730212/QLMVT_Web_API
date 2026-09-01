from django.db import models
from .nhanvien import NhanVien


class NhatKyLoi(models.Model):
    ma_loi = models.AutoField(db_column="MaLoi", primary_key=True)
    ma_tb = models.ForeignKey(
        "ThietBi", models.DO_NOTHING, db_column="MaTB", blank=True, null=True
    )
    thoi_gian_loi = models.DateTimeField(db_column="ThoiGianLoi", blank=True, null=True)
    mo_ta_loi = models.TextField(
        db_column="MoTaLoi",
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    muc_do_nghiem_trong = models.IntegerField(
        db_column="MucDoNghiemTrong", blank=True, null=True
    )
    manv_xuly = models.ForeignKey(
        NhanVien, models.DO_NOTHING, db_column="MaNV_XuLy", blank=True, null=True
    )
    da_xu_ly = models.BooleanField(db_column="DaXuLy")
    thoi_gian_hoan_thanh = models.DateTimeField(
        db_column="ThoiGianHoanThanh", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "NhatKyLoi"
