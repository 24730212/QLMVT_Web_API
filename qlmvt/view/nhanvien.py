from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from ..model.nhanvien import NhanVien
from ..serializers import NhanVienSerializer
from ..utils.errorhandler import get_sql_error

@api_view(["GET"])
def api_get_ds_nv(request):
    """ API lấy danh sách nhân viên"""
    try:
        ds_nv = NhanVien.objects.all()
        serializer = NhanVienSerializer(ds_nv, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status_code)


@api_view(["GET"])
def api_get_nv(request, ma_nv):
    """ API lấy nhân viên theo mã nhân viên"""
    try:
        nv = NhanVien.objects.get(ma_nv=ma_nv)
        serializer = NhanVienSerializer(nv)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    except NhanVien.DoesNotExist:
                return JsonResponse({
                    "error": "Không tìm thấy nhân viên"
                }, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status_code)


@api_view(["POST"])
def api_create_nv(request):
    """ API thêm 1 hoặc nhiều nhân viên cùng lúc"""
    try:
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
        return JsonResponse({
            "error": message
        }, status=status_code)


@api_view(["PUT"])
def api_update_nv(request, ma_nv):
    """ API cập nhật thông tin nhân viên"""
    try:
        nv = NhanVien.objects.get(ma_nv=ma_nv)

        serializer = NhanVienSerializer(nv, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except NhanVien.DoesNotExist:
        return JsonResponse({
            "error": "Không tìm thấy nhân viên"
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status_code)


@api_view(["DELETE"])
def api_delete_nv(request, ma_nv):
    """ API xoá nhân viên theo mã nhân viên, không được xoá admin (đã xử lý ở SQL) """
    try:
        nv = NhanVien.objects.get(ma_nv=ma_nv)

        nv.delete()

        return JsonResponse({
            "message": "Đã xoá thành công"
        }, status=status.HTTP_200_OK)

    except NhanVien.DoesNotExist:
        return JsonResponse({
            "error": "Không tìm thấy nhân viên"
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status_code)