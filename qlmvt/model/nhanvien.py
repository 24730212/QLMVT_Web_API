from django.db import models


class NhanVien(models.Model):
    ma_nv = models.AutoField(db_column="MaNV", primary_key=True)
    ho_ten = models.CharField(
        db_column="HoTen",
        max_length=100,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    email = models.CharField(
        db_column="Email",
        unique=True,
        max_length=100,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    so_dien_thoai = models.CharField(
        db_column="SoDienThoai",
        max_length=15,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    vai_tro = models.CharField(
        db_column="VaiTro",
        max_length=50,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    chuyen_mon = models.CharField(
        db_column="ChuyenMon",
        max_length=100,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )

    def __str__(self):
        return str([self.ma_nv, self.ho_ten])

    class Meta:
        managed = False
        db_table = "NhanVien"
