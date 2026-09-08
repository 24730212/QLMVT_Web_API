from django.http import JsonResponse
from django.utils import timezone
from rest_framework import status
from ..model.nhatkyloi import NhatKyLoi
from ..model.nhanvien import NhanVien
from ..serializers import NhatKyLoiSerializer
from ..utils.sql_error_handler import get_sql_error


def get_ds_nkl(request):
    """lấy danh sách nhật ký lỗi"""
    try:
        if request.user.is_staff:
            ds_nkl = NhatKyLoi.objects.all()
        else:
            nv = request.user.employee_account.nhan_vien

            # User chỉ xem các lỗi được phân công cho mình
            ds_nkl = NhatKyLoi.objects.filter(manv_xuly=nv.ma_nv)

        serializer = NhatKyLoiSerializer(ds_nkl, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({"error": message}, status=status_code)


def get_nkl(request, ma_loi):
    """lấy bản ghi nhật ký lỗi theo mã lỗi, user chỉ được xem lỗi được phân công cho user đó"""
    try:
        nkl = NhatKyLoi.objects.get(ma_loi=ma_loi)
        # User chỉ được xem lỗi được phân công cho mình
        if not request.user.is_staff:
            nv = request.user.employee_account.nhan_vien

            if nkl.manv_xuly.ma_nv != int(nv.ma_nv):
                return JsonResponse(
                    {"error": "Bạn không có quyền xem nhật ký lỗi này"},
                    status=status.HTTP_403_FORBIDDEN,
                )

        serializer = NhatKyLoiSerializer(nkl)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    except NhatKyLoi.DoesNotExist:
        return JsonResponse(
            {"error": "Không tìm thấy nhật ký lỗi"}, status=status.HTTP_404_NOT_FOUND
        )

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({"error": message}, status=status_code)


def create_nkl(request):
    """tạo mới log lỗi, chỉ ADMIN được xử lý:
    + ma_loi tự sinh
    + thoi_gian_loi nếu không truyền thì tự động sinh với timezone
    + da_xu_ly là bắt buộc
    +
    """
    try:
        if not request.user.is_staff:
            return JsonResponse(
                {"error": "Bạn không có quyền tạo nhật ký lỗi"},
                status=status.HTTP_403_FORBIDDEN,
            )

        data = request.data.copy()
        if isinstance(data, list):
            for item in data:
                item.pop("ma_loi", None)
                item.setdefault("thoi_gian_loi", timezone.now())
            serializer = NhatKyLoiSerializer(data=data, many=True)
        else:
            data.pop("ma_loi", None)
            data.setdefault("thoi_gian_loi", timezone.now())
            serializer = NhatKyLoiSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({"error": message}, status=status_code)


def update_nkl(request, ma_loi):
    """hàm cập nhật nhật ký lỗi
    ADMIN:
        + được cập nhật tất cả trừ ma_loi, thoi_gian_hoan_thanh, thoi_gian_loi
    USER:
        + chỉ được sửa lỗi mình xử lý, chỉ được cập nhật da_xu_ly: False -> True
        + thoi_gian_hoan_thanh tự động log timezone

    """
    try:
        nkl = NhatKyLoi.objects.get(ma_loi=ma_loi)

        # Không cho sửa các field hệ thống
        forbidden = {"ma_loi", "thoi_gian_loi", "thoi_gian_hoan_thanh"}
        if forbidden.intersection(request.data.keys()):
            return JsonResponse(
                {"error": "Không được phép sửa mã lỗi và thời gian"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # USER
        if not request.user.is_staff:
            nv = request.user.employee_account.nhan_vien

            if nkl.manv_xuly.ma_nv != nv.ma_nv:
                return JsonResponse(
                    {"error": "Bạn không có quyền sửa nhật ký lỗi này"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            if set(request.data.keys()) != {"da_xu_ly"}:
                return JsonResponse(
                    {"error": "Nhân viên chỉ được phép cập nhật da_xu_ly"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            if nkl.da_xu_ly or request.data["da_xu_ly"] is not True:
                return JsonResponse(
                    {"error": "Chỉ được chuyển da_xu_ly từ false sang true"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            nkl.da_xu_ly = True
            nkl.thoi_gian_hoan_thanh = timezone.now()
            nkl.save(update_fields=["da_xu_ly", "thoi_gian_hoan_thanh"])

        # ADMIN
        else:
            data = request.data.copy()

            if "da_xu_ly" in data:
                if not nkl.da_xu_ly and data["da_xu_ly"] is True:
                    nkl.thoi_gian_hoan_thanh = timezone.now()

                elif nkl.da_xu_ly and data["da_xu_ly"] is False:
                    nkl.thoi_gian_hoan_thanh = None

            serializer = NhatKyLoiSerializer(nkl, data=data, partial=True)

            if not serializer.is_valid():
                return JsonResponse(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

            nkl = serializer.save()

            # Lưu thời gian hoàn thành tự động
            if "da_xu_ly" in data:
                nkl.save(update_fields=["da_xu_ly", "thoi_gian_hoan_thanh"])

        return JsonResponse(NhatKyLoiSerializer(nkl).data, status=status.HTTP_200_OK)

    except NhatKyLoi.DoesNotExist:
        return JsonResponse(
            {"error": "Không tìm thấy nhật ký lỗi"}, status=status.HTTP_404_NOT_FOUND
        )

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({"error": message}, status=status_code)


def delete_nkl(request, ma_loi):
    """xoá bản ghi nhât ký lỗi theo mã lỗi, chỉ admin được phép"""
    try:
        if not request.user.is_staff:
            return JsonResponse(
                {"error": "Bạn không có quyền xoá nhật ký lỗi"},
                status=status.HTTP_403_FORBIDDEN,
            )
        nkl = NhatKyLoi.objects.get(ma_loi=ma_loi)

        nkl.delete()

        return JsonResponse({"message": "Đã xoá thành công"}, status=status.HTTP_200_OK)

    except NhatKyLoi.DoesNotExist:
        return JsonResponse(
            {"error": "Không tìm thấy nhật ký lỗi"}, status=status.HTTP_404_NOT_FOUND
        )

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({"error": message}, status=status_code)


def get_nkl_theo_xuly(request):
    """lấy các lỗi chưa xử lý / đã xử lý: ?da_xu_ly=true|false
    User chỉ được xem các lỗi của mình, admin xem tất cả
    """
    try:
        da_xu_ly = request.GET.get("da_xu_ly")
        if request.user.is_staff:
            filters = {}

        else:
            nv = request.user.employee_account.nhan_vien
            filters = {"manv_xuly": nv.ma_nv}

        if da_xu_ly is not None:
            if da_xu_ly.lower() == "true":
                filters["da_xu_ly"] = True
            elif da_xu_ly.lower() == "false":
                filters["da_xu_ly"] = False
            else:
                return JsonResponse(
                    {"error": "da_xu_ly phải là true hoặc false"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        ds_nkl = NhatKyLoi.objects.filter(**filters)

        if not ds_nkl.exists():
            return JsonResponse(
                {"error": f"Không tìm thấy lỗi với da_xu_ly = {da_xu_ly}"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = NhatKyLoiSerializer(ds_nkl, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({{"error": message}}, status=status_code)


def phan_cong_nv_xuly_loi(request, ma_loi):
    """phân công nhân viên xử lý lỗi theo mã lỗi, manv_xuly bắt buộc có tồn tại"""
    try:
        if not request.user.is_staff:
            return JsonResponse(
                {"error": "Bạn không có quyền phân công nhân viên xử lý lỗi"},
                status=status.HTTP_403_FORBIDDEN,
            )
        nkl = NhatKyLoi.objects.get(ma_loi=ma_loi)

        if nkl.da_xu_ly == True:
            return JsonResponse(
                {
                    "error": f"Lỗi đã xử lý xong, không thể phân công lại nhân viên xử lý"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        ma_nv = request.data.get("manv_xuly")
        if not ma_nv:
            return JsonResponse(
                {"error": "Vui lòng cung cấp mã nhân viên xử lý"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        NhanVien.objects.get(ma_nv=ma_nv)

        da_xu_ly = request.data.get("da_xu_ly")
        new_data = request.data
        if not da_xu_ly:
            new_data["da_xu_ly"] = False

        serializer = NhatKyLoiSerializer(nkl, data=new_data)
        serializer.is_valid()
        serializer.save()
        return JsonResponse(
            {"message": "Phân công nhân viên xử lý lỗi thành công"},
            status=status.HTTP_200_OK,
        )

    except NhatKyLoi.DoesNotExist:
        return JsonResponse(
            {"error": f"Lỗi {ma_loi} không tồn tại"}, status=status.HTTP_404_NOT_FOUND
        )

    except NhanVien.DoesNotExist:
        return JsonResponse(
            {"error": "Nhân viên không tồn tại"}, status=status.HTTP_404_NOT_FOUND
        )

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({{"error": message}}, status=status_code)
