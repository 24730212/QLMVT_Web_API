from django.db import models


class LienKet(models.Model):
    ma_lk = models.AutoField(db_column="MaLK", primary_key=True)
    matb_goc = models.ForeignKey(
        "ThietBi", models.DO_NOTHING, db_column="MaTB_Goc", blank=True, null=True
    )
    matb_dich = models.ForeignKey(
        "ThietBi",
        models.DO_NOTHING,
        db_column="MaTB_Dich",
        related_name="lienket_matb_dich_set",
        blank=True,
        null=True,
    )
    bang_thong_toi_da = models.FloatField(
        db_column="BangThongToiDa", blank=True, null=True
    )
    manv_tao = models.ForeignKey(
        "NhanVien", models.DO_NOTHING, db_column="MaNV_Tao", blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "LienKet"
