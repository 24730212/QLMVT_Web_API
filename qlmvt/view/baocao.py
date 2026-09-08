from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from ..controller import baocao


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_get_bao_cao_tong_quan(request):
    return baocao.get_bao_cao_tong_quan(request)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_get_tong_loi_nv_xu_ly(request):
    return baocao.get_tong_loi_nv_xu_ly(request)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_get_kpi_nhan_vien(request):
    return baocao.get_kpi_nhan_vien(request)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_get_tinh_trang_lo_hong(request):
    return baocao.get_tinh_trang_lo_hong(request)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_get_lo_hong_theo_thiet_bi(request):
    return baocao.get_lo_hong_theo_thiet_bi(request)
