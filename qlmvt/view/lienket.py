from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from ..model.lienket import LienKet
from ..serializers import LienKetSerializer
from ..utils.errorhandler import get_sql_error


@api_view(["GET"])
def api_get_ds_lk(request):
    """ API lấy danh sách liên kết"""
    try:
        ds_lk = LienKet.objects.all()
        serializer = LienKetSerializer(ds_lk, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status_code)


@api_view(["GET"])
def api_get_lk(request, ma_lk):
    """ API lầy liên kết theo mã liên kết"""
    try:
        lk = LienKet.objects.get(ma_lk=ma_lk)
        serializer = LienKetSerializer(lk)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    
    except LienKet.DoesNotExist:
        return JsonResponse({
            "error": "Không tìm thấy liên kết"
        }, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status_code)


@api_view(["POST"])
def api_create_lk(request):
    """ API thêm mới 1 hoặc nhiều liên kết cùng lúc"""
    try:
        data = request.data
        if isinstance(data, list):
            serializer = LienKetSerializer(data=data, many=True)
        else:
            serializer = LienKetSerializer(data=data)

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
def api_update_lk(request, ma_lk):
    """ API cập nhật liên kết"""
    try:
        lk = LienKet.objects.get(ma_lk=ma_lk)

        serializer = LienKetSerializer(lk, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except LienKet.DoesNotExist:
        return JsonResponse({
            "error": "Không tìm thấy liên kết"
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status_code)


@api_view(["DELETE"])
def api_delete_lk(request, ma_lk):
    """ API xoá liên kết theo mã liên kết"""
    try:
        lk = LienKet.objects.get(ma_lk=ma_lk)

        lk.delete()

        return JsonResponse({
            "message": "Đã xoá thành công"
        }, status=status.HTTP_200_OK)

    except LienKet.DoesNotExist:
        return JsonResponse({
            "error": "Không tìm thấy liên kết"
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status_code)