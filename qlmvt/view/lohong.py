from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from ..controller import lohong


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_get_ds_lh(request):
    """API lấy danh sách lỗ hổng, user chỉ được xem lỗ hổng mình xử lý"""
    return lohong.get_ds_lh(request)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_get_lh(request, ma_lh):
    """API lấy lỗ hổng theo mã lỗ hổng, user chỉ được xem lỗ hổng mình xử lý"""
    return lohong.get_lh(request, ma_lh)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_create_lh(request):
    """API thêm mới 1 hoặc nhiều lỗ hổng cùng lúc"""
    return lohong.create_lh(request)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def api_update_lh(request, ma_lh):
    """API cập nhật lỗ hổng theo mã lỗ hổng"""
    return lohong.update_lh(request, ma_lh)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def api_delete_lh(request, ma_lh):
    """API xoá lỗ hổng theo mã lỗ hổng"""
    return lohong.delete_lh(request, ma_lh)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_get_lh_theo_trangthai(request):
    """API lấy các lỗ hổng đã vá / chưa vá / đang xử lý: ?trang_thai"""
    return lohong.get_lh_theo_trangthai(request)
