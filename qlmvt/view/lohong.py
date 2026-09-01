from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from ..model.lohong import LoHong
from ..serializers import LoHongSerializer
from ..utils.errorhandler import get_sql_error


@api_view(["GET"])
def api_get_ds_lh(request):
    try:
        ds_lh = LoHong.objects.all()
        serializer = LoHongSerializer(ds_lh, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
    
    except Exception as e:
        message, status = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status)


@api_view(["GET"])
def api_get_lh(request, ma_lh):
    try:
        lh = LoHong.objects.get(ma_lh=ma_lh)
        serializer = LoHongSerializer(lh)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    
    except Exception as e:
        message, status = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status)


@api_view(["POST"])
def api_create_lh(request):
    try:
        data = request.data
        if isinstance(data, list):
            serializer = LoHongSerializer(data=data, many=True)
        else:
            serializer = LoHongSerializer(data=data)

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
def api_update_lh(request, ma_lh):
    try:
        lh = LoHong.objects.get(ma_lh=ma_lh)

        serializer = LoHongSerializer(lh, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)

        return JsonResponse(serializer.errors, status=400)

    except LoHong.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)

    except Exception as e:
        message, status = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status)


@api_view(["DELETE"])
def api_delete_lh(request, ma_lh):
    try:
        lh = LoHong.objects.get(ma_lh=ma_lh)

        lh.delete()

        return JsonResponse({
            "message": "Deleted successfully"
        }, status=200)

    except LoHong.DoesNotExist:
        return JsonResponse({
            "error": "Not found"
        }, status=404)

    except Exception as e:
        message, status = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status)


#API lấy các lỗ hổng đã vá 

#API lấy các lỗ hổng chưa vá

