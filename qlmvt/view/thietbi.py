from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from ..controller import thietbi


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_get_ds_tb(request):
    return thietbi.get_ds_tb(request)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_get_tb(request, ma_tb):
    return thietbi.get_tb(request, ma_tb)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_get_tb_theo_loai_tb(request):
    return thietbi.get_tb_theo_loai_tb(request)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_create_tb(request):
    return thietbi.create_tb(request)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def api_update_tb(request, ma_tb):
    return thietbi.update_tb(request, ma_tb)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def api_delete_tb(request, ma_tb):
    return thietbi.delete_tb(request, ma_tb)
