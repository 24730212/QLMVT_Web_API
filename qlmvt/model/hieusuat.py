from django.db import models


class ChiSoHieuSuat(models.Model):
    ma_cs = models.AutoField(db_column="MaCS", primary_key=True)
    ma_tb = models.ForeignKey(
        "ThietBi", models.DO_NOTHING, db_column="MaTB", blank=True, null=True
    )
    thoi_gian_ghi_nhan = models.DateTimeField(
        db_column="ThoiGianGhiNhan", blank=True, null=True
    )
    do_tre = models.FloatField(db_column="DoTre", blank=True, null=True)
    mat_goi = models.FloatField(db_column="MatGoi", blank=True, null=True)
    bang_thong_su_dung = models.FloatField(
        db_column="BangThongSuDung", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "ChiSoHieuSuat"
