from django.contrib import admin

# Register your models here.
from .model.nhanvien import NhanVien
from .model.thietbi import ThietBi
from .model.lienket import LienKet
from .model.chisohieusuat import ChiSoHieuSuat
from .model.lohong import LoHong
from .model.nhatkyloi import NhatKyLoi



admin.site.register(NhanVien)
admin.site.register(ThietBi)
admin.site.register(LienKet)
admin.site.register(ChiSoHieuSuat)
admin.site.register(LoHong)
admin.site.register(NhatKyLoi)
