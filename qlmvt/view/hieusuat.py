from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from ..model.chisohieusuat import ChiSoHieuSuat
from ..serializers import ChiSoHieuSuatSerializer


@api_view(["GET"])
def api_get_ds_hs(request):
    ds_hs = ChiSoHieuSuat.objects.all()
    serializer = ChiSoHieuSuatSerializer(ds_hs, many=True)
    return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)


@api_view(["GET"])
def api_get_hs(request, ma_hs):
    try:
        hs = ChiSoHieuSuat.objects.get(ma_hs=ma_hs)
        serializer = ChiSoHieuSuatSerializer(hs)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    except ChiSoHieuSuat.DoesNotExist:
        return JsonResponse({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)
