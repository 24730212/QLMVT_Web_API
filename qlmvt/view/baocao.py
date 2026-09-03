from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from ..model.nhanvien import NhanVien
from ..model.thietbi import ThietBi
from ..model.lohong import LoHong
from ..model.hieusuat import ChiSoHieuSuat
from ..model.nhatkyloi import NhatKyLoi
from ..model.lienket import LienKet
from ..utils.errorhandler import get_sql_error
from ..services.baocao_service import BaoCaoService


@api_view(["GET"])
def api_get_bao_cao_tong_quan(request):
    """API lấy tổng quan số lượng dữ liệu trong hệ thống"""
    try:
        data = {
            "nhan_vien": NhanVien.objects.count(),
            "thiet_bi": ThietBi.objects.count(),
            "lien_ket": LienKet.objects.count(),
            "nhat_ky_loi": {
                "tong": NhatKyLoi.objects.count(),
                "da_xu_ly": NhatKyLoi.objects.filter(da_xu_ly=True).count(),
                "chua_xu_ly": NhatKyLoi.objects.filter(da_xu_ly=False).count(),
            },
            "lo_hong": {
                "tong": LoHong.objects.count(),
                "da_va": LoHong.objects.filter(trang_thai_khac_phuc="Đã vá").count(),
                "chua_va": LoHong.objects.filter(
                    trang_thai_khac_phuc="Chưa vá"
                ).count(),
                "dang_xu_ly": LoHong.objects.filter(
                    trang_thai_khac_phuc="Đang xử lý"
                ).count(),
            },
            "chi_so_hieu_suat": ChiSoHieuSuat.objects.count(),
        }

        return JsonResponse(data, status=status.HTTP_200_OK)

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({"error": message}, status=status_code)


@api_view(["GET"])
def api_get_tong_loi_nv_xu_ly(request):
    """API lấy tổng lỗi nhân viên đã + đang xử lý"""
    try:
        nhan_vien = NhanVien.objects.all()

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


@api_view(["GET"])
def api_get_kpi_nhan_vien(request):
    """API thống kê KPI của nhân viên gổm tổng lỗi + lỗ hổng đã xử lý xong"""

    try:
        data = BaoCaoService.get_kpi_nhan_vien()

        return JsonResponse(data, status=status.HTTP_200_OK, safe=False)

    except Exception as e:
        message, status_code = get_sql_error(e)

        return JsonResponse({"error": message}, status=status_code)


@api_view(["GET"])
def api_get_tinh_trang_lo_hong(request):
    """API lấy thống kê số lượng lỗ hổng theo trạng thái khác phục"""
    try:
        data = {
            "tong": LoHong.objects.count(),
            "da_va": LoHong.objects.filter(trang_thai_khac_phuc="Đã vá").count(),
            "chua_va": LoHong.objects.filter(trang_thai_khac_phuc="Chưa vá").count(),
            "dang_xu_ly": LoHong.objects.filter(
                trang_thai_khac_phuc="Đang xử lý"
            ).count(),
        }

        return JsonResponse(data, status=status.HTTP_200_OK)

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({"error": message}, status=status_code)


@api_view(["GET"])
def api_get_lo_hong_theo_thiet_bi(request):
    """API thống kê số lỗ hổng theo thiết bị"""
    try:
        data = BaoCaoService.get_lo_hong_theo_thiet_bi()

        return JsonResponse(data, status=status.HTTP_200_OK, safe=False)

    except Exception as e:
        message, status_code = get_sql_error(e)

        return JsonResponse({"error": message}, status=status_code)
