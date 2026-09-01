from django.db import models


class LoHong(models.Model):
    ma_lh = models.AutoField(db_column="MaLH", primary_key=True)
    ma_tb = models.ForeignKey(
        "ThietBi", models.DO_NOTHING, db_column="MaTB", blank=True, null=True
    )
    ten_lo_hong = models.CharField(
        db_column="TenLoHong",
        max_length=200,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    muc_do = models.CharField(
        db_column="MucDo",
        max_length=20,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    trang_thai_khac_phuc = models.CharField(
        db_column="TrangThaiKhacPhuc",
        max_length=20,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    thoi_gian_xay_ra_su_co = models.DateTimeField(
        db_column="ThoiGianXayRaSuCo", blank=True, null=True
    )
    thoi_gian_xu_ly_su_co = models.DateTimeField(
        db_column="ThoiGianXuLySuCo", blank=True, null=True
    )
    manv_xuly = models.ForeignKey(
        "NhanVien", models.DO_NOTHING, db_column="MaNV_XuLy", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "LoHong"
