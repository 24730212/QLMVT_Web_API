from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from ..controller import nhatkyloi


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_get_ds_nkl(request):
    return nhatkyloi.get_ds_nkl(request)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_get_nkl(request, ma_loi):
    return nhatkyloi.get_nkl(request, ma_loi)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_get_nkl_theo_xuly(request):
    return nhatkyloi.get_nkl_theo_xuly(request)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_create_nkl(request):
    return nhatkyloi.create_nkl(request)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def api_update_nkl(request, ma_loi):
    return nhatkyloi.update_nkl(request, ma_loi)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def api_phan_cong_nv_xuly_loi(request, ma_loi):
    return nhatkyloi.phan_cong_nv_xuly_loi(request, ma_loi)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def api_delete_nkl(request, ma_loi):
    return nhatkyloi.delete_nkl(request, ma_loi)
