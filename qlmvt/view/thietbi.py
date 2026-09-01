from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from ..model.thietbi import ThietBi
from ..serializers import ThietBiSerializer
from ..utils.errorhandler import get_sql_error

@api_view(["GET"])
def api_get_ds_tb(request):
    try:
        ds_tb = ThietBi.objects.all()
        serializer = ThietBiSerializer(ds_tb, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
    except Exception as e:
        message, status = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status)


@api_view(["GET"])
def api_get_tb(request, ma_tb):
    try:
        tb = ThietBi.objects.get(ma_tb=ma_tb)
        serializer = ThietBiSerializer(tb)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        message, status = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status)


@api_view(["POST"])
def api_create_tb(request):
    try:
        data = request.data
        if isinstance(data, list):
            serializer = ThietBiSerializer(data=data, many=True)
        else:
            serializer = ThietBiSerializer(data=data)

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
def api_update_tb(request, ma_tb):
    try:
        nv = ThietBi.objects.get(ma_tb=ma_tb)

        serializer = ThietBiSerializer(nv, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)

        return JsonResponse(serializer.errors, status=400)

    except ThietBi.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)

    except Exception as e:
        message, status = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status)


@api_view(["DELETE"])
def api_delete_tb(request, ma_tb):
    try:
        tb = ThietBi.objects.get(ma_tb=ma_tb)

        tb.delete()

        return JsonResponse({
            "message": "Deleted successfully"
        }, status=200)

    except ThietBi.DoesNotExist:
        return JsonResponse({
            "error": "Not found"
        }, status=404)

    except Exception as e:
        message, status = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status)