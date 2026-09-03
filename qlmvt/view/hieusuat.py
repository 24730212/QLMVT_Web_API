from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from ..model.hieusuat import ChiSoHieuSuat
from ..serializers import ChiSoHieuSuatSerializer
from ..utils.errorhandler import get_sql_error

@api_view(["GET"])
def api_get_ds_cshs(request):
    """ API lấy danh sách chỉ số hiệu suất"""
    try:
        ds_cshs = ChiSoHieuSuat.objects.all()
        serializer = ChiSoHieuSuatSerializer(ds_cshs, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status_code)


@api_view(["GET"])
def api_get_cshs(request, ma_cs):
    """ API lấy chỉ số hiệu suất theo mã chỉ số hiệu suất"""
    try:
        hs = ChiSoHieuSuat.objects.get(ma_cs=ma_cs)
        serializer = ChiSoHieuSuatSerializer(hs)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    
    except ChiSoHieuSuat.DoesNotExist:
        return JsonResponse({
            "error": "Không tìm thấy chỉ số hiệu suất"
        }, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({
            "error":message
        }, status=status_code)