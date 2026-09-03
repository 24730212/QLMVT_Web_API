from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from ..model.lohong import LoHong
from ..serializers import LoHongSerializer
from ..utils.errorhandler import get_sql_error


@api_view(["GET"])
def api_get_ds_lh(request):
    """ API lấy danh sách lỗ hổng"""
    try:
        ds_lh = LoHong.objects.all()
        serializer = LoHongSerializer(ds_lh, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status_code)


@api_view(["GET"])
def api_get_lh(request, ma_lh):
    """ API lấy lỗ hổng theo mã lỗ hổng"""
    try:
        lh = LoHong.objects.get(ma_lh=ma_lh)
        serializer = LoHongSerializer(lh)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    except LoHong.DoesNotExist:
        return JsonResponse({
            "error": "Không tìm thấy lỗ hổng"
        }, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status_code)


@api_view(["POST"])
def api_create_lh(request):
    """ API thêm mới 1 hoặc nhiều lỗ hổng cùng lúc"""
    try:
        data = request.data
        if isinstance(data, list):
            serializer = LoHongSerializer(data=data, many=True)
        else:
            serializer = LoHongSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status_code)


@api_view(["PUT"])
def api_update_lh(request, ma_lh):
    """ API cập nhật lỗ hổng theo mã lỗ hổng"""
    try:
        lh = LoHong.objects.get(ma_lh=ma_lh)

        serializer = LoHongSerializer(lh, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except LoHong.DoesNotExist:
        return JsonResponse({
            "error": "Không tìm thấy lỗ hổng"
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status_code)


@api_view(["DELETE"])
def api_delete_lh(request, ma_lh):
    """ API xoá lỗ hổng theo mã lỗ hổng"""
    try:
        lh = LoHong.objects.get(ma_lh=ma_lh)

        lh.delete()

        return JsonResponse({
            "message": "Đã xoá thành công"
        }, status=status.HTTP_200_OK)

    except LoHong.DoesNotExist:
        return JsonResponse({
            "error": "Không tìm thấy lỗ hổng"
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status_code)


@api_view(["GET"])
def api_get_lh_theo_trangthai(request):
    """API lấy các lỗ hổng đã vá / chưa vá / đang xử lý: ?trang_thai"""
    try:
        trang_thai = request.GET.get("trang_thai")
        status_map = {
            "fixed" : "Đã vá",
            "unfixed" : "Chưa vá",
            "processing" : "Đang xử lý"
        }

        if trang_thai:
            if trang_thai not in status_map:
                return JsonResponse({
                    "error": "Trạng thái không hợp lệ"
                }, status=status.HTTP_400_BAD_REQUEST)
            lohong = LoHong.objects.filter(trang_thai_khac_phuc=status_map[trang_thai])
        else:
            lohong = LoHong.objects.all()

        if not lohong.exists():
            return JsonResponse({
                "error": f"Không tìm thấy lỗ hổng với tình trạng {status_map[trang_thai]}"
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = LoHongSerializer(lohong, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        message, status_code=get_sql_error(e)
        return JsonResponse({{
            "error": message
        }}, status=status_code)


