from django.http import JsonResponse
from rest_framework import status
from ..model.nhanvien import NhanVien
from ..serializers import NhanVienSerializer
from ..utils.sql_error_handler import get_sql_error


def get_ds_nv(request):
    """lấy danh sách nhân viên - Admin và User đều được xem"""
    try:
        ds_nv = NhanVien.objects.all()
        serializer = NhanVienSerializer(ds_nv, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({"error": message}, status=status_code)


def get_nv(request, ma_nv):
    """lấy nhân viên theo mã nhân viên - Admin xem tất cả, User chỉ xem chính mình"""
    try:
        # User chỉ được xem chính mình
        if not request.user.is_staff:
            nv_user = request.user.employee_account.nhan_vien

            if nv_user.ma_nv != int(ma_nv):
                return JsonResponse(
                    {"error": "Bạn không có quyền xem thông tin nhân viên này"},
                    status=status.HTTP_403_FORBIDDEN,
                )
        nv = NhanVien.objects.get(ma_nv=ma_nv)
        serializer = NhanVienSerializer(nv)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    except NhanVien.DoesNotExist:
        return JsonResponse(
            {"error": "Không tìm thấy nhân viên"}, status=status.HTTP_404_NOT_FOUND
        )

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({"error": message}, status=status_code)


def create_nv(request):
    """thêm 1 hoặc nhiều nhân viên cùng lúc, chỉ admin được thêm"""
    try:
        if not request.user.is_staff:
            return JsonResponse(
                {"error": "Bạn không có quyền thêm nhân viên"},
                status=status.HTTP_403_FORBIDDEN,
            )
        data = request.data
        if isinstance(data, list):
            serializer = NhanVienSerializer(data=data, many=True)
        else:
            serializer = NhanVienSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({"error": message}, status=status_code)


def update_nv(request, ma_nv):
    """cập nhật thông tin nhân viên"""
    try:
        nv = NhanVien.objects.get(ma_nv=ma_nv)
        # User chỉ được sửa chính mình và không được tự sửa vai trò, chuyên môn
        if not request.user.is_staff:
            nv_user = request.user.employee_account.nhan_vien

            if nv_user.ma_nv != int(ma_nv):
                return JsonResponse(
                    {"error": "Bạn không có quyền sửa thông tin nhân viên này"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            # Không được sửa vai trò
            if "vai_tro" in request.data:
                return JsonResponse(
                    {"error": "Bạn không được phép sửa vai trò"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Không được sửa chuyên môn
            if "chuyen_mon" in request.data:
                return JsonResponse(
                    {"error": "Bạn không được phép sửa chuyên môn"},
                    status=status.HTTP_403_FORBIDDEN,
                )

        serializer = NhanVienSerializer(nv, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except NhanVien.DoesNotExist:
        return JsonResponse(
            {"error": "Không tìm thấy nhân viên"}, status=status.HTTP_404_NOT_FOUND
        )

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({"error": message}, status=status_code)


def delete_nv(request, ma_nv):
    """xoá nhân viên theo mã nhân viên, user không được phép, không được xoá admin (đã xử lý ở SQL)"""
    try:
        if not request.user.is_staff:
            return JsonResponse(
                {"error": "Bạn không có quyền xoá thông tin nhân viên"},
                status=status.HTTP_403_FORBIDDEN,
            )

        nv = NhanVien.objects.get(ma_nv=ma_nv)

        nv.delete()

        return JsonResponse({"message": "Đã xoá thành công"}, status=status.HTTP_200_OK)

    except NhanVien.DoesNotExist:
        return JsonResponse(
            {"error": "Không tìm thấy nhân viên"}, status=status.HTTP_404_NOT_FOUND
        )

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({"error": message}, status=status_code)
