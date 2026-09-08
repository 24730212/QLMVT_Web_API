from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from ..model.lienket import LienKet
from ..serializers import LienKetSerializer
from ..utils.sql_error_handler import get_sql_error
from ..controller import lienket


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_get_ds_lk(request):
    return lienket.get_ds_lk(request)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_get_lk(request, ma_lk):
    return lienket.get_lk(request, ma_lk)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_create_lk(request):
    return lienket.create_lk(request)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def api_update_lk(request, ma_lk):
    return lienket.update_lk(request, ma_lk)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def api_delete_lk(request, ma_lk):
    return lienket.delete_lk(request, ma_lk)
