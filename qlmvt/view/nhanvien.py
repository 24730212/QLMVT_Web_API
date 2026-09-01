from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from ..model.nhanvien import NhanVien
from ..serializers import NhanVienSerializer
from ..utils.errorhandler import get_sql_error

@api_view(["GET"])
def api_get_ds_nv(request):
    try:
        ds_nv = NhanVien.objects.all()
        serializer = NhanVienSerializer(ds_nv, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
    
    except Exception as e:
        message, status = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status)


@api_view(["GET"])
def api_get_nv(request, ma_nv):
    try:
        nv = NhanVien.objects.get(ma_nv=ma_nv)
        serializer = NhanVienSerializer(nv)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    
    except Exception as e:
        message, status = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status)


@api_view(["POST"])
def api_create_nv(request):
    try:
        data = request.data
        if isinstance(data, list):
            serializer = NhanVienSerializer(data=data, many=True)
        else:
            serializer = NhanVienSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)

        return JsonResponse(serializer.errors, status=400)
    
    except Exception as e:
        message, status = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status)


@api_view(["PUT"])
def api_update_nv(request, ma_nv):
    try:
        nv = NhanVien.objects.get(ma_nv=ma_nv)

        serializer = NhanVienSerializer(nv, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)

        return JsonResponse(serializer.errors, status=400)

    except NhanVien.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)

    except Exception as e:
        message, status = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status)


@api_view(["DELETE"])
def api_delete_nv(request, ma_nv):
    try:
        nv = NhanVien.objects.get(ma_nv=ma_nv)

        nv.delete()

        return JsonResponse({
            "message": "Deleted successfully"
        }, status=200)

    except NhanVien.DoesNotExist:
        return JsonResponse({
            "error": "Not found"
        }, status=404)

    except Exception as e:
        message, status = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status)