from rest_framework import serializers
from .model.nhanvien import NhanVien
from .model.thietbi import ThietBi
from .model.nhatkyloi import NhatKyLoi
from .model.lienket import LienKet
from .model.lohong import LoHong
from .model.chisohieusuat import ChiSoHieuSuat


class NhanVienSerializer(serializers.ModelSerializer):
    class Meta:
        model = NhanVien
        fields = "__all__"


class ThietBiSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThietBi
        fields = "__all__"


class NhatKyLoiSerializer(serializers.ModelSerializer):
    class Meta:
        model = NhatKyLoi
        fields = "__all__"


class LienKetSerializer(serializers.ModelSerializer):
    class Meta:
        model = LienKet
        fields = "__all__"


class LoHongSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoHong
        fields = "__all__"


class ChiSoHieuSuatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChiSoHieuSuat
        fields = "__all__"
