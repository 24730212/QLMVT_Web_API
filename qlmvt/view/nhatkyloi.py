from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from ..model.nhatkyloi import NhatKyLoi
from ..model.nhanvien import NhanVien
from ..serializers import NhatKyLoiSerializer
from ..utils.errorhandler import get_sql_error

@api_view(["GET"])
def api_get_ds_nkl(request):
    """ API lấy danh sách nhật ký lỗi"""
    try:
        ds_nkl = NhatKyLoi.objects.all()
        serializer = NhatKyLoiSerializer(ds_nkl, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
    
    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status_code)

    

@api_view(["GET"])
def api_get_nkl(request, ma_loi):
    """ API lấy bản ghi nhật ký lỗi theo mã lỗi"""
    try:
        nkl = NhatKyLoi.objects.get(ma_loi=ma_loi)
        serializer = NhatKyLoiSerializer(nkl)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    
    except NhatKyLoi.DoesNotExist:
            return JsonResponse({
                "error": "Không tìm thấy nhật ký lỗi"
            }, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status_code)


@api_view(["POST"])
def api_create_nkl(request):
    """ API tạo mới log lỗi, da_xu_ly là bắt buộc"""
    try:
        data = request.data
        if isinstance(data, list):
            serializer = NhatKyLoiSerializer(data=data, many=True)
        else:
            serializer = NhatKyLoiSerializer(data=data)

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
def api_update_nkl(request, ma_loi):
    """ API cập nhật thông tin bản ghi nhật ký lỗi, da_xu_ly là bắt buộc"""
    try:
        nkl = NhatKyLoi.objects.get(ma_loi=ma_loi)

        serializer = NhatKyLoiSerializer(nkl, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except NhatKyLoi.DoesNotExist:
        return JsonResponse({
            "error": "Không tìm thấy nhật ký lỗi"
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status_code)


@api_view(["DELETE"])
def api_delete_nkl(request, ma_loi):
    """ API xoá bản ghi nhât ký lỗi theo mã lỗi"""
    try:
        nkl = NhatKyLoi.objects.get(ma_loi=ma_loi)

        nkl.delete()

        return JsonResponse({
            "message": "Đã xoá thành công"
        }, status=status.HTTP_200_OK)

    except NhatKyLoi.DoesNotExist:
        return JsonResponse({
            "error": "Không tìm thấy nhật ký lỗi"
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        message, status_code = get_sql_error(e)
        return JsonResponse({
            "error": message
        }, status=status_code)


@api_view(["GET"])
def api_get_nkl_theo_xuly(request):
    """ API lấy các lỗi chưa xử lý / đã xử lý: ?da_xu_ly """
    try:
        da_xu_ly = request.GET.get("da_xu_ly")

        if da_xu_ly is None:
            ds_nkl = NhatKyLoi.objects.all()
        elif da_xu_ly.lower() == "true":
            ds_nkl = NhatKyLoi.objects.filter(da_xu_ly=True)
        elif da_xu_ly.lower()=="false":
            ds_nkl = NhatKyLoi.objects.filter(da_xu_ly=False)
        else:
            return JsonResponse({
                "error": "da_xu_ly phải là true hoặc false"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not ds_nkl.exists():
            return JsonResponse({
                "error": f"Không tìm thấy lỗi với da_xu_ly = {da_xu_ly}"
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = NhatKyLoiSerializer(ds_nkl, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    
    except Exception as e:
        message, status_code=get_sql_error(e)
        return JsonResponse({{
            "error": message
        }}, status=status_code)


@api_view(["PUT"])
def api_phan_cong_nv_xuly_loi(request, ma_loi):
    """API phân công nhân viên xử lý lỗi theo mã lỗi, manv_xuly bắt buộc có tồn tại"""
    try:
        nkl = NhatKyLoi.objects.get(ma_loi=ma_loi)
        
        if nkl.da_xu_ly == True:
            return JsonResponse({
                "error": f"Lỗi đã xử lý xong, không thể phân công lại nhân viên xử lý"
            }, status=status.HTTP_404_NOT_FOUND)
        
        ma_nv = request.data.get("manv_xuly")
        if not ma_nv:
            return JsonResponse({
                "error":"Vui lòng cung cấp mã nhân viên xử lý"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        NhanVien.objects.get(ma_nv = ma_nv)

        da_xu_ly = request.data.get("da_xu_ly")
        new_data = request.data
        if not da_xu_ly:
            new_data["da_xu_ly"]=False

        serializer = NhatKyLoiSerializer(nkl, data=new_data)
        serializer.is_valid()
        serializer.save()
        return JsonResponse({
            "message":"Phân công nhân viên xử lý lỗi thành công"
        }, status=status.HTTP_200_OK)

    except NhatKyLoi.DoesNotExist:
            return JsonResponse({
                "error": f"Lỗi {ma_loi} không tồn tại"
            }, status=status.HTTP_404_NOT_FOUND)    

    except NhanVien.DoesNotExist:
        return JsonResponse({
            "error":"Nhân viên không tồn tại"
        }, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
            message, status_code=get_sql_error(e)
            return JsonResponse({{
                "error": message
            }}, status=status_code)