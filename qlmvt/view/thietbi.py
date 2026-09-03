from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from ..model.thietbi import ThietBi
from ..serializers import ThietBiSerializer
from ..utils.errorhandler import get_sql_error

@api_view(["GET"])
def api_get_ds_tb(request):
    """ API lấy danh sách thiết bị"""
    try:
        ds_tb = ThietBi.objects.all()
        serializer = ThietBiSerializer(ds_tb, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status_code)


@api_view(["GET"])
def api_get_tb(request, ma_tb):
    """ API lấy thiết bị theo mã thiết bị"""
    try:
        tb = ThietBi.objects.get(ma_tb=ma_tb)
        serializer = ThietBiSerializer(tb)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    
    except ThietBi.DoesNotExist:
        return JsonResponse({
            "error": "Không tìm thấy thiết bị"
        }, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status_code)


@api_view(["POST"])
def api_create_tb(request): 
    """ API Tạo mới 1 hoặc nhiều thiết bị cùng lúc, ma_tb tự sinh, không được trùng ip"""
    try:
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
        return JsonResponse({
            "error": message
        }, status=status_code)


@api_view(["PUT"])
def api_update_tb(request, ma_tb):
    """API cập nhật thiết bị theo mã thiết bị, tinh_trang bắt buộc"""
    try:
        nv = ThietBi.objects.get(ma_tb=ma_tb)

        serializer = ThietBiSerializer(nv, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except ThietBi.DoesNotExist:
        return JsonResponse({
            "error": "Không tìm thấy thiết bị"
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status_code)


@api_view(["DELETE"])
def api_delete_tb(request, ma_tb):
    """ API xoá thiết bị theo mã thiết bị"""
    try:
        tb = ThietBi.objects.get(ma_tb=ma_tb)

        tb.delete()

        return JsonResponse({
            "message": "Đã xoá thành công"
        }, status=status.HTTP_200_OK)

    except ThietBi.DoesNotExist:
        return JsonResponse({
            "error": "Không tìm thấy thiết bị"
        }, status=status.HTTP_404_NOT_FOUND)
    

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status_code)


@api_view(["GET"])
def api_get_tb_theo_loai_tb(request):
    """API lấy danh sách theo loai thiết bị, khi không truyền -> trả toàn bộ danh sách"""
    try:
        loai_tb = request.GET.get("loai_tb")
        if loai_tb:
            loai_tb = loai_tb.strip()

            ds_tb = ThietBi.objects.filter(
                loai_tb__icontains=loai_tb
            ) # loai_tb có chứa chuỗi truyền vào
        else:
            ds_tb = ThietBi.objects.all()

        if not ds_tb.exists():
            return JsonResponse({
                "error": f"Không tìm thấy {loai_tb}"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = ThietBiSerializer(ds_tb, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
                
    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status_code)