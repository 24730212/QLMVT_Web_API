from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from ..utils.sql_error_handler import get_sql_error
from datetime import datetime, timezone

# from rest_framework.authtoken.models import Token


from ..model.auth import UserAccount
from ..model.nhanvien import NhanVien
from ..serializers import (
    LoginSerializer,
    CreateAccountSerializer,
    AccountSerializer,
    ChangePasswordSerializer,
)


def login(request):
    """Đăng nhập bằng email + password truyền qua body"""
    try:
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return JsonResponse(
                {"error": serializer.errors}, status=status.HTTP_401_UNAUTHORIZED
            )

        user = serializer.validated_data["user"]
        account = serializer.validated_data["account"]

        # Tạo token + expired time
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        access_expired_at = datetime.fromtimestamp(access["exp"], tz=timezone.utc)

        refresh_expired_at = datetime.fromtimestamp(refresh["exp"], tz=timezone.utc)

        role = "admin" if user.is_staff else "user"

        return JsonResponse(
            {
                "message": "Đăng nhập thành công",
                "access_token": str(access),
                "access_expired_at": access_expired_at.isoformat(),
                "refresh_token": str(refresh),
                "refresh_expired_at": refresh_expired_at.isoformat(),
                "user": {
                    "ma_nv": account.nhan_vien.ma_nv,
                    "ho_ten": account.nhan_vien.ho_ten,
                    "email": user.email,
                    "role": role,
                },
            },
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({"error": message}, status=status_code)


def logout(request):
    """Đăng xuất bằng blacklist refreshtoken truyền ở body"""
    refresh_token = request.data.get("refresh")

    if not refresh_token:
        return JsonResponse(
            {"error": "Thiếu refresh token"}, status=status.HTTP_400_BAD_REQUEST
        )
    try:
        token = RefreshToken(refresh_token)

        # Blacklist refresh token
        token.blacklist()

        return JsonResponse(
            {"message": "Đăng xuất thành công"}, status=status.HTTP_200_OK
        )

    except TokenError:
        return JsonResponse(
            {"error": "Refresh token không hợp lệ hoặc đã hết hạn"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({"error": message}, status=status_code)


def get_me(request):
    """
    Lấy thông tin tài khoản đang đăng nhập.
    Header: Authorization: Bearer <access_token>
    """

    try:
        account = request.user.employee_account
        serializer = AccountSerializer(account)

        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    except Exception:
        return JsonResponse(
            {"error": ("Tài khoản chưa được liên kết với nhân viên.")},
            status=status.HTTP_404_NOT_FOUND,
        )


def create_account(request):
    """
    Admin tạo tài khoản cho nhân viên.
    Body:
    {
        "ma_nv": 21,
        "password": "123456",
        "is_admin": false
    }
    """

    serializer = CreateAccountSerializer(data=request.data)

    if not serializer.is_valid():
        return JsonResponse(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )
    try:
        account = serializer.save()

        return JsonResponse(
            {
                "message": "Tạo tài khoản thành công",
                "account": AccountSerializer(account).data,
            },
            status=status.HTTP_201_CREATED,
        )
    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({"error": message}, status=status_code)


def change_password(request):
    """
    User/Admin đổi password của chính mình.
    Body:
    {
        "old_password": "123456",
        "new_password": "654321"
    }
    """

    serializer = ChangePasswordSerializer(
        data=request.data, context={"request": request}
    )

    if not serializer.is_valid():
        return JsonResponse(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    serializer.save()

    # Xóa token cũ, người dùng phải login lại sau khi đổi password.
    try:
        serializer.save()

        return JsonResponse(
            {"message": "Đổi password thành công. Vui lòng đăng nhập lại."},
            status=status.HTTP_200_OK,
        )

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({"error": message}, status=status_code)
