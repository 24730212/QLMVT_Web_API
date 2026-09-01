from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from ..model.lienket import LienKet
from ..serializers import LienKetSerializer
from ..utils.errorhandler import get_sql_error


@api_view(["GET"])
def api_get_ds_lk(request):
    try:
        ds_lk = LienKet.objects.all()
        serializer = LienKetSerializer(ds_lk, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
    
    except Exception as e:
        message, status = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status)


@api_view(["GET"])
def api_get_lk(request, ma_lk):
    try:
        lk = LienKet.objects.get(ma_lk=ma_lk)
        serializer = LienKetSerializer(lk)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    
    except Exception as e:
        message, status = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status)


@api_view(["POST"])
def api_create_lk(request):
    try:
        data = request.data
        if isinstance(data, list):
            serializer = LienKetSerializer(data=data, many=True)
        else:
            serializer = LienKetSerializer(data=data)

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
def api_update_lk(request, ma_lk):
    try:
        lk = LienKet.objects.get(ma_lk=ma_lk)

        serializer = LienKetSerializer(lk, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)

        return JsonResponse(serializer.errors, status=400)

    except LienKet.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)

    except Exception as e:
        message, status = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status)


@api_view(["DELETE"])
def api_delete_lk(request, ma_lk):
    try:
        lk = LienKet.objects.get(ma_lk=ma_lk)

        lk.delete()

        return JsonResponse({
            "message": "Deleted successfully"
        }, status=200)

    except LienKet.DoesNotExist:
        return JsonResponse({
            "error": "Not found"
        }, status=404)

    except Exception as e:
        message, status = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status)