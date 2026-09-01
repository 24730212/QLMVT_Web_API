from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from ..model.nhatkyloi import NhatKyLoi
from ..serializers import NhatKyLoiSerializer
from ..utils.errorhandler import get_sql_error

@api_view(["GET"])
def api_get_ds_nkl(request):
    try:
        ds_nkl = NhatKyLoi.objects.all()
        serializer = NhatKyLoiSerializer(ds_nkl, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
    
    except Exception as e:
        message, status = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status)

    

@api_view(["GET"])
def api_get_nkl(request, ma_nkl):
    try:
        nkl = NhatKyLoi.objects.get(ma_nkl=ma_nkl)
        serializer = NhatKyLoiSerializer(nkl)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    
    except Exception as e:
        message, status = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status)


@api_view(["POST"])
def api_create_nkl(request):
    try:
        data = request.data
        if isinstance(data, list):
            serializer = NhatKyLoiSerializer(data=data, many=True)
        else:
            serializer = NhatKyLoiSerializer(data=data)

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
def api_update_nkl(request, ma_nkl):
    try:
        nkl = NhatKyLoi.objects.get(ma_nkl=ma_nkl)

        serializer = NhatKyLoiSerializer(nkl, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)

        return JsonResponse(serializer.errors, status=400)

    except NhatKyLoi.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)

    except Exception as e:
        message, status = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status)


@api_view(["DELETE"])
def api_delete_nkl(request, ma_nkl):
    try:
        nkl = NhatKyLoi.objects.get(ma_nkl=ma_nkl)

        nkl.delete()

        return JsonResponse({
            "message": "Deleted successfully"
        }, status=200)

    except NhatKyLoi.DoesNotExist:
        return JsonResponse({
            "error": "Not found"
        }, status=404)

    except Exception as e:
        message, status = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status)


#API lấy lỗi chưa xử lý

#API phân công nhân viên xử lý lỗi