from django.db import models


class ThietBi(models.Model):
    ma_tb = models.AutoField(db_column="MaTB", primary_key=True)
    ten_tb = models.CharField(
        db_column="TenTB",
        max_length=100,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    loai_tb = models.CharField(
        db_column="LoaiTB",
        max_length=50,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    dia_chi_ip = models.CharField(
        db_column="DiaChiIP",
        unique=True,
        max_length=15,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    vi_tri = models.CharField(
        db_column="ViTri",
        max_length=200,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    trang_thai = models.CharField(
        db_column="TrangThai",
        max_length=20,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    tinh_trang = models.CharField(
        db_column="TinhTrang",
        max_length=20,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
    )

    class Meta:
        managed = False
        db_table = "ThietBi"
