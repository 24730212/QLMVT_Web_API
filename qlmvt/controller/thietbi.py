from django.http import JsonResponse
from rest_framework import status
from ..model.thietbi import ThietBi
from ..serializers import ThietBiSerializer
from ..utils.sql_error_handler import get_sql_error


def get_ds_tb(request):
    """lấy danh sách thiết bị"""
    try:
        ds_tb = ThietBi.objects.all()
        serializer = ThietBiSerializer(ds_tb, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({"error": message}, status=status_code)


def get_tb(request, ma_tb):
    """lấy thiết bị theo mã thiết bị"""
    try:
        tb = ThietBi.objects.get(ma_tb=ma_tb)
        serializer = ThietBiSerializer(tb)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    except ThietBi.DoesNotExist:
        return JsonResponse(
            {"error": "Không tìm thấy thiết bị"}, status=status.HTTP_404_NOT_FOUND
        )

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({"error": message}, status=status_code)


def get_tb_theo_loai_tb(request):
    """lấy danh sách theo loai thiết bị, khi không truyền -> trả toàn bộ danh sách"""
    try:
        loai_tb = request.GET.get("loai_tb")
        if loai_tb:
            loai_tb = loai_tb.strip()

            ds_tb = ThietBi.objects.filter(
                loai_tb__icontains=loai_tb
            )  # loai_tb có chứa chuỗi truyền vào
        else:
            ds_tb = ThietBi.objects.all()

        if not ds_tb.exists():
            return JsonResponse(
                {"error": f"Không tìm thấy {loai_tb}"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ThietBiSerializer(ds_tb, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({"error": message}, status=status_code)


def create_tb(request):
    """Tạo mới 1 hoặc nhiều thiết bị cùng lúc, ma_tb tự sinh, không được trùng ip"""
    try:
        if not request.user.is_staff:
            return JsonResponse(
                {"error": "Bạn không có quyền thêm thiết bị"},
                status=status.HTTP_403_FORBIDDEN,
            )
        data = request.data
        if isinstance(data, list):
            serializer = ThietBiSerializer(data=data, many=True)
        else:
            serializer = ThietBiSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({"error": message}, status=status_code)


def update_tb(request, ma_tb):
    """cập nhật thiết bị theo mã thiết bị, tinh_trang bắt buộc"""
    try:
        if not request.user.is_staff:
            return JsonResponse(
                {"error": "Bạn không có quyền sửa thiết bị"},
                status=status.HTTP_403_FORBIDDEN,
            )
        nv = ThietBi.objects.get(ma_tb=ma_tb)

        if "ma_tb" in request.data:
            return JsonResponse(
                {"error": "Không được phép sửa mã thiết bị"},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = ThietBiSerializer(nv, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except ThietBi.DoesNotExist:
        return JsonResponse(
            {"error": "Không tìm thấy thiết bị"}, status=status.HTTP_404_NOT_FOUND
        )

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({"error": message}, status=status_code)


def delete_tb(request, ma_tb):
    """xoá thiết bị theo mã thiết bị, user không được phép"""
    try:
        if not request.user.is_staff:
            return JsonResponse(
                {"error": "Bạn không có quyền xoá thiết bị"},
                status=status.HTTP_403_FORBIDDEN,
            )
        tb = ThietBi.objects.get(ma_tb=ma_tb)

        tb.delete()

        return JsonResponse({"message": "Đã xoá thành công"}, status=status.HTTP_200_OK)

    except ThietBi.DoesNotExist:
        return JsonResponse(
            {"error": "Không tìm thấy thiết bị"}, status=status.HTTP_404_NOT_FOUND
        )

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({"error": message}, status=status_code)
