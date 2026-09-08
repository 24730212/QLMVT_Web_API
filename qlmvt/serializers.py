from rest_framework import serializers
from .model.nhanvien import NhanVien
from .model.thietbi import ThietBi
from .model.nhatkyloi import NhatKyLoi
from .model.lienket import LienKet
from .model.lohong import LoHong
from .model.hieusuat import ChiSoHieuSuat

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import transaction


from .model.auth import UserAccount


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


class LoginSerializer(serializers.Serializer):
    """
    Serializer đăng nhập bằng email + password.
    """

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs["email"].strip().lower()
        password = attrs["password"]

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Email hoặc password không chính xác.")

        user = authenticate(username=user.username, password=password)

        if user is None:
            raise serializers.ValidationError("Email hoặc password không chính xác.")

        if not user.is_active:
            raise serializers.ValidationError("Tài khoản đã bị khóa.")

        try:
            account = user.employee_account
        except UserAccount.DoesNotExist:
            raise serializers.ValidationError(
                "Tài khoản chưa được liên kết với nhân viên."
            )

        attrs["user"] = user
        attrs["account"] = account

        return attrs


class CreateAccountSerializer(serializers.Serializer):
    """
    Admin dùng serializer này để tạo tài khoản
    cho một nhân viên đã tồn tại.
    """

    ma_nv = serializers.IntegerField()
    password = serializers.CharField(write_only=True, min_length=6)

    is_admin = serializers.BooleanField(default=False)

    def validate_ma_nv(self, value):
        try:
            nhan_vien = NhanVien.objects.get(ma_nv=value)
        except NhanVien.DoesNotExist:
            raise serializers.ValidationError("Nhân viên không tồn tại.")

        if not nhan_vien.email:
            raise serializers.ValidationError("Nhân viên chưa có email.")

        if User.objects.filter(email__iexact=nhan_vien.email).exists():
            raise serializers.ValidationError(
                "Email này đã được sử dụng cho tài khoản khác."
            )

        if UserAccount.objects.filter(nhan_vien=nhan_vien).exists():
            raise serializers.ValidationError("Nhân viên này đã có tài khoản.")

        return value

    @transaction.atomic
    def create(self, validated_data):
        ma_nv = validated_data["ma_nv"]
        password = validated_data["password"]
        is_admin = validated_data["is_admin"]

        nhan_vien = NhanVien.objects.get(ma_nv=ma_nv)

        user = User.objects.create_user(
            username=str(nhan_vien.ma_nv),
            email=nhan_vien.email.strip().lower(),
            password=password,
        )

        user.is_staff = is_admin
        user.is_superuser = is_admin
        user.is_active = True
        user.save(
            update_fields=[
                "is_staff",
                "is_superuser",
                "is_active",
            ]
        )

        account = UserAccount.objects.create(user=user, nhan_vien=nhan_vien)

        return account


class AccountSerializer(serializers.ModelSerializer):
    """
    Trả thông tin tài khoản hiện tại.
    """

    ma_nv = serializers.IntegerField(source="nhan_vien.ma_nv", read_only=True)

    ho_ten = serializers.CharField(source="nhan_vien.ho_ten", read_only=True)

    email = serializers.EmailField(source="user.email", read_only=True)

    role = serializers.SerializerMethodField()

    class Meta:
        model = UserAccount
        fields = [
            "ma_nv",
            "ho_ten",
            "email",
            "role",
        ]

    def get_role(self, obj):
        if obj.user.is_staff:
            return "admin"

        return "user"


class ChangePasswordSerializer(serializers.Serializer):
    """
    Đổi password của tài khoản hiện tại.
    """

    old_password = serializers.CharField(write_only=True)

    new_password = serializers.CharField(write_only=True, min_length=6)

    def validate_old_password(self, value):
        user = self.context["request"].user

        if not user.check_password(value):
            raise serializers.ValidationError("Password hiện tại không chính xác.")

        return value

    def validate_new_password(self, value):
        old_password = self.initial_data.get("old_password")

        if value == old_password:
            raise serializers.ValidationError("Password mới phải khác password cũ.")

        return value

    def save(self, **kwargs):
        user = self.context["request"].user

        user.set_password(self.validated_data["new_password"])

        user.save(update_fields=["password"])

        return user
