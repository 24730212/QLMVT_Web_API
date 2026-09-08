from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from ..controller import nhanvien


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_get_ds_nv(request):
    return nhanvien.get_ds_nv(request)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_get_nv(request, ma_nv):
    return nhanvien.get_nv(request, ma_nv)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_create_nv(request):
    return nhanvien.create_nv(request)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def api_update_nv(request, ma_nv):
    return nhanvien.update_nv(request, ma_nv)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def api_delete_nv(request, ma_nv):
    return nhanvien.delete_nv(request, ma_nv)
