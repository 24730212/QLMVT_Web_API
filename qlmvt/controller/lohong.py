from django.http import JsonResponse
from django.utils import timezone
from rest_framework import status
from ..model.lohong import LoHong
from ..serializers import LoHongSerializer
from ..utils.sql_error_handler import get_sql_error


def get_ds_lh(request):
    """lấy danh sách lỗ hổng, user chỉ được xem lỗ hổng mình xử lý"""
    try:
        if request.user.is_staff:
            ds_lh = LoHong.objects.all()
        else:
            nv = request.user.employee_account.nhan_vien
            ds_lh = LoHong.objects.filter(manv_xuly=nv.ma_nv)

        serializer = LoHongSerializer(ds_lh, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({"error": message}, status=status_code)


def get_lh(request, ma_lh):
    """lấy lỗ hổng theo mã lỗ hổng, user chỉ được xem lỗ hổng mình xử lý"""
    try:
        lh = LoHong.objects.get(ma_lh=ma_lh)
        if not request.user.is_staff:
            nv = request.user.employee_account.nhan_vien
            if lh.manv_xuly.ma_nv != nv.ma_nv:
                return JsonResponse(
                    {"error": "Bạn không có quyền xem lỗ hổng này"},
                    status=status.HTTP_403_FORBIDDEN,
                )
        serializer = LoHongSerializer(lh)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    except LoHong.DoesNotExist:
        return JsonResponse(
            {"error": "Không tìm thấy lỗ hổng"}, status=status.HTTP_404_NOT_FOUND
        )

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({"error": message}, status=status_code)


def create_lh(request):
    """thêm mới 1 hoặc nhiều lỗ hổng cùng lúc"""
    try:
        if not request.user.is_staff:
            return JsonResponse(
                {"error": "Bạn không có quyền thêm lỗ hổng"},
                status=status.HTTP_403_FORBIDDEN,
            )

        data = request.data.copy()
        if isinstance(data, list):
            for item in data:
                item.pop("ma_lh", None)
                item.setdefault("thoi_gian_xay_ra_su_co", timezone.now())
                item.setdefault("trang_thai_khac_phuc", "Chưa vá")
            serializer = LoHongSerializer(data=data, many=True)
        else:
            data.pop("ma_lh", None)
            data.setdefault("thoi_gian_xay_ra_su_co", timezone.now())
            data.setdefault("trang_thai_khac_phuc", "Chưa vá")
            serializer = LoHongSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        message, status_code = get_sql_error(e)
        # return JsonResponse({"error": message}, status=status_code)
        return JsonResponse({"error": str(e)}, status=status_code)


def update_lh(request, ma_lh):
    """Cập nhật lỗ hổng theo mã lỗ hổng:
    + User chỉ được cập nhật trang_thai_khac_phuc: Chưa vá -> Đang xử lý -> Đã vá
    + Admin:
        + Tất cả trường thông tin trừ ma_lh
        + Chuyển từ Đã vá về Chưa vá/ Đang xử lý
        + Gán nhân viên xử lý, không được gán khi Đang xử lý/ Đã vá
        + Có thể gán nhân viên mới xử lý lh Đã vá nếu đồng thời chuyển qua Chưa vá
    + Thoi gian xu ly su co khong duoc qua 24 gio ke tu thoi gian xay ra su co
    """
    try:
        lh = LoHong.objects.get(ma_lh=ma_lh)
        data = request.data.copy()
        if "ma_lh" in request.data:
            return JsonResponse(
                {"error": "Không được phép sửa mã lỗ hổng"},
                status=status.HTTP_403_FORBIDDEN,
            )
        # Format lại trang_thai_khac_phuc
        new_status = data.get("trang_thai_khac_phuc")
        if new_status:
            status_map = {
                "chưa vá": "Chưa vá",
                "đang xử lý": "Đang xử lý",
                "đã vá": "Đã vá",
            }
            new_status = status_map.get(new_status.strip().lower())
            if not new_status:
                return JsonResponse(
                    {"error": "Trạng thái không hợp lệ"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            data["trang_thai_khac_phuc"] = new_status

        # USER
        if not request.user.is_staff:
            nv = request.user.employee_account.nhan_vien
            if lh.manv_xuly.ma_nv != nv.ma_nv:
                return JsonResponse(
                    {"error": "Bạn không có quyền sửa thông tin lỗ hổng này"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            if set(data.keys()) != {"trang_thai_khac_phuc"}:
                return JsonResponse(
                    {"error": "Nhân viên chỉ được phép cập nhật trang_thai_khac_phuc"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            user_allowed = {"Chưa vá": "Đang xử lý", "Đang xử lý": "Đã vá"}
            if user_allowed.get(lh.trang_thai_khac_phuc) != new_status:
                return JsonResponse(
                    {
                        "error": "Trạng thái chỉ được chuyển theo thứ tự: "
                        "Chưa vá -> Đang xử lý -> Đã vá"
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )
        # ADMIN
        else:
            # Không cho đổi nhân viên khi đang xử lý hoặc đã vá
            if (
                lh.trang_thai_khac_phuc in {"Đang xử lý", "Đã vá"}
                and "manv_xuly" in data
                and data["manv_xuly"] != lh.manv_xuly.ma_nv
            ):
                # Chỉ có thể đổi nhân viên nếu đồng thời chuyển về "Chưa vá" (gán cho nhân viên khác làm)
                if not (
                    lh.trang_thai_khac_phuc == "Đã vá"
                    and data.get("trang_thai_khac_phuc") == "Chưa vá"
                ):
                    return JsonResponse(
                        {
                            "error": "Lỗ hổng đang/đã được xử lý, không thể phân công nhân viên khác"
                        },
                        status=status.HTTP_403_FORBIDDEN,
                    )
            # Admin chỉ trả Đã vá -> Chưa vá
            if lh.trang_thai_khac_phuc == "Đã vá" and new_status == "Chưa vá":
                lh.thoi_gian_xu_ly_su_co = None

        # Khi Đã vá -> tự động cập nhật thời gian hoàn thành
        if new_status == "Đã vá":
            lh.thoi_gian_xu_ly_su_co = timezone.now()

        serializer = LoHongSerializer(lh, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            if new_status in ["Đã vá", "Chưa vá"]:
                lh.save(update_fields=["thoi_gian_xu_ly_su_co"])
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except LoHong.DoesNotExist:
        return JsonResponse(
            {"error": "Không tìm thấy lỗ hổng"}, status=status.HTTP_404_NOT_FOUND
        )

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({"error": message}, status=status_code)


def delete_lh(request, ma_lh):
    """xoá lỗ hổng theo mã lỗ hổng"""
    try:
        if not request.user.is_staff:
            return JsonResponse(
                {"error": "Bạn không có quyền xoá lỗ hổng"},
                status=status.HTTP_403_FORBIDDEN,
            )
        lh = LoHong.objects.get(ma_lh=ma_lh)

        lh.delete()

        return JsonResponse({"message": "Đã xoá thành công"}, status=status.HTTP_200_OK)

    except LoHong.DoesNotExist:
        return JsonResponse(
            {"error": "Không tìm thấy lỗ hổng"}, status=status.HTTP_404_NOT_FOUND
        )

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({"error": message}, status=status_code)


def get_lh_theo_trangthai(request):
    """lấy các lỗ hổng đã vá / chưa vá / đang xử lý: ?trang_thai
    + User chỉ được xem lỗ hổng mình xử lý
    + Admin xem toàn bộ
    """
    try:
        trang_thai = request.GET.get("trang_thai")
        status_map = {
            "fixed": "Đã vá",
            "unfixed": "Chưa vá",
            "processing": "Đang xử lý",
        }
        filters = {}
        if trang_thai:
            if trang_thai not in status_map:
                return JsonResponse(
                    {"error": "Trạng thái không hợp lệ"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            filters["trang_thai_khac_phuc"] = status_map[trang_thai]

        if not request.user.is_staff:
            nv = request.user.employee_account.nhan_vien
            filters["manv_xuly"] = nv.ma_nv

        lohong = LoHong.objects.filter(**filters)

        if not lohong.exists():
            return JsonResponse(
                {
                    "error": f"Không tìm thấy lỗ hổng với tình trạng {status_map[trang_thai]}"
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = LoHongSerializer(lohong, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({{"error": message}}, status=status_code)
