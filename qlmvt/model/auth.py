from django.contrib.auth.models import User
from django.db import models

from .nhanvien import NhanVien


class UserAccount(models.Model):
    """
    Liên kết tài khoản Django với nhân viên trong hệ thống.

    Django User:
        - username
        - password
        - is_staff
        - is_active

    NhanVien:
        - ma_nv
        - ho_ten
        - email
        - ...
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="employee_account",
    )

    nhan_vien = models.OneToOneField(
        NhanVien,
        on_delete=models.PROTECT,
        related_name="user_account",
        db_column="MaNV",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "api_useraccount"

    def __str__(self):
        return f"{self.nhan_vien.ma_nv} - {self.user.email}"
