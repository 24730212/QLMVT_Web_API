from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from ..controller import hieusuat


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_get_ds_cshs(request):
    """API lấy danh sách chỉ số hiệu suất"""
    return hieusuat.get_ds_cshs(request)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_get_cshs(request, ma_cs):
    """API lấy chỉ số hiệu suất theo mã chỉ số hiệu suất"""
    return hieusuat.get_cshs(request, ma_cs)
