from django.http import JsonResponse
from rest_framework import status
from ..model.nhanvien import NhanVien
from ..model.thietbi import ThietBi
from ..model.lohong import LoHong
from ..model.hieusuat import ChiSoHieuSuat
from ..model.nhatkyloi import NhatKyLoi
from ..model.lienket import LienKet
from ..utils.sql_error_handler import get_sql_error
from ..services.baocao_service import BaoCaoService


def get_bao_cao_tong_quan(request):
    """lấy tổng quan số lượng dữ liệu trong hệ thống"""
    try:
        # Admin xem toàn bộ
        if request.user.is_staff:
            nhat_ky_loi = NhatKyLoi.objects.all()
            lo_hong = LoHong.objects.all()
        # User chỉ xem của user xử lý
        else:
            nv = request.user.employee_account.nhan_vien
            nhat_ky_loi = NhatKyLoi.objects.filter(manv_xuly=nv.ma_nv)

            lo_hong = LoHong.objects.filter(manv_xuly=nv.ma_nv)

        data = {
            "nhan_vien": NhanVien.objects.count(),
            "thiet_bi": ThietBi.objects.count(),
            "lien_ket": LienKet.objects.count(),
            "nhat_ky_loi": {
                "tong": nhat_ky_loi.count(),
                "da_xu_ly": nhat_ky_loi.filter(da_xu_ly=True).count(),
                "chua_xu_ly": nhat_ky_loi.filter(da_xu_ly=False).count(),
            },
            "lo_hong": {
                "tong": lo_hong.count(),
                "da_va": lo_hong.filter(trang_thai_khac_phuc="Đã vá").count(),
                "chua_va": lo_hong.filter(trang_thai_khac_phuc="Chưa vá").count(),
                "dang_xu_ly": lo_hong.filter(trang_thai_khac_phuc="Đang xử lý").count(),
            },
            "chi_so_hieu_suat": ChiSoHieuSuat.objects.count(),
        }

        return JsonResponse(data, status=status.HTTP_200_OK)

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({"error": message}, status=status_code)


def get_tong_loi_nv_xu_ly(request):
    """lấy tổng lỗi nhân viên đã + đang xử lý"""
    try:
        if request.user.is_staff:
            nhan_vien = NhanVien.objects.all()
        else:
            nv = request.user.employee_account.nhan_vien
            nhan_vien = NhanVien.objects.filter(ma_nv=nv.ma_nv)

        result = []

        for nv in nhan_vien:

            su_co = NhatKyLoi.objects.filter(manv_xuly=nv.ma_nv)

            tong = su_co.count()
            da_xu_ly = su_co.filter(da_xu_ly=True).count()
            dang_xu_ly = su_co.filter(da_xu_ly=False).count()

            result.append(
                {
                    "ma_nv": nv.ma_nv,
                    "ho_ten": nv.ho_ten,
                    "su_co": {
                        "tong": tong,
                        "da_xu_ly": da_xu_ly,
                        "dang_xu_ly": dang_xu_ly,
                    },
                }
            )

        result.sort(key=lambda x: x["su_co"]["tong"], reverse=True)

        return JsonResponse(result, status=status.HTTP_200_OK, safe=False)
    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({"error": message}, status=status_code)


def get_kpi_nhan_vien(request):
    """thống kê KPI của nhân viên gổm tổng lỗi + lỗ hổng đã xử lý xong"""

    try:
        if request.user.is_staff:
            # Admin → xem tất cả
            data = BaoCaoService.get_kpi_nhan_vien()
        else:
            # User → chỉ xem bản thân
            nv = request.user.employee_account.nhan_vien
            data = BaoCaoService.get_kpi_nhan_vien(nv.ma_nv)

        return JsonResponse(data, status=status.HTTP_200_OK, safe=False)

    except Exception as e:
        message, status_code = get_sql_error(e)

        return JsonResponse({"error": message}, status=status_code)


def get_tinh_trang_lo_hong(request):
    """lấy thống kê số lượng lỗ hổng theo trạng thái khác phục"""
    try:
        if request.user.is_staff:
            # Admin → tất cả lỗ hổng
            lo_hong = LoHong.objects.all()

        else:
            # User → chỉ lỗ hổng mình xử lý
            nv = request.user.employee_account.nhan_vien

            lo_hong = LoHong.objects.filter(manv_xuly=nv.ma_nv)
        data = {
            "tong": lo_hong.count(),
            "da_va": lo_hong.filter(trang_thai_khac_phuc="Đã vá").count(),
            "chua_va": lo_hong.filter(trang_thai_khac_phuc="Chưa vá").count(),
            "dang_xu_ly": lo_hong.filter(trang_thai_khac_phuc="Đang xử lý").count(),
        }

        return JsonResponse(data, status=status.HTTP_200_OK)

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({"error": message}, status=status_code)


def get_lo_hong_theo_thiet_bi(request):
    """thống kê số lỗ hổng theo thiết bị"""
    try:
        data = BaoCaoService.get_lo_hong_theo_thiet_bi()

        return JsonResponse(data, status=status.HTTP_200_OK, safe=False)

    except Exception as e:
        message, status_code = get_sql_error(e)

        return JsonResponse({"error": message}, status=status_code)
